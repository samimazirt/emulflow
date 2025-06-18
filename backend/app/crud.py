from sqlalchemy.orm import Session
from . import models, schemas
import datetime

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

def get_test(db: Session, test_id: int):
    return db.query(models.Test).filter(models.Test.id == test_id).first()

def get_tests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Test).order_by(models.Test.start_time.desc()).offset(skip).limit(limit).all()

def create_test(db: Session, test: schemas.TestCreate) -> models.Test:
    db_test = models.Test(intensity=test.intensity)
    db.add(db_test)
    
    appliances = db.query(models.Appliance).filter(models.Appliance.id.in_(test.appliance_ids)).all()
    db_test.appliances.extend(appliances)
    
    db.commit()
    db.refresh(db_test)
    return db_test

def update_test(db: Session, test_id: int, test_data: schemas.TestUpdate):
    db_test = get_test(db, test_id)
    if db_test:
        update_data = test_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_test, key, value)
        
        if 'status' in update_data and update_data['status'] in [models.TestStatus.COMPLETED, models.TestStatus.FAILED, models.TestStatus.STOPPED]:
            db_test.end_time = datetime.datetime.utcnow()

        db.add(db_test)
        db.commit()
        db.refresh(db_test)
    return db_test 


def get_forti_session(db: Session):
    return db.query(models.FortiSession).order_by(models.FortiSession.created_at.desc()).first()

def create_or_update_forti_session(db: Session, session_id: str):
    session = get_forti_session(db)
    if session:
        session.session_id = session_id
        session.created_at = datetime.utcnow()
    else:
        session = models.FortiSession(session_id=session_id)
        db.add(session)
    db.commit()
    return session

def delete_forti_session(db: Session):
    session = get_forti_session(db)
    if session:
        db.delete(session)
        db.commit()