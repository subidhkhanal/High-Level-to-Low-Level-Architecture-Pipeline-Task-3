# Architecture Pipeline — Multi-Agent Technical Spec Generator

A Streamlit-based tool that converts high-level business requirements into detailed low-level technical specifications using a **CrewAI multi-agent system** with 4 specialized AI agents.

## Architecture

```
[User Input: business requirement text]
    → CrewAI Crew kicks off (Process.sequential)
        → Task 1: Requirement Analyst   → structured plan (modules, entities, relationships)
        → Task 2: Database Architect     → JSON Schema definitions (receives Task 1 as context)
        → Task 3: API Architect          → REST API specification (receives Task 1 as context)
        → Task 4: Logic Designer         → Pseudocode (receives Task 1 + Task 2 as context)
    → Merge all task outputs
    → Render in Streamlit
```

## Agents

| Agent | Role | What It Does |
|-------|------|-------------|
| **Requirement Analyst** | Senior Business Analyst | Decomposes requirements into modules, entities, endpoints, and tech stack |
| **Database Architect** | Senior Database Engineer | Designs normalized schemas with relationships and constraints |
| **API Architect** | Senior Backend Engineer | Creates RESTful API specs with request/response formats |
| **Logic Designer** | Senior Software Engineer | Writes pseudocode for core business logic per module |

## How CrewAI Orchestration Works

- Tasks run **sequentially** via `Process.sequential`
- Each task produces **structured output** using Pydantic models
- **Context passing**: Tasks 2 & 3 receive Task 1's output; Task 4 receives Tasks 1 & 2
- This enables agents to build on each other's work — e.g., pseudocode references actual entity field names from the database schemas

## Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd architecture-pipeline
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your Groq API key
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Click one of the 3 example buttons or type your own business requirement
2. Click **"Analyze & Generate"**
3. Wait for the 4 agents to complete (~30-60 seconds)
4. Browse the results:
   - **Requirement Analysis** — modules, entities, tech stack
   - **Database Schemas** tab — entity properties, relationships
   - **API Specification** tab — endpoints grouped by module
   - **Pseudocode** tab — business logic per module

## Example Requirements

- **E-Commerce Platform** — marketplace with sellers, buyers, cart, payments, analytics
- **Hospital Management System** — appointments, schedules, billing, pharmacy
- **Learning Management System** — courses, quizzes, assignments, certificates

## Tech Stack

- **CrewAI** — Multi-agent orchestration framework
- **Groq (LLaMA 3.3 70B)** — LLM backend via litellm
- **Pydantic** — Structured output validation
- **Streamlit** — Web UI
- **python-dotenv** — Environment variable management
