from sqlalchemy.orm import Session
from . import models, schemas

def get_appliance(db: Session, appliance_id: int):
    return db.query(models.Appliance).filter(models.Appliance.id == appliance_id).first()

def get_appliance_by_ip(db: Session, ip_address: str):
    return db.query(models.Appliance).filter(models.Appliance.ip_address == ip_address).first()

def get_appliances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Appliance).offset(skip).limit(limit).all()

def create_appliance(db: Session, appliance: schemas.ApplianceCreate):
    # In a real app, hash the password
    db_appliance = models.Appliance(
        name=appliance.name,
        ip_address=str(appliance.ip_address),
        appliance_type=appliance.appliance_type,
        appliance_family=appliance.appliance_family,
        username=appliance.username,
        password=appliance.password # Hashing should be done here
    )
    db.add(db_appliance)
    db.commit()
    db.refresh(db_appliance)
    return db_appliance

def delete_appliance(db: Session, appliance_id: int):
    db_appliance = db.query(models.Appliance).filter(models.Appliance.id == appliance_id).first()
    if db_appliance:
        db.delete(db_appliance)
        db.commit()
        return db_appliance
    return None 