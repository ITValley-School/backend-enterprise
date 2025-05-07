from typing import List
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
