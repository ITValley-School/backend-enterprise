from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session
from typing import List, Optional

from api.v1.schemas.country_schema import CountryCreate, CountryUpdate
from db.models.country import Country

def get_country_by_id(db: Session, country_id: str) -> Optional[Country]:
    return db.query(Country).filter(Country.id == country_id, Country.is_active == True).first()

def get_country_by_name(db: Session, name: str) -> Optional[Country]:
    return db.query(Country).filter(Country.name == name, Country.is_active == True).first()

def get_country_by_code(db: Session, code: str) -> Optional[Country]:
    return db.query(Country).filter(Country.code == code, Country.is_active == True).first()

def get_all_countries(db: Session) -> List[Country]:
    return db.query(Country).filter(Country.is_active == True).all()

def create_country(db: Session, country: CountryCreate) -> Country:
    existing_country = get_country_by_name(db, country.name)
    if existing_country:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Country with this name already exists",
        )
    
    if country.code:
        existing_code = get_country_by_code(db, country.code)
        if existing_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Country with this code already exists",
            )
    
    db_country = Country(
        name=country.name,
        flag_image=country.flag_image,
        code=country.code,
    )
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def update_country(db: Session, country_id: str, data: CountryUpdate) -> Country:
    country = get_country_by_id(db, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    if data.name:
        existing_name = db.query(Country).filter(
            and_(Country.name == data.name, Country.id != country_id, Country.is_active == True)
        ).first()
        if existing_name:
            raise HTTPException(status_code=400, detail="Country name is already in use")

    if data.code:
        existing_code = db.query(Country).filter(
            and_(Country.code == data.code, Country.id != country_id, Country.is_active == True)
        ).first()
        if existing_code:
            raise HTTPException(status_code=400, detail="Country code is already in use")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(country, field, value)
        
    country.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(country)
    return country

def delete_country(db: Session, country_id: str) -> Country:
    country = get_country_by_id(db, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found or already inactive")
    
    country.is_active = False
    country.deleted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(country)
    return country 