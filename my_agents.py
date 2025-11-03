# ---------------------------------------------------------------------------
# A self-contained multi-agent orchestration pipeline using Gemini (ADK style)
# ---------------------------------------------------------------------------

#from google.adk.agents import Agent
#from google.adk.models import Gemini
#from google.adk.tools import FunctionTool
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ---------------------- ENV & MODEL ----------------------
load_dotenv()
#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash-lite"
#model = genai.GenerativeModel("gemini-2.0-pro")
#model = Gemini(api_key=GEMINI_API_KEY,model_name="gemini-2.5-pro",)

# ---------------------- HELPER FUNCTIONS ----------------------
def send_email(recipient: str, subject: str, body: str) -> dict:
    print(f"📧 Sending email to {recipient} with subject '{subject}'")
    return {"status": "sent", "recipient": recipient, "subject": subject}

def google_search(query: str) -> str:
    print(f"🔎 Searching Google for: {query}")
    # In a production system, this would call a real search API
    return f"Simulated Google results for '{query}'"

def load_files_from_folder(folder_path: str) -> list:
    """Read all text files from a folder and return list of contents."""
    contents = []
    for fname in os.listdir(folder_path):
        full_path = os.path.join(folder_path, fname)
        if os.path.isfile(full_path):
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    contents.append(f"\n\n--- FILE: {fname} ---\n" + f.read())
            except Exception as e:
                contents.append(f"[Error reading {fname}: {str(e)}]")
    return contents

def load_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        # For now, just return a placeholder if file cannot be read
        return f"[Could not read {os.path.basename(file_path)}]"

# ---------------------- AGENT CLASSES ----------------------
class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    def generate_text(self, prompt: str, max_tokens: int = 300) -> str:
        # Correct current SDK usage
        #response = genai.generate(
           # model=MODEL_NAME,
          #   max_output_tokens=max_tokens
        #)
        #return response.output_text.strip()
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()

class CleanerAgent(BaseAgent):
    def __init__(self):
        super().__init__("CleanerAgent")
        #self.description = "Cleans and summarizes input text"
        #self.model = model

    def run(self, text: str) -> str:
        prompt = (
            "Clean and summarize the following text. "
            "Focus on key information and remove noise:\n\n"
            f"{text}"
        )
        #response = genai.generate(
        #    model=self.model,
        #    prompt=prompt,
        #    max_output_tokens=300
        #)        
        #return response.text.strip()
        return self.generate_text(prompt)


class WranglerAgent(BaseAgent):
    def __init__(self):
        super().__init__("WranglerAgent")

    def run(self, summary: str) -> str:
        prompt = (
            "Based on the following summary, draft a polite and professional "
            "email requesting missing or incomplete records:\n\n"
            f"{summary}"
        )
        return self.generate_text(prompt)

class ClientAgent(BaseAgent):
    def __init__(self):
        super().__init__("ClientAgent")

    def run(self, summary: str) -> str:
        prompt = (
            "Draft a concise, professional, and empathetic client update based on this summary:\n\n"
            f"{summary}"
        )
        return self.generate_text(prompt)

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("ResearchAgent")

    def run(self, summary: str) -> str:
        query = f"Relevant legal precedents for: {summary}"
        search_results = google_search(query)
        prompt = f"Summarize and interpret the following search results:\n{search_results}"
        return self.generate_text(prompt)


def select_agents_ai(summary: str) -> list:
    """
    Ask the AI which agents to run based on the summary.
    Returns a list of agent names.
    """
    prompt = f"""
    Based on the following summary, decide which of these agents should run next: 
    - WranglerAgent: drafts requests for missing or incomplete records
    - ClientAgent: drafts client updates
    - ResearchAgent: researches legal precedents

    Summary:
    {summary}

    Return a JSON array of agent names to run.
    Example: ["ClientAgent", "ResearchAgent"]
    """
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    
    try:
        # Try parsing AI response as JSON
        import json
        agents = json.loads(response.text.strip())
        # Filter out invalid agent names
        valid_agents = ["WranglerAgent", "ClientAgent", "ResearchAgent"]
        agents = [a for a in agents if a in valid_agents]
        return agents
    except Exception as e:
        print("Error parsing AI agent selection:", e)
        return []

# ---------------------- ORCHESTRATOR ----------------------
def orchestrate_case(file_contents: list, optional_prompt: str = "") -> dict:
    combined_text = "\n".join(file_contents)

    cleaner = CleanerAgent()
    wrangler = WranglerAgent()
    client = ClientAgent()
    researcher = ResearchAgent()

    # Step 1: Clean & summarize
    print("🧹 Running CleanerAgent...")
    try:
        summary = cleaner.run(combined_text)
    except Exception as e:
        return {"summary": "[Error in summarization]", "tasks": [], "error": str(e)}

    # Step 2: Decide which agents to run
    if optional_prompt.strip():
        # Use keyword-based routing if prompt exists
        prompt_lower = optional_prompt.lower()
        tasks_to_run = []
        if any(word in prompt_lower for word in ["record", "missing", "request"]):
            tasks_to_run.append(("request_records", wrangler))
        if any(word in prompt_lower for word in ["client", "update", "inform"]):
            tasks_to_run.append(("email_client", client))
        if any(word in prompt_lower for word in ["research", "precedent", "legal", "case"]):
            tasks_to_run.append(("research_case", researcher))
    else:
        # Let AI choose agents automatically
        agent_names = select_agents_ai(summary)
        tasks_to_run = []
        for name in agent_names:
            if name == "WranglerAgent":
                tasks_to_run.append(("request_records", wrangler))
            elif name == "ClientAgent":
                tasks_to_run.append(("email_client", client))
            elif name == "ResearchAgent":
                tasks_to_run.append(("research_case", researcher))

    # Step 3: Execute selected agents (if any)
    if not tasks_to_run:
        return {"summary": summary, "tasks": []}

    results = []
    for task_type, agent in tasks_to_run:
        print(f"🤖 Running {agent.name} for task '{task_type}'...")
        try:
            output = agent.run(summary)
        except Exception as e:
            output = f"[Error: {str(e)}]"
        results.append({
            "task": task_type,
            "agent": agent.name,
            "result": output
        })

    return {"summary": summary, "tasks": results}

#disregard
#pipeline = SequentialAgent(
#    name="CasePipeline",
#    sub_agents=[cleaner_agent, wrangler_agent, client_agent, research_agent]
#)

# ---------------------- MAIN EXECUTION TESTING ----------------------
if __name__ == "__main__":
    # Example: process a folder of text files (or just dummy strings)
    dummy_files = [
        "Client case: Missing medical records and pending insurance approval.",
        "Email from hospital: Request for updated consent form.",
        "Court notice: Submission deadline next week."
    ]

    result = orchestrate_case(dummy_files, optional_prompt="Focus on urgent client updates.")
    print("\n\n🧾 FINAL OUTPUT ----------------------")
    print(result)
