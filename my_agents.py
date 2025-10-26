#from adk import Agent, GeminiModel, Tool, ToolParameter
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools import Tool, ToolParameter
from dotenv import load_dotenv
import os
import json

model = Gemini(model="gemini-2.5-pro")

# ---------------------- ENV & MODEL ----------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = Gemini(       #not geminimodel now
    api_key=GEMINI_API_KEY,
    model_name="gemini-2.5-pro",
)

# ---------------------- TOOLS ----------------------
def send_email(recipient: str, subject: str, body: str):
    print(f"Sending email to {recipient} with subject '{subject}'")
    return {"status": "sent", "recipient": recipient}

def summarized_text_tool_func(text: str):
    response = model.generate(f"Summarize the following text concisely:\n{text}")
    return response.text

def read_file_tool(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def google_search(query: str):
    print(f"🔎 Searching Google for: {query}")
    return f"Simulated search results for '{query}'"

# ---------------------- TOOL OBJECTS ----------------------
send_email_tool = Tool(
    name="send_email",
    description="Send an email",
    parameters=[
        ToolParameter("recipient", "string"),
        ToolParameter("subject", "string"),
        ToolParameter("body", "string")
    ],
    function=send_email
)

summarized_text_tool = Tool(
    name="summarized_text",
    description="Summarizes text",
    parameters=[ToolParameter("text", "string")],
    function=summarized_text_tool_func
)

file_read_tool = Tool(
    name="file_read",
    description="Read a file",
    parameters=[ToolParameter("file_path", "string")],
    function=read_file_tool
)

search_tool = Tool(
    name="google_search",
    description="Search the web",
    parameters=[ToolParameter("query", "string")],
    function=google_search
)

# ---------------------- AGENTS ----------------------
cleaner_agent = Agent(
    name="CleanerAgent",
    model=model,
    tools=[file_read_tool, summarized_text_tool],
    description="Cleans and summarizes input text",
    instruction="Extract key content and remove irrelevant noise"
)

wrangler_agent = Agent(
    name="WranglerAgent",
    model=model,
    tools=[send_email_tool],
    description="Draft requests for missing records",
    instruction="Draft polite requests for missing records"
)

client_agent = Agent(
    name="ClientAgent",
    model=model,
    tools=[send_email_tool],
    description="Draft messages to clients",
    instruction="Draft professional and empathetic client messages"
)

research_agent = Agent(
    name="ResearchAgent",
    model=model,
    tools=[search_tool],
    description="Find legal precedents",
    instruction="Search for relevant legal cases"
)

# ---------------------- HELPER FUNCTIONS ----------------------
def load_files_from_folder(folder_path):
    content = ""
    for fname in os.listdir(folder_path):
        full_path = os.path.join(folder_path, fname)
        if os.path.isfile(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                content += f"\n\n--- FILE: " + fname + " ---\n" + f.read()
    return content

# ---------------------- ORCHESTRATOR ----------------------
def orchestrate_case(file_contents: list, optional_prompt: str = ""):
    """
    Sequentially processes files with agents and returns structured JSON.
    """
    combined_text = "\n".join(file_contents)
    
    # clean & summarize text
    summary = cleaner_agent.run(f"Summarize this text:\n{combined_text}\n{optional_prompt}")
    
    # detect tasks (static mapping for demonstration)
    tasks = [
        {"type": "request_records", "agent": "WranglerAgent"},
        {"type": "email_client", "agent": "ClientAgent"},
        {"type": "research_case", "agent": "ResearchAgent"},
    ]
    
    # loop through tasks and execute corresponding agent
    task_results = []
    for task in tasks:
        agent_name = task["agent"]
        if agent_name == "WranglerAgent":
            result = wrangler_agent.run(summary)
        elif agent_name == "ClientAgent":
            result = client_agent.run(summary)
        elif agent_name == "ResearchAgent":
            result = research_agent.run(summary)
        else:
            result = f"No agent found for {agent_name}"
        task_results.append({"task": task["type"], "agent": agent_name, "result": result})
    
    # return structured JSON
    return {
        "summary": summary,
        "tasks": task_results
    }
