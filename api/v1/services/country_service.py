from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.v1.schemas.country_schema import CountryCreate, CountryUpdate, CountryResponse
from api.v1.repository import country_repository

def get_country_by_id(db: Session, country_id: str) -> CountryResponse:
    country = country_repository.get_country_by_id(db, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return CountryResponse.model_validate(country)

def get_all_countries(db: Session) -> List[CountryResponse]:
    countries = country_repository.get_all_countries(db)
    return [CountryResponse.model_validate(country) for country in countries]

def create_country(db: Session, country: CountryCreate) -> CountryResponse:
    db_country = country_repository.create_country(db, country)
    return CountryResponse.model_validate(db_country)

def update_country(db: Session, country_id: str, data: CountryUpdate) -> CountryResponse:
    db_country = country_repository.update_country(db, country_id, data)
    return CountryResponse.model_validate(db_country)

def delete_country(db: Session, country_id: str) -> CountryResponse:
    db_country = country_repository.delete_country(db, country_id)
    return CountryResponse.model_validate(db_country) 