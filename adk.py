#from adk import Agent, Session
#from adk.models import GeminiModel
#from adk.tools import Tool, ToolParameter, google_search, http_request, file_read, pdf_extract, file_write
from adk import Agent, Session, GeminiModel, Tool, ToolParameter
from dotenv import load_dotenv
import os
import json

# load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# initialize model
model = GeminiModel(
    api_key=os.getenv("GEMINI_API_KEY"),
    model_name="gemini-2.5-pro",
)

# initialized functions used in the tools
def send_email(recipient: str, subject: str, body: str):
    print(f"Sending email to {recipient} with subject '{subject}'")
    return {"status": "sent", "recipient": recipient}

def summarized_text_tool_func(text: str):
    """
    Summarizes the given text using GeminiModel.
    """
    response = model.generate(f"Summarize the following text concisely:\n{text}")
    return response.text

def read_file_tool(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    
def google_search(query: str):
    print(f"🔎 Searching Google for: {query}")
    # Replace with real API call later
    return f"Simulated search results for '{query}'"
    
# simple in-memory calendar
calendar_store = []
def calendar_api_tool_func(action: str, event_name: str = "", date: str = ""):
    """
    action: 'add' or 'view'
    event_name: name of the event to add
    date: date of the event (string)
    """
    if action == "add":
        calendar_store.append({"event": event_name, "date": date})
        return f"Event '{event_name}' added on {date}."
    elif action == "view":
        if not calendar_store:
            return "No events scheduled."
        return "\n".join([f"{ev['date']}: {ev['event']}" for ev in calendar_store])
    else:
        return "Invalid action. Use 'add' or 'view'."


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

summarized_text_tool = Tool(
    name="summarized_text",
    description="Summarizes text into concise points",
    parameters=[
        ToolParameter("text", "string", "Text to summarize")
    ],
    function=summarized_text_tool_func
)


file_read_tool = Tool(
    name="file_read",
    description="Reads content from a file",
    parameters=[ToolParameter("file_path", "string", "Path to file")],
    function=read_file_tool
)

search_tool = Tool(
    name="google_search",
    description="Searches the web for legal cases or relevant information",
    parameters=[ToolParameter("query", "string", "Search query")],
    function=google_search
)

calendar_api_tool = Tool(
    name="calendar_api",
    description="Add or view calendar events",
    parameters=[
        ToolParameter("action", "string", "Action to perform: add or view"),
        ToolParameter("event_name", "string", "Name of the event"),
        ToolParameter("date", "string", "Date of the event")
    ],
    function=calendar_api_tool_func
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

    # ask user for confirmation
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

# initializes all the agents
cleaner_agent = Agent(
    name="cleanerAgent",
    model=model,
    tools=[file_read_tool, summarized_text_tool], 
    description="Cleans, parses, and organizes raw input files and text into structured JSON.",
    instruction= "Extract key content (emails, texts, transcripts) and remove irrelevant noise or duplicates."
)

wrangler_agent = Agent(
    name="WranglerAgent",
    model=model,
    tools=[send_email_tool],  
    description="Finds missing records or bills, and drafts requests to providers.",
    instruction= "When records or bills are missing, draft polite requests or follow-up messages to obtain them."

)

scheduler_agent = Agent(
    name="SchedulerAgent",
    model=model,
    tools=[calendar_api_tool],  
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
    tools=[search_tool], 
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

if __name__ == "__main__":
    # load files from a folder
    folder_path = "mock_data/emails"  # replace with your actual folder
    input_data = load_files_from_folder(folder_path)

    # call the orchestrator with the loaded content
    orchestrate_case([input_data])

    # print a summary of the calendar (if scheduler tasks added events)
    print("\n📅 Current calendar events:")
    print(calendar_api_tool_func("view"))
