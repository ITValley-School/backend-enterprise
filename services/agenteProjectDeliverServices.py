from agents import Agent, Runner, set_default_openai_key, ModelSettings, function_tool
import os
from dotenv import load_dotenv
import logging
from models.outputSchemas.projectModel import MenuItem, ProjectStructure, Projeto, RequirementDocument, SubMenuItem
from models.agents.agentModel import AgentProjectCreateMenu, AgentProjectDesigner, AgentRequirementAnalyst
import markdown
import re

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
    if not requisitos or not isinstance(requisitos, str) or len(requisitos.strip()) < 20:
        raise ValueError("O conteúdo do prompt é muito curto ou inválido.")
    
    def strip_html_tags(text: str) -> str:
        return re.sub(r'<[^>]+>', '', text)
    
    clean_prompt = strip_html_tags(requisitos.strip())
    
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
        result = await Runner.run(agente, f"Com base nos seguintes requisitos, estruture o projeto:\n\n{clean_prompt}")
        
        # Retorna a saída final validada como instância do modelo Projeto
        projeto_validado = result.final_output_as(Projeto, raise_if_incorrect_type=True)
        logging.info("Projeto estruturado e validado com sucesso.")
        return projeto_validado
            
    except Exception as e:
        logging.error(f"Erro ao processar requisitos: {e}")
        raise

async def generate_requirement_document(prompt: str) -> RequirementDocument:
    """
    Gera o documento de requisitos do sistema a partir da descrição do cliente.
    Retorna o conteúdo renderizado como HTML.
    """
    if not prompt or not isinstance(prompt, str) or len(prompt.strip()) < 20:
        raise ValueError("O conteúdo do prompt é muito curto ou inválido.")
    
    def strip_html_tags(text: str) -> str:
        return re.sub(r'<[^>]+>', '', text)
    
    clean_prompt = strip_html_tags(prompt.strip())
    
    agente_def = AgentRequirementAnalyst()

    agente = Agent(
        name=agente_def.name,
        instructions=agente_def.instructions + "\n\nRetorne a estrutura como um documento bem formatado.",
        model=agente_def.model,
        output_type=str
    )

    try:
        logging.info("Gerando documento de requisitos...")
        result = await Runner.run(agente, clean_prompt)
        markdown_content = result.final_output_as(str, raise_if_incorrect_type=True)
        full_markdown = f"\n{markdown_content}"
        html_content = markdown.markdown(full_markdown, extensions=["tables", "fenced_code"])
        return RequirementDocument(title="", content=html_content)

    except Exception as e:
        logging.error(f"Erro ao gerar documento de requisitos: {e}")
        raise

async def generate_project_menus(prompt: str) -> ProjectStructure:
    """
    Gera a estrutura de menus da aplicação a partir da descrição fornecida.
    Retorna JSON com menus e submenus para uso no front-end.
    """
    if not prompt or not isinstance(prompt, str) or len(prompt.strip()) < 20:
        raise ValueError("O conteúdo do prompt é muito curto ou inválido.")
    
    def strip_html_tags(text: str) -> str:
        return re.sub(r'<[^>]+>', '', text)
    
    clean_prompt = strip_html_tags(prompt.strip())
    
    agente_def = AgentProjectCreateMenu()

    agente = Agent(
        name=agente_def.name,
        instructions=agente_def.instructions + "\n\nRetorne apenas a estrutura dos menus e telas.",
        model=agente_def.model,
        output_type=str
    )

    try:
        logging.info("Gerando estrutura de menus...")
        result = await Runner.run(agente, clean_prompt)
        raw_response = result.final_output_as(str, raise_if_incorrect_type=True)

        main_menu = []
        current_menu = None
        lines = raw_response.splitlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("Menus") or line.startswith("1.") or line.startswith("2."):
                continue

            if line.startswith("- "):  # menu principal
                if ":" in line:
                    menu_name, submenu_line = line[2:].split(":", 1)
                    submenus = [
                        SubMenuItem(name=sub.strip()) for sub in submenu_line.split(",") if sub.strip()
                    ]
                    main_menu.append(MenuItem(name=menu_name.strip(), submenus=submenus))
                else:
                    current_menu = MenuItem(name=line[2:].strip(), submenus=[])
                    main_menu.append(current_menu)

            elif current_menu and line.startswith("  - "):  # submenu
                current_menu.submenus.append(SubMenuItem(name=line[4:].strip()))

        return ProjectStructure(main_menu=main_menu)

    except Exception as e:
        logging.error(f"Erro ao gerar estrutura de menus: {e}")
        raise