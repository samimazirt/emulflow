from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.database import get_db
from app.worker import run_test

router = APIRouter()

@router.post("/", response_model=schemas.Test, status_code=201)
def create_test(test: schemas.TestCreate, db: Session = Depends(get_db)):
    """
    Create a new test and launch the execution task.
    """
    db_test = crud.create_test(db=db, test=test)
    run_test.delay(db_test.id)
    return db_test

@router.get("/", response_model=List[schemas.Test])
def read_tests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all tests.
    """
    tests = crud.get_tests(db, skip=skip, limit=limit)
    return tests

@router.get("/{test_id}", response_model=schemas.Test)
def read_test(test_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single test by its ID.
    """
    db_test = crud.get_test(db, test_id=test_id)
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return db_test 