from agents import Agent, Runner, set_default_openai_key, ModelSettings, function_tool
import asyncio
import os
from dotenv import load_dotenv
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

set_default_openai_key(os.environ.get("OPENAI_API_KEY"))


# Passos (Parte 1):
# 1. Criar os outputsStructs para cada função
# 2. As Tools (funções) devem ser criadas com o decorator @function_tool
# 3. Criar os agentes com as Tools (funções)  que eles podem executar e se o caso com os OutputsStructs

#Passos (Parte 2):
# 4. Criar o runAgent para executar o agente

def get_agent_capabilities():
#region
    """
    Function to return the catalog of agent capabilities
    """
    capabilities = {
        "email": "Posso enviar e-mails via API quando solicitado",
        "contacts": "Posso acessar um catálogo de endereços com e-mails salvos. Basta informar o nome da pessoa",
        "conversation": "Posso conversar amigavelmente e ajudar com suas dúvidas"
    }
    return capabilities
#endregion

@function_tool
def listar_capacidades():
    """Lista todas as capacidades que o agente possui"""
    capabilities = get_agent_capabilities()
    return {
        "capacidades": "\n".join([f"{i+1}. {val}" for i, val in enumerate(capabilities.values())])
    }

@function_tool
def buscar_capacidade(tipo: str):
    """
    Busca informações sobre uma capacidade específica
    
    Args:
        tipo: Tipo de capacidade (email, contacts, conversation)
    """
    capabilities = get_agent_capabilities()
    if tipo.lower() in capabilities:
        return {"detalhes": capabilities[tipo.lower()]}
    else:
        return {"detalhes": f"Capacidade '{tipo}' não encontrada. Capacidades disponíveis: {', '.join(capabilities.keys())}"}

# Cria o agente de catálogo
agente_catalogo = Agent(
    name="Catálogo de Capacidades",
    instructions="""
    Você é um agente que tem acesso a todo o catálogo de ações e funcionalidades disponíveis.
    Suas funções são:
    1. Informar sobre a capacidade de enviar e-mail via API, quando solicitado pelo usuário
    2. Informar sobre a capacidade de acessar um catálogo de endereços com emails salvos
    3. Informar sobre a capacidade de conversar amigavelmente com o usuário
    
    Quando perguntado sobre o que você pode fazer, liste suas capacidades.
    Quando perguntado sobre uma capacidade específica, forneça mais detalhes.
    """,
    model="gpt-3.5-turbo",
    tools=[listar_capacidades, buscar_capacidade]
)


def get_email_catalog():
    """
    Returns a catalog of contacts with their email addresses
    """
    catalog = {
        "carlos viana": "carlosaraujoviana@gmail.com",
        "carlos santana": "carlossantana@gmail.com",
        "julia robert": "julia@robert.com"
    }
    return catalog

@function_tool
def buscar_email(nome: str):
    """
    Busca o email de um contato pelo nome
    
    Args:
        nome: Nome do contato a ser buscado
    """
    catalog = get_email_catalog()
    nome_lower = nome.lower()
    
    # Busca exata
    if nome_lower in catalog:
        return {"email": catalog[nome_lower], "nome": nome}
    
    # Busca parcial
    possiveis_contatos = []
    for contato in catalog.keys():
        if nome_lower in contato:
            nome_formatado = ' '.join(word.capitalize() for word in contato.split())
            possiveis_contatos.append(f"{nome_formatado}: {catalog[contato]}")
    
    if possiveis_contatos:
        return {
            "mensagem": f"Encontrei {len(possiveis_contatos)} contato(s) que correspondem a '{nome}':",
            "contatos": "\n".join(possiveis_contatos)
        }
    else:
        return {"mensagem": f"Não encontrei nenhum contato com o nome '{nome}' no catálogo."}

@function_tool
def listar_contatos():
    """Lista todos os contatos disponíveis no catálogo"""
    catalog = get_email_catalog()
    contatos_formatados = []
    
    for nome, email in catalog.items():
        nome_formatado = ' '.join(word.capitalize() for word in nome.split())
        contatos_formatados.append(f"{nome_formatado}: {email}")
    
    return {
        "contatos": "\n".join(contatos_formatados)
    }



# Cria o agente de catálogo de emails
agente_catalogo_emails = Agent(
    name="Catálogo de Emails",
    instructions="""
    Você é um agente especializado em gerenciar um catálogo de emails.
    
    Suas funções são:
    1. Listar todos os contatos disponíveis no catálogo quando solicitado
    2. Buscar o email de uma pessoa específica quando o usuário informar o nome
    
    Quando o usuário perguntar sobre contatos disponíveis, liste todos os contatos.
    Quando o usuário buscar o email de alguém, procure pelo nome no catálogo e retorne o email correspondente.
    Se o nome exato não for encontrado, busque por correspondências parciais.
    Se nenhum contato for encontrado, informe ao usuário que o contato não existe no catálogo.
    """,

    tools=[listar_contatos, buscar_email, buscar_capacidade]
)

async def run_agent(agent, prompt):
    """Função auxiliar para executar o agente assincronamente"""
    result = await Runner.run(agent, prompt)
    return result.final_output

async def interactive_chat():
    """Função para interagir continuamente com o agente"""
    print("\n=== Assistente de Catálogo de Emails ===")
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
            response = await run_agent(agente_catalogo_emails, user_input)
            
            # Exibe a resposta do agente
            print(f"\nAssistente: {response}")
            
    except Exception as e:
        logging.error(f"Erro durante a conversa: {e}")
        print(f"\nOcorreu um erro: {e}")

if __name__ == "__main__":
    # Executa o chat interativoqu
    asyncio.run(interactive_chat())