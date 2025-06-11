from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Appliance)
def create_appliance(appliance: schemas.ApplianceCreate, db: Session = Depends(get_db)):
    db_appliance = crud.get_appliance_by_ip(db, ip_address=str(appliance.ip_address))
    if db_appliance:
        raise HTTPException(status_code=400, detail="IP address already registered")
    return crud.create_appliance(db=db, appliance=appliance)

@router.get("/", response_model=List[schemas.Appliance])
def read_appliances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appliances = crud.get_appliances(db, skip=skip, limit=limit)
    return appliances

@router.get("/{appliance_id}", response_model=schemas.Appliance)
def read_appliance(appliance_id: int, db: Session = Depends(get_db)):
    db_appliance = crud.get_appliance(db, appliance_id=appliance_id)
    if db_appliance is None:
        raise HTTPException(status_code=404, detail="Appliance not found")
    return db_appliance

@router.delete("/{appliance_id}", response_model=schemas.Appliance)
def delete_appliance(appliance_id: int, db: Session = Depends(get_db)):
    db_appliance = crud.delete_appliance(db, appliance_id=appliance_id)
    if db_appliance is None:
        raise HTTPException(status_code=404, detail="Appliance not found")
    return db_appliance 