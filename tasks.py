from crewai import Task
from models import (
    RequirementAnalysis,
    DatabaseSchemas,
    APISpecification,
    PseudocodeSpec,
)


def create_tasks(agents: dict, requirement: str):
    """Creates and returns all 4 tasks in sequential order."""

    task_analyze = Task(
        description=(
            f"Analyze the following business requirement and break it down into:\n"
            f"1. A list of cohesive, loosely-coupled modules with clear responsibilities\n"
            f"2. All data entities with their relationships\n"
            f"3. An overview of API endpoints needed\n"
            f"4. A suggested tech stack\n\n"
            f"If the requirement is vague, make reasonable assumptions and list them.\n\n"
            f"BUSINESS REQUIREMENT:\n{requirement}"
        ),
        expected_output="A structured analysis with modules, entities, endpoint overview, and tech stack",
        agent=agents["analyst"],
        output_pydantic=RequirementAnalysis,
    )

    task_schemas = Task(
        description=(
            "Based on the requirement analysis, design JSON Schema definitions for EVERY entity identified. "
            "Include:\n"
            "- All properties with appropriate types and formats (uuid, email, date-time, etc.)\n"
            "- Required fields list\n"
            "- Relationship mappings with foreign key references\n"
            "- Sensible constraints where obvious\n\n"
            "Make sure schemas are internally consistent — if Entity A references Entity B, "
            "the foreign key must exist in the schema."
        ),
        expected_output="JSON Schema definitions for all entities with relationships",
        agent=agents["db_architect"],
        output_pydantic=DatabaseSchemas,
        context=[task_analyze],
    )

    task_api = Task(
        description=(
            "Based on the requirement analysis, design a complete REST API specification. "
            "Include:\n"
            "- All CRUD endpoints for each entity, grouped by module\n"
            "- Request body or query parameters where relevant\n"
            "- Success response format (with realistic example data types)\n"
            "- At least one error response per endpoint\n"
            "- Authentication requirement per endpoint\n"
            "- Follow REST conventions: proper HTTP methods, plural resource names, nested routes where logical"
        ),
        expected_output="Complete REST API specification with all endpoints",
        agent=agents["api_architect"],
        output_pydantic=APISpecification,
        context=[task_analyze],
    )

    task_pseudocode = Task(
        description=(
            "Based on the requirement analysis and database schemas, write pseudocode for the "
            "core business logic of each module. Include:\n"
            "- 2-3 most important functions per module\n"
            "- Error handling (not just happy path)\n"
            "- References to actual entity names and fields from the schemas\n"
            "- Language-agnostic but readable pseudocode (Python-ish structure is fine)\n"
            "- Each function should have a clear description"
        ),
        expected_output="Pseudocode for core business logic organized by module",
        agent=agents["logic_designer"],
        output_pydantic=PseudocodeSpec,
        context=[task_analyze, task_schemas],
    )

    return [task_analyze, task_schemas, task_api, task_pseudocode]
