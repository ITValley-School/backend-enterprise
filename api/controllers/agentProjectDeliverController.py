from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.agenteProjectDeliverServices import gerar_estrutura_projeto  # ajuste o path conforme sua estrutura
from models.outputSchemas.projectModel import Projeto

router = APIRouter()

class PromptInput(BaseModel):
    prompt: str

@router.post("/projeto/gerar", response_model=Projeto)
async def gerar_projeto(prompt_input: PromptInput):
    """
    Gera a estrutura de um projeto a partir de um prompt textual.
    """
    try:
        projeto = await gerar_estrutura_projeto(prompt_input.prompt)
        return projeto
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar estrutura do projeto: {str(e)}")
