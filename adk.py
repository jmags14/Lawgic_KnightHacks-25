from adk import Agent, Session
from adk.models import GeminiModel
from adk.tools import Tool, ToolParameter, google_search, http_request, file_read, pdf_extract, file_write
from dotenv import load_dotenv
import os
import json

# load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# initialize model
model = GeminiModel(
    api_key=os.getenv("GEMINI_API_KEY"),
    model_name="gemini-2.0-flash",
)

def send_email(recipient: str, subject: str, body: str):
    print(f"Sending email to {recipient} with subject '{subject}'")
    return {"status": "sent", "recipient": recipient}

# initializes all the tools
send_email_tool = Tool(
    name="send_email",
    description="Send an email to a client or provider",
    parameters=[
        ToolParameter("recipient", "string", "Email address"),
        ToolParameter("subject", "string", "Email subject"),
        ToolParameter("body", "string", "Email content")
    ],
    function=send_email    
)

calendar_api_tool

summarized_text

# initializes all the agents
cleaner_agent = Agent(
    name="cleanerAgent",
    model=model,
    tools=[file_read, pdf_extract, summarized_text], 
    description="Cleans, parses, and organizes raw input files and text into structured JSON.",
    instruction= "Extract key content (emails, texts, transcripts) and remove irrelevant noise or duplicates."
)

wrangler_agent = Agent(
    name="WranglerAgent",
    model=model,
    tools=[send_email_tool, http_request],  
    description="Finds missing records or bills, and drafts requests to providers.",
    instruction= "When records or bills are missing, draft polite requests or follow-up messages to obtain them."

)

scheduler_agent = Agent(
    name="SchedulerAgent",
    model=model,
    tools=[calendar_api],  
    description="Coordinates depositions, mediations, or medical appointments.",
    instruction= "Schedule appointments and confirm availability. Prepare calendar-ready data."
)

client_agent = Agent(
    name="ClientAgent",
    model=model,
    tools=[send_email_tool], 
    description="Drafts empathetic, professional messages to clients on behalf of the firm.",
    instruction= "Ensure all communication is kind, professional, and clear to clients."
)

research_agent = Agent(
    name="ResearchAgent",
    model=model,
    tools=[google_search], 
    description="Finds supporting verdicts or legal precedents to strengthen a case.",
    instruction= "Use search tools or case summaries to suggest useful case law or arguments."
)

manager_agent = Agent(
    name="ManagerAgent",
    model=model,
    tools=[orchestrate_case], 
    description="Reads all content, detects actionable tasks, and routes them to the right specialist.",
    instruction= """
        Read the cleaned input. Identify actionable tasks (e.g., scheduling, emailing clients, or requesting records).
        If an actionable task is found, ask the user if they want to continue. 
        If yes, return a JSON list like this:
        {
            "tasks": [
                {"type": "request_records", "agent": "WranglerAgent"},
                {"type": "schedule_appointment", "agent": "SchedulerAgent"}
            ]
        }
    """
)

# main orchestration function
def orchestrate_case(files: list, optional_prompt: str = ""):
    # clean and normalize data first
    cleaned_output = cleaner_agent.run(
        f"Clean and summarize these files: {files}"
    )

    # then detect actionable tasks
    print("\n[ManagerAgent] Detecting actionable tasks...")
    detection_result = manager_agent.run(cleaned_output)

    try:
        task_data = json.loads(detection_result)
        tasks = task_data.get("tasks", [])
    except Exception as e:
        print(f" Could not parse task output: {e}")
        tasks = []

    # 3. Ask user for confirmation
    for task in tasks:
        task_type = task["type"]
        assigned_agent = task["agent"]
        print(f"\nDetected Task: {task_type} → Suggested Agent: {assigned_agent}")
        user_input = input("Continue with this task? (yes/no): ").strip().lower()

        if user_input == "yes":
            if assigned_agent == "RecordsWrangler":
                wrangler_agent.run(cleaned_output)
            elif assigned_agent == "ClientCommunicationGuru":
                client_agent.run(cleaned_output)
            elif assigned_agent == "LegalResearcher":
                research_agent.run(cleaned_output)
            elif assigned_agent == "VoiceBotScheduler":
                scheduler_agent.run(cleaned_output)
            elif assigned_agent == "EvidenceSorter":
                evidence_agent.run(cleaned_output)
            else:
                print(f"No known agent for {assigned_agent}")
        else:
            print("Skipping task.")

#load files from a folder
def load_files_from_folder(folder_path):
    content = ""
    for fname in os.listdir(folder_path):
        with open(os.path.join(folder_path, fname), "r", encoding="utf-8") as f:
            content += f"\n\n--- FILE: " + fname + " ---\n" + f.read()
    return content

