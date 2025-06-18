from fastapi import APIRouter, Query, Depends, HTTPException, Response
import asyncio
from app.core.http_stress import fortimanager
from sqlalchemy.orm import Session
import json
import requests
import datetime
import threading
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

from app.database import get_db
from app import models, crud
from app import schemas

router = APIRouter()

@router.post("/forti_test", status_code=201)
async def create_and_run_test(test: schemas.TestCreate, db: Session = Depends(get_db)):
    forti_session = crud.get_forti_session(db)
    print(forti_session)
    session_id = None
    if forti_session:
        session_id = forti_session.session_id
    else:
        _, ok, detail = fortimanager.login()
        print(detail)
        if not ok:
            raise HTTPException(status_code=500, detail="Login FortiManager failed")
        session_id = fortimanager.session_id  
        crud.create_or_update_forti_session(db, session_id)

    def background_task():
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(fortimanager.run_forti_workflow(db, new_test.id, session_id=session_id))
        loop.close()

    new_test = crud.create_test(db=db, test=test)
    threading.Thread(target=background_task, daemon=True).start()
    return {"status": "forti stress test started", "test_id": new_test.id}

@router.get("/forti_test/{test_id}/report", response_class=Response)
def download_test_report(test_id: int, db: Session = Depends(get_db)):
    test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    results = test.results or {}

    total = len(results.get("success", [])) + len(results.get("failed", []))
    nb_success = len(results.get("success", []))
    nb_failed = len(results.get("failed", []))
    details = results.get("details", [])
    duration = None
    if test.start_time and test.end_time:
        duration = (test.end_time - test.start_time).total_seconds()
    else:
        duration = "N/A"

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 50, f"Rapport de Test FortiManager #{test.id}")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 90, f"Date de début : {test.start_time}")
    p.drawString(50, height - 110, f"Date de fin   : {test.end_time}")
    p.drawString(50, height - 130, f"Durée         : {duration} secondes")
    p.drawString(50, height - 150, f"Intensité     : {test.intensity}")
    p.drawString(50, height - 170, f"Status final  : {test.status}")

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 210, "KPI")
    p.setFont("Helvetica", 12)
    p.drawString(70, height - 230, f"Total opérations : {total}")
    p.drawString(70, height - 250, f"Succès           : {nb_success}")
    p.drawString(70, height - 270, f"Échecs           : {nb_failed}")
    if total > 0:
        p.drawString(70, height - 290, f"Taux de succès   : {round(nb_success/total*100, 2)} %")
    else:
        p.drawString(70, height - 290, f"Taux de succès   : N/A")

    
    p.showPage()
    p.save()
    buffer.seek(0)

    return Response(
        content=buffer.read(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=rapport_test_{test.id}.pdf"}
    )



