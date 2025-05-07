from agents import Agent, Runner, set_default_openai_key, ModelSettings, function_tool
import asyncio
import os
import json
from dotenv import load_dotenv
import logging
from models.outputSchemas.projectModel import Projeto
from models.agents.agentModel import AgentProjectDesigner

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Carrega variáveis de ambiente
load_dotenv()

# Configura a chave da API OpenAI
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))

async def gerar_estrutura_projeto(requisitos: str) -> Projeto:
    """
    Recebe os requisitos do projeto como string e retorna a estrutura
    do projeto no formato validado conforme o schema Pydantic 'Projeto'.
    
    Args:
        requisitos: String contendo os requisitos do projeto
        
    Returns:
        Instância de Projeto validada pelo Pydantic
    """
    # Instancia o agente de design de projetos
    agente_def = AgentProjectDesigner()
    
    # Cria o agente com o schema de saída corretamente definido
    agente = Agent(
        name=agente_def.name,
        instructions=agente_def.instructions + "\n\nRetorne a estrutura do projeto exatamente no formato especificado.",
        model=agente_def.model,
        output_type=Projeto  # Passa a CLASSE, não o .schema()
    )
    
    try:
        # Executa o agente com os requisitos fornecidos
        logging.info("Processando requisitos do projeto...")
        result = await Runner.run(agente, f"Com base nos seguintes requisitos, estruture o projeto:\n\n{requisitos}")
        
        # Retorna a saída final validada como instância do modelo Projeto
        projeto_validado = result.final_output_as(Projeto, raise_if_incorrect_type=True)
        logging.info("Projeto estruturado e validado com sucesso.")
        return projeto_validado
            
    except Exception as e:
        logging.error(f"Erro ao processar requisitos: {e}")
        raise
