from crewai import Crew, Process, LLM
from agents import create_agents
from tasks import create_tasks
from dotenv import load_dotenv
import os

load_dotenv()


AGENT_STEPS = [
    {"key": "analysis", "label": "Requirement Analyst", "description": "Decomposing requirements into modules, entities, and endpoints..."},
    {"key": "schemas", "label": "Database Architect", "description": "Designing normalized database schemas with relationships..."},
    {"key": "api", "label": "API Architect", "description": "Designing RESTful API specification with endpoints..."},
    {"key": "pseudocode", "label": "Logic Designer", "description": "Writing pseudocode for core business logic..."},
]


def run_crew(requirement: str, on_task_complete=None) -> dict:
    """Assembles and kicks off the CrewAI crew. Returns a dict with all 4 task outputs."""

    llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3,
    )

    agents = create_agents(llm)
    tasks = create_tasks(agents, requirement)

    # Attach per-task callbacks for live progress
    if on_task_complete:
        for i, task in enumerate(tasks):
            step = AGENT_STEPS[i]
            task.callback = lambda output, idx=i, s=step: on_task_complete(idx, s, output)

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    try:
        result = crew.kickoff()

        output = {}
        for i, step in enumerate(AGENT_STEPS):
            task_output = tasks[i].output
            output[step["key"]] = task_output.pydantic if task_output else None

        output["raw_result"] = str(result)

    except Exception as e:
        output = {step["key"]: None for step in AGENT_STEPS}
        output["raw_result"] = None
        output["error"] = str(e)

    return output
