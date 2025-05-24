from typing import List
from sqlalchemy.orm.exc import NoResultFound
from db.models.project import Project
from db.models.task import AcceptanceCriteria, Deliverable, Task
from db.session import SessionLocal
from sqlalchemy.orm import joinedload

async def save_project_to_sql(
    project_name: str, 
    deliverables: list, 
    user_id: str, 
    blob_path: str, 
    description: str,
    technologies: list,
    complexity: str,
    category: str,
    score: str):
    
    db = SessionLocal()
    try:
        project = Project(
            name=project_name,
            user_id=user_id,
            blob_path=blob_path,
            description=description,
            technologies=technologies,
            complexity=complexity,
            category=category,
            score=score
        )
        db.add(project)
        db.flush()  # Para gerar o ID do projeto

        for ent in deliverables:
            deliverable = Deliverable(name=ent["nome"], project_id=project.id)
            db.add(deliverable)
            db.flush()

            for task in ent["tarefas"]:
                task_obj = Task(
                    name=task["nome"],
                    description=task["descricao"],
                    estimated_time=task["tempo_estimado"],
                    deliverable_id=deliverable.id,
                )
                db.add(task_obj)
                db.flush()

                for criterio in task["criterios_de_aceitacao"]:
                    crit = AcceptanceCriteria(description=criterio, task_id=task_obj.id)
                    db.add(crit)

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

async def get_all_projects() -> List[Project]:
    db = SessionLocal()
    try:
        return db.query(Project).all()
    finally:
        db.close()

async def get_project_by_id(project_id: int) -> Project:
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NoResultFound("Project not found")
        return project
    finally:
        db.close()

async def update_project(project_id: int, new_name: str) -> Project:
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NoResultFound("Project not found")

        project.name = new_name
        db.commit()
        db.refresh(project)
        return project
    finally:
        db.close()

async def delete_project(project_id: int) -> bool:
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NoResultFound("Project not found")

        db.delete(project)
        db.commit()
        return True
    finally:
        db.close()

def get_projects_by_user(user_id: str):
    db = SessionLocal()
    try:
        return db.query(Project).options(
            joinedload(Project.deliverables)
            .joinedload(Deliverable.tasks)
            .joinedload(Task.acceptance_criteria)
        ).filter(Project.user_id == user_id).all()
    finally:
        db.close()