from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import requests
import os
import urllib3

from app.database import get_db
from app import crud

router = APIRouter()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FORTI_URL = os.getenv("FORTI_URL", "https://192.168.1.99/jsonrpc")
FORTI_USER = os.getenv("FORTI_USER", "admin")
FORTI_PASS = os.getenv("FORTI_PASS", "admin")

session = requests.Session()
session.verify = False
session.headers.update({"Content-Type": "application/json"})

def login_and_store_session(db: Session):
    payload = {
        "method": "exec",
        "params": [{
            "url": "sys/login/user",
            "data": {
                "user": FORTI_USER,
                "passwd": FORTI_PASS
            }
        }],
        "id": 1
    }
    response = session.post(FORTI_URL, json=payload)
    response_json = response.json()
    if "session" not in response_json:
        raise Exception(f"Login failed: {response_json}")
    session_id = response_json.get("session")
    crud.create_or_update_forti_session(db, session_id)
    return session_id

@router.get("/fortimanager/stats")
def get_fortimanager_stats(db: Session = Depends(get_db)):
    def do_stats_query(session_id):
        payload = {
            "id": 3,
            "method": "get",
            "params": [
                {"url": "/cli/global/system/performance"}
            ],
            "session": session_id,
            "verbose": 1
        }
        r = session.post(FORTI_URL, json=payload)
        r.raise_for_status()
        return r.json()

    try:
        forti_session = crud.get_forti_session(db)
        if forti_session:
            session_id = forti_session.session_id
        else:
            session_id = login_and_store_session(db)

        resp_json = do_stats_query(session_id)

        session_invalid = False
        if "error" in resp_json and resp_json["error"].get("code") == -11:
            session_invalid = True
        elif "result" in resp_json and resp_json["result"]:
            status = resp_json["result"][0].get("status", {})
            if status.get("code") == -11:
                session_invalid = True

        if session_invalid:
            crud.delete_forti_session(db)
            session_id = login_and_store_session(db)
            resp_json = do_stats_query(session_id)

        if "result" not in resp_json or not resp_json["result"]:
            raise Exception("No result in response")
        
        data = resp_json["result"][0].get("data", {})

        cpu_info = data.get("CPU", {})
        memory_info = data.get("Memory", {})
        flash_disk_info = data.get("Flash Disk", {})
        hard_disk_info = data.get("Hard Disk", {})

        return {
            "cpu": cpu_info,
            "memory": memory_info,
            "flash_disk": flash_disk_info,
            "hard_disk": hard_disk_info,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
