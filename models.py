from pydantic import BaseModel
from typing import Optional


# ============================================================
# TASK 1 OUTPUT: Requirement Analyst
# ============================================================

class ModulePlan(BaseModel):
    name: str
    responsibility: str
    depends_on: list[str]


class EntityPlan(BaseModel):
    name: str
    description: str
    relationships: list[str]


class EndpointOverview(BaseModel):
    method: str
    path: str
    module: str


class TechStackSuggestion(BaseModel):
    backend: str
    database: str
    auth: str


class RequirementAnalysis(BaseModel):
    project_name: str
    summary: str
    assumptions: list[str]
    modules: list[ModulePlan]
    entities: list[EntityPlan]
    endpoints_overview: list[EndpointOverview]
    suggested_tech_stack: TechStackSuggestion


# ============================================================
# TASK 2 OUTPUT: Database Architect
# ============================================================

class PropertyDefinition(BaseModel):
    type: str
    format: Optional[str] = None
    description: str


class RelationshipDefinition(BaseModel):
    type: str
    target: str
    foreign_key: str


class EntitySchema(BaseModel):
    entity: str
    properties: dict[str, PropertyDefinition]
    required_fields: list[str]
    relationships: dict[str, RelationshipDefinition]


class DatabaseSchemas(BaseModel):
    schemas: list[EntitySchema]


# ============================================================
# TASK 3 OUTPUT: API Architect
# ============================================================

class APIEndpoint(BaseModel):
    method: str
    path: str
    module: str
    description: str
    request_body: Optional[dict] = None
    query_params: Optional[dict] = None
    response_success: dict
    response_error: dict
    auth_required: bool


class APISpecification(BaseModel):
    base_url: str
    endpoints: list[APIEndpoint]


# ============================================================
# TASK 4 OUTPUT: Logic Designer
# ============================================================

class FunctionPseudocode(BaseModel):
    name: str
    description: str
    pseudocode: str


class ModulePseudocode(BaseModel):
    module_name: str
    functions: list[FunctionPseudocode]


class PseudocodeSpec(BaseModel):
    modules: list[ModulePseudocode]
