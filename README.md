# 📦 Projeto Agentes Carlos

Este projeto é uma API desenvolvida com **FastAPI** e **SQL Server** com arquitetura organizada em múltiplas camadas para facilitar manutenção, escalabilidade e legibilidade do código.

---

## 📁 Estrutura de Pastas

```
app-agentescarlos/
│
├── api/v1/                # Módulo principal da API (versão 1)
│   ├── controllers/       # Camada de controle (rotas e endpoints)
│   ├── repository/        # Camada de repositórios (acesso ao banco)
│   ├── schemas/           # Schemas Pydantic (entrada e saída de dados)
│   ├── services/          # Regras de negócio (service layer)
│   └── routes.py          # Arquivo que registra e monta todas as rotas da API
│
├── db/                    # Configurações de banco de dados
│   ├── models/            # Modelos SQLAlchemy (tabelas do banco)
│   ├── base.py            # Declarative base
│   ├── init_db.py         # Script de criação inicial do banco
│   └── session.py         # Sessão de conexão com o banco (engine/sessionmaker)
│
├── main.py                # Entrada principal da aplicação FastAPI
├── .env                   # Variáveis de ambiente do projeto
├── .gitignore             # Arquivos a serem ignorados pelo Git
└── requirements.txt       # Dependências Python do projeto
```

---

## ⚙️ Tecnologias Usadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Azure SQL Database](https://learn.microsoft.com/pt-br/azure/azure-sql/)
- [Azure Blob Storage](https://learn.microsoft.com/pt-br/azure/storage/blobs/)
- [Uvicorn](https://www.uvicorn.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 🔌 Executando o Projeto

```bash
# Crie o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip3 install -r requirements.txt

# Crie o arquivo .env com as variáveis abaixo:
```

### 📁 .env exemplo
```
OPENAI_API_KEY=your-openai-api-key
CORS_ORIGINS=http://localhost:3000
AZURE_SQL_CONNECTION_STRING=your-azure-sql-connection-string
AZURE_STORAGE_CONNECTION_STRING=your-azure-storage-connection-string
```

```bash
# Rode o servidor de desenvolvimento
uvicorn main:app --reload
```

---

## 🔍 Organização por Responsabilidades

| Pasta               | Responsabilidade                                                                 |
|---------------------|----------------------------------------------------------------------------------|
| `controllers`       | Define os endpoints da API (camada de rota)                                      |
| `services`          | Contém a lógica de negócio da aplicação                                          |
| `repository`        | Isola a camada de persistência (comunicação com o banco)                         |
| `schemas`           | Define os modelos Pydantic usados na entrada e saída da API                      |
| `models` (em `db/`) | Contém os modelos relacionais (ORM - SQLAlchemy) que refletem as tabelas no SQL  |
| `session.py`        | Criação de conexão com o banco (engine e sessão global reutilizável)             |
| `base.py`           | Declara o `Base = declarative_base()`                                            |

---

## 🛠️ Convenções

- Nome dos arquivos em `snake_case`.
- Camada `service` nunca acessa diretamente o banco (usa `repository`).
- `main.py` registra as rotas e configura middlewares.
- Versões da API são organizadas por pasta (`api/v1/`).

---

## 📄 Licença

Este projeto é privado e distribuído exclusivamente para fins educacionais e internos.

---

