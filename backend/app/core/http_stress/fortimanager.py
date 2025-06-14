import json
import requests
from typing import Tuple
from sqlalchemy.orm import Session
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
import asyncio
import json
from app.database import SessionLocal

import requests
import datetime

from app.database import get_db
from app import models, crud

server_ip = "192.168.1.99"
user = "admin"
pwd = "admin"
adom_name = "root"
pkg_name = "test"

dst_address = 'all'
dst_interface = 'any'
logtraffic = 2
policy_name = 'TEST'
service = 'ALL'
src_address = 'all'
src_interface = 'any'
action = 1
nat = 0

allow_routing = 0
associated_interface = 'any'
object_name = 'NEW-ADDR'
subnet = ['1.1.1.1', '255.255.255.255']

session_id = None


def login() -> Tuple[str, bool, str]:
    global session_id
    try:
        url = f"https://{server_ip}/jsonrpc"
        payload_object = {
            "method": "exec",
            "params": [{"data": [{"passwd": pwd, "user": user}], "url": "sys/login/user"}],
            "id": 1
        }
        payload = json.dumps(payload_object)
        headers = {'Content-Type': "application/json"}
        resp = requests.post(url, data=payload, headers=headers, verify=False)
        resp.raise_for_status()
        result = resp.json()
        session_id = result.get("session")
        return "login", True, json.dumps(result)
    except Exception as e:
        return "login", False, f"login ERROR: {e}"


def lock_adom() -> Tuple[str, bool, str]:
    try:
        url = f"https://{server_ip}/jsonrpc"
        payload_object = {
            "method": "exec",
            "params": [{"url": f"/dvmdb/adom/{adom_name}/workspace/lock"}],
            "session": session_id,
            "id": 1
        }
        resp = requests.post(url, json=payload_object, verify=False)
        resp.raise_for_status()
        result = resp.json()
        return "lock_adom", True, json.dumps(result)
    except Exception as e:
        return "lock_adom", False, f"lock_adom ERROR: {e}"


def commit_changes() -> Tuple[str, bool, str]:
    try:
        url = f"https://{server_ip}/jsonrpc"
        payload_object = {
            "method": "exec",
            "params": [{"url": f"/dvmdb/adom/{adom_name}/workspace/commit"}],
            "session": session_id,
            "id": 1
        }
        resp = requests.post(url, json=payload_object, verify=False)
        resp.raise_for_status()
        result = resp.json()
        return "commit_changes", True, json.dumps(result)
    except Exception as e:
        return "commit_changes", False, f"commit_changes ERROR: {e}"


def unlock_adom() -> Tuple[str, bool, str]:
    try:
        url = f"https://{server_ip}/jsonrpc"
        payload_object = {
            "method": "exec",
            "params": [{"url": f"/dvmdb/adom/{adom_name}/workspace/unlock"}],
            "session": session_id,
            "id": 1
        }
        resp = requests.post(url, json=payload_object, verify=False)
        resp.raise_for_status()
        result = resp.json()
        return "unlock_adom", True, json.dumps(result)
    except Exception as e:
        return "unlock_adom", False, f"unlock_adom ERROR: {e}"


def add_firewall_policy() -> Tuple[str, bool, str]:
    try:
        url = f"https://{server_ip}/jsonrpc"
        payload_object = {
            "method": "add",
            "params": [{
                "data": [{
                    "dstaddr": dst_address,
                    "dstintf": dst_interface,
                    "logtraffic": logtraffic,
                    "name": policy_name,
                    "service": service,
                    "srcaddr": src_address,
                    "srcintf": src_interface,
                    "action": action,
                    "nat": nat,
                    "schedule": "always"
                }],
                "url": f"/pm/config/adom/{adom_name}/pkg/{pkg_name}/firewall/policy"
            }],
            "session": session_id,
            "id": 1
        }
        resp = requests.post(url, json=payload_object, verify=False)
        resp.raise_for_status()
        result = resp.json()
        return "add_firewall_policy", True, json.dumps(result)
    except Exception as e:
        return "add_firewall_policy", False, f"add_firewall_policy ERROR: {e}"


def add_firewall_address() -> Tuple[str, bool, str]:
    try:
        url = f"https://{server_ip}/jsonrpc"
        payload_object = {
            "method": "add",
            "params": [{
                "data": [{
                    "allow-routing": allow_routing,
                    "associated-interface": associated_interface,
                    "name": object_name,
                    "subnet": subnet
                }],
                "url": f"/pm/config/adom/{adom_name}/obj/firewall/address"
            }],
            "session": session_id,
            "id": 1
        }
        resp = requests.post(url, json=payload_object, verify=False)
        resp.raise_for_status()
        result = resp.json()
        return "add_firewall_address", True, json.dumps(result)
    except Exception as e:
        return "add_firewall_address", False, f"add_firewall_address ERROR: {e}"


def logout() -> Tuple[str, bool, str]:
    try:
        url = f"https://{server_ip}/jsonrpc"
        payload_object = {
            "method": "exec",
            "params": [{"data": [{"unlocked": True}], "url": "sys/logout"}],
            "session": session_id,
            "id": 1
        }
        resp = requests.post(url, json=payload_object, verify=False)
        resp.raise_for_status()
        result = resp.json()
        return "logout", True, json.dumps(result)
    except Exception as e:
        return "logout", False, f"logout ERROR: {e}"


def run_workflow():
    steps = [
        login,
        lock_adom,
        add_firewall_address,
        add_firewall_policy,
        commit_changes,
        unlock_adom,
        logout,
    ]

    results = {
        "success": [],
        "failed": [],
        "details": []
    }

    for step in steps:
        name, ok, detail = step()
        if ok:
            results["success"].append(name)
        else:
            results["failed"].append(name)
        results["details"].append(detail)

    return results 


async def run_forti_workflow(global_db: Session, test_id: int):
    local_db = SessionLocal()
    try:
        test = crud.get_test(local_db, test_id)
        test.status = models.TestStatus.RUNNING
        test.start_time = datetime.datetime.utcnow()
        local_db.commit()

        results = await asyncio.to_thread(run_workflow)

        test = crud.get_test(local_db, test_id)
        test.results = results
        test.status = models.TestStatus.COMPLETED
        test.end_time = datetime.datetime.utcnow()
        local_db.commit()

    except Exception as e:
        test = crud.get_test(local_db, test_id)
        test.status = models.TestStatus.FAILED
        test.end_time = datetime.datetime.utcnow()
        test.results = {"error": str(e)}
        local_db.commit()

    finally:
        local_db.close()
