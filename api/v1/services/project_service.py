import os
import json
import datetime
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob.aio import BlobServiceClient
from api.v1.repository.project_repository import (
    get_projects_by_user,
    save_project_to_sql,
    get_all_projects,
    get_project_by_id,
    update_project,
    delete_project
)


async def publish_project_service(data):
    connection_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    async with BlobServiceClient.from_connection_string(connection_str) as blob_service_client:
        container_client = blob_service_client.get_container_client("projects")

        # Attempt to create the container if it doesn't exist
        try:
            await container_client.create_container()
        except ResourceExistsError:
            pass  # Container already exists

        # Unique path for project assets
        timestamp = datetime.datetime.utcnow().isoformat().replace(":", "-")
        path_prefix = f"{data.user_id}/{data.project_name}_{timestamp}"

        # Upload files to Azure Blob Storage
        await container_client.upload_blob(
            name=f"{path_prefix}/requirements.html",
            data=data.requirements_html,
            overwrite=True
        )
        await container_client.upload_blob(
            name=f"{path_prefix}/menus.json",
            data=json.dumps(data.menus),
            overwrite=True
        )
        await container_client.upload_blob(
            name=f"{path_prefix}/deliverables.json",
            data=json.dumps(data.deliverables),
            overwrite=True
        )

    # Save project metadata and structure to SQL database
    await save_project_to_sql(
        project_name=data.project_name,
        deliverables=data.deliverables,
        user_id=data.user_id,
        blob_path=path_prefix,
        description=data.description,
        technologies=data.technologies,
        complexity=data.complexity,
        category=data.category,
        score=data.score,
        country=data.country
    )

    return path_prefix

# Retorna todos os projetos
async def list_projects_service():
    return await get_all_projects()

# Retorna um projeto por ID
async def get_project_service(project_id: int):
    return await get_project_by_id(project_id)

# Atualiza um projeto
async def update_project_service(project_id: int, update_data: dict):
    return await update_project(project_id, update_data)

# Deleta um projeto
async def delete_project_service(project_id: int):
    return await delete_project(project_id)

async def list_user_projects(user_id: str):
    return get_projects_by_user(user_id)