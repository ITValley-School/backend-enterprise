from fastapi import APIRouter, HTTPException
from api.v1.services.agent_project_delivery_service import generate_project_menus, generate_requirement_document, gerar_estrutura_projeto
from api.v1.schemas.project_schema import ProjectStructure, Projeto, PromptInput, RequirementDocument

router = APIRouter()

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

@router.post("/requirement-documents/generate", response_model=RequirementDocument)
async def generate_requirement(prompt_input: PromptInput):
    try:
        return await generate_requirement_document(prompt_input.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating requirement document: {str(e)}")


@router.post("/project-structure/generate", response_model=ProjectStructure)
async def generate_menus(prompt_input: PromptInput):
    try:
        return await generate_project_menus(prompt_input.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating project structure: {str(e)}")