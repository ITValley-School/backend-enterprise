from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from api.v1.schemas.country_schema import CountryCreate, CountryUpdate, CountryResponse
from api.v1.services import country_service
from db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[CountryResponse])
def get_all_countries(db: Session = Depends(get_db)):
    return country_service.get_all_countries(db)

@router.get("/{country_id}", response_model=CountryResponse)
def get_country(country_id: str, db: Session = Depends(get_db)):
    return country_service.get_country_by_id(db, country_id)

@router.post("/", response_model=CountryResponse, status_code=status.HTTP_201_CREATED)
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    return country_service.create_country(db, country)

@router.put("/{country_id}", response_model=CountryResponse)
def update_country(country_id: str, country_data: CountryUpdate, db: Session = Depends(get_db)):
    return country_service.update_country(db, country_id, country_data)

@router.delete("/{country_id}", response_model=CountryResponse)
def delete_country(country_id: str, db: Session = Depends(get_db)):
    return country_service.delete_country(db, country_id) 