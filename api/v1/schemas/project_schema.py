from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from api.v1.schemas.student_schema import StudentResponse



class Tarefa(BaseModel):
    nome: str
    descricao: str
    tempo_estimado: float  # horas
    criterios_de_aceitacao: List[str]

class Entregavel(BaseModel):
    nome: str
    tarefas: List[Tarefa]

class Projeto(BaseModel):
    projeto: str
    entregaveis: List[Entregavel]
    descricao: str
    tecnologias: List[str]
    complexidade: str
    categoria: str
    pontuacao: str
    status: str
    progress: str

class RequirementDocument(BaseModel):
    title: str
    content: str

class SubMenuItem(BaseModel):
    name: str

class MenuItem(BaseModel):
    name: str
    submenus: List[SubMenuItem] = []

class ProjectStructure(BaseModel):
    main_menu: List[MenuItem]

class CompleteProjectInput(BaseModel):
    enterprise_id: str
    project_name: str
    requirements_html: str
    menus: list
    deliverables: list
    description: str
    technologies: List[str]
    complexity: str
    category: str
    score: str
    country: str

class UpdateProjectInput(BaseModel):
    name: str

class PromptInput(BaseModel):
    prompt: str

class AcceptanceCriteriaSchema(BaseModel):
    description: str

    model_config = {
        "from_attributes": True
    }

class TaskSchema(BaseModel):
    name: str
    description: str
    status: str
    estimated_time: Optional[float]
    acceptance_criteria: List[AcceptanceCriteriaSchema]

    model_config = {
        "from_attributes": True
    }

class DeliverableSchema(BaseModel):
    name: str
    tasks: List[TaskSchema]
    status: str

    model_config = {
        "from_attributes": True
    }

class ProjectResponse(BaseModel):
    id: str
    name: str
    enterprise_id: str
    created_at: datetime
    deliverables: List[DeliverableSchema]
    description: str
    technologies: List[str]
    complexity: str
    category: str
    score: str
    country: str
    status: str
    progress: int
    team: List[StudentResponse]

    model_config = {
        "from_attributes": True
    }
    
    
class ProjectList(BaseModel):
    id: str
    name: str
    created_at: datetime
    description: str
    technologies: List[str]
    complexity: str
    category: str
    score: str
    country: str
    status: str
    progress: int
    team: List[StudentResponse]

    model_config = {
        "from_attributes": True
    }
class UpdateStatusInput(BaseModel):
    new_status: str
