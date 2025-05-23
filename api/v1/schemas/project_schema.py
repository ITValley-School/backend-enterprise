from typing import List, Optional
from pydantic import BaseModel

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
    user_id: str
    project_name: str
    requirements_html: str
    menus: list
    deliverables: list

class UpdateProjectInput(BaseModel):
    name: str

class PromptInput(BaseModel):
    prompt: str
