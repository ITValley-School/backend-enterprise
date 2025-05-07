import asyncio
import os
import logging
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_key

# Usando importações relativas
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.agents.agentModel import AgentAssistant, AgentCatalog, AgentEmail
from models.functions.toolsModel import AgentTools

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carrega variáveis de ambiente
load_dotenv()

# Configura a chave da API OpenAI
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))

async def run_agent(agent, prompt):
    """Função auxiliar para executar o agente assincronamente"""
    result = await Runner.run(agent, prompt)
    return result.final_output

async def interactive_chat(agent_instance):
    """Função para interagir continuamente com o agente"""
    print(f"\n=== Assistente {agent_instance.name} ===")
    print("Digite 'exit' para sair da conversa\n")
    
    try:
        # Loop de conversa
        while True:
            # Obtém a entrada do usuário
            user_input = input("\nVocê: ")
            
            # Verifica se o usuário quer sair
            if user_input.lower().strip() == "exit":
                print("\nEncerrando conversa. Até logo!")
                break
                
            # Registra a entrada do usuário no log
            logging.info(f"Entrada do usuário: {user_input}")
            
            # Processa a entrada com o agente
            print("\nProcessando...")
            response = await run_agent(agent_instance, user_input)
            
            # Exibe a resposta do agente
            print(f"\nAssistente: {response}")
            
    except Exception as e:
        logging.error(f"Erro durante a conversa: {e}")
        print(f"\nOcorreu um erro: {e}")

def main():
    """Função principal que configura e executa o aplicativo"""
    
    toolAgents = AgentTools()
    # Instancia as classes de ferramentas
    catalog_tools = [toolAgents.listar_capacidades, toolAgents.listar_contatos]


    # Instancia as classes dos agentes
    agent_catalog_def = AgentCatalog()

    
    # Cria o agente de catálogo de capacidades
    agente_catalogo = Agent(
        name=agent_catalog_def.name,
        instructions=agent_catalog_def.instructions,
        
        tools=[
            toolAgents.listar_capacidades,
            toolAgents.buscar_capacidade,
            toolAgents.buscar_email
        ]
    )
    

    # Executa o chat interativo com o agente de emails
    # Você pode mudar para agente_catalogo se preferir interagir com esse agente
    asyncio.run(interactive_chat(agente_catalogo))

if __name__ == "__main__":
    main()