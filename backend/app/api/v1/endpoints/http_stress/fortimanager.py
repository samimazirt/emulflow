from fastapi import APIRouter, Query, Depends, HTTPException
import asyncio
from app.core.http_stress import fortimanager
from sqlalchemy.orm import Session
import json
import requests
import datetime

from app.database import get_db
from app import models, crud
from app import schemas

router = APIRouter()

@router.post("/forti_test", status_code=201)
async def create_and_run_test(test: schemas.TestCreate, db: Session = Depends(get_db)):
    new_test = crud.create_test(db=db, test=test)

    async def loop_workflow():
        start_time = asyncio.get_event_loop().time()
        duration = 10 
        results = []

        while (asyncio.get_event_loop().time() - start_time) < duration:
            try:
                await fortimanager.run_forti_workflow(db, new_test.id)
            except Exception as e:
                print(f"Error during workflow: {e}")
            await asyncio.sleep(test.intensity)

    asyncio.create_task(loop_workflow())
    return {"status": "forti stress test started", "test_id": new_test.id}

