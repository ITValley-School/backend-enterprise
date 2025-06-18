from typing import List
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import String, case, cast, extract, func, literal, text
from sqlalchemy.orm.exc import NoResultFound
from db.models.project import Project
from db.models.student import Student
from db.models.student_project import StudentProject
from db.models.task import AcceptanceCriteria, Deliverable, Task
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from db.models.enterprise import Enterprise

valid_transitions = {
    "PENDING": ["OPEN", "CANCELLED"],
    "OPEN": ["IN_PROGRESS", "CANCELLED"],
    "IN_PROGRESS": ["COMPLETED", "CANCELLED"],
    "COMPLETED": [],
    "CANCELLED": []
}


async def save_project_to_sql(
    db: Session,
    project_name: str, 
    deliverables: list, 
    enterprise_id: str, 
    blob_path: str, 
    description: str,
    technologies: list,
    complexity: str,
    category: str,
    score: str,
    country: str):
    
    try:
        project = Project(
            name=project_name,
            enterprise_id=enterprise_id,
            blob_path=blob_path,
            description=description,
            technologies=technologies,
            complexity=complexity,
            category=category,
            score=score,
            country=country
        )
        
        enterprise = db.query(Enterprise).filter(Enterprise.id == project.enterprise_id).first()
        if not enterprise:
            raise HTTPException(status_code=400, detail="Enterprise not found.")
        
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

async def get_all_projects(db: Session) -> List[Project]:
    return (
        db.query(Project)
        .options(joinedload(Project.students))
        .all()
    )

async def get_project_by_id(db: Session, project_id: int) -> Project:
    try:
        project = db.query(Project).options(
            joinedload(Project.deliverables)
            .joinedload(Deliverable.tasks)
            .joinedload(Task.acceptance_criteria)).filter(Project.id == project_id).first()
        if not project:
            raise NoResultFound("Project not found")
        return project
    finally:
        db.close()

async def update_project(db: Session, project_id: int, new_name: str) -> Project:
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

async def delete_project(db: Session, project_id: int) -> bool:
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NoResultFound("Project not found")

        db.delete(project)
        db.commit()
        return True
    finally:
        db.close()

def get_projects_by_enterprise(db: Session, enterprise_id: str)-> List[Project]:
    try:
        return db.query(Project).options(
            joinedload(Project.students),
            joinedload(Project.deliverables)
            .joinedload(Deliverable.tasks)
            .joinedload(Task.acceptance_criteria)
        ).filter(Project.enterprise_id == enterprise_id).all()
    finally:
        db.close()
        
def filter_projects_by_name(db: Session, name: str):
    return db.query(Project).filter(Project.name.ilike(f"%{name}%")).all()


def can_transition(current: str, new: str) -> bool:
    return new in valid_transitions.get(current, [])

def update_project_status(db: Session, project_id: str, new_status: str):
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NoResultFound("Project not found")
        
        current_status = project.status

        if not can_transition(current_status, new_status):
            raise HTTPException(status_code=400, detail=f"Cannot transition from {current_status} to {new_status}")

        project.status = new_status
        
        if new_status == "IN_PROGRESS":
            for deliverable in project.deliverables:
                if deliverable.status in ["IN_PLANNING"]:
                    deliverable.status = "IN_DEVELOPMENT"
                    
        if new_status == "COMPLETED":
            for deliverable in project.deliverables:
                if deliverable.status in ["IN_DEVELOPMENT"]:
                    deliverable.status = "COMPLETED"
        
        db.commit()
        db.refresh(project)
        return project
    finally:
        db.close()
        
def get_visible_projects_for_students(db: Session) -> List[Project]:
  return (
        db.query(Project)
        .options(
            joinedload(Project.owner),  # para acessar project.owner.name
            joinedload(Project.deliverables).joinedload(Deliverable.tasks)  # para acessar deliverable.tasks
        )
        .filter(Project.status != "PENDING")
        .order_by(Project.created_at.desc())
        .all()
    )

def list_projects_by_enterprise(db: Session, enterprise_id: UUID) -> List[Project]:
    return (
        db.query(Project)
        .filter(Project.enterprise_id == enterprise_id)
        .order_by(Project.name)
        .all()
    )