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


def lock_adom(session_id) -> Tuple[str, bool, str]:
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
        status = None
        if "result" in result and result["result"]:
            status = result["result"][0].get("status", {})
        if status and status.get("code", 0) != 0:
            return "lock_adom", False, json.dumps(result)
        return "lock_adom", True, json.dumps(result)
    except Exception as e:
        return "lock_adom", False, f"lock_adom ERROR: {e}"


def commit_changes(session_id) -> Tuple[str, bool, str]:
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
        status = None
        if "result" in result and result["result"]:
            status = result["result"][0].get("status", {})
        if status and status.get("code", 0) != 0:
            return "commit_changes", False, json.dumps(result)
        return "commit_changes", True, json.dumps(result)
    except Exception as e:
        return "commit_changes", False, f"commit_changes ERROR: {e}"


def unlock_adom(session_id) -> Tuple[str, bool, str]:
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
        status = None
        if "result" in result and result["result"]:
            status = result["result"][0].get("status", {})
        if status and status.get("code", 0) != 0:
            return "unlock_adom", False, json.dumps(result)
        return "unlock_adom", True, json.dumps(result)
    except Exception as e:
        return "unlock_adom", False, f"unlock_adom ERROR: {e}"


def add_firewall_policy(policy_name, session_id) -> Tuple[str, bool, str]:
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
        status = None
        if "result" in result and result["result"]:
            status = result["result"][0].get("status", {})
        if status and status.get("code", 0) != 0:
            return "add_firewall_policy", False, json.dumps(result)
        return "add_firewall_policy", True, json.dumps(result)
    except Exception as e:
        return "add_firewall_policy", False, f"add_firewall_policy ERROR: {e}"


def add_firewall_address(session_id) -> Tuple[str, bool, str]:
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
        status = None
        if "result" in result and result["result"]:
            status = result["result"][0].get("status", {})
        if status and status.get("code", 0) != 0:
            return "add_firewall_address", False, json.dumps(result)
        return "add_firewall_address", True, json.dumps(result)
    except Exception as e:
        return "add_firewall_address", False, f"add_firewall_address ERROR: {e}"


def logout(session_id) -> Tuple[str, bool, str]:
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
        status = None
        if "result" in result and result["result"]:
            status = result["result"][0].get("status", {})
        if status and status.get("code", 0) != 0:
            return "logout", False, json.dumps(result)
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


async def run_forti_workflow(global_db: Session, test_id: int, session_id=None):
    local_db = SessionLocal()
    try:
        test = crud.get_test(local_db, test_id)
        test.status = models.TestStatus.RUNNING
        test.start_time = datetime.datetime.utcnow()
        local_db.commit()

        login_name, login_ok, login_detail = login()
        if not login_ok:
            raise Exception(f"Login failed: {login_detail}")

        all_results = {
            "success": [],
            "failed": [],
            "details": []
        }
        
        if login_ok:
            all_results["success"].append(login_name)
        else:
            all_results["failed"].append(login_name)
        all_results["details"].append(login_detail)

        start_time = asyncio.get_event_loop().time()
        duration = 100
        iteration = 0

        while (asyncio.get_event_loop().time() - start_time) < duration:
            iteration += 1
            print(f"Iteration {iteration} - Time elapsed: {asyncio.get_event_loop().time() - start_time:.2f}s")
            try:
                lock_name, lock_ok, lock_detail = lock_adom(session_id)
                if lock_ok:
                    all_results["success"].append(f"{lock_name}_iter_{iteration}")
                else:
                    all_results["failed"].append(f"{lock_name}_iter_{iteration}")
                all_results["details"].append(f"{lock_detail}_iter_{iteration}")

                if lock_ok:
                    addr_name, addr_ok, addr_detail = add_firewall_address(session_id)
                    if addr_ok:
                        all_results["success"].append(f"{addr_name}_iter_{iteration}")
                    else:
                        all_results["failed"].append(f"{addr_name}_iter_{iteration}")
                    all_results["details"].append(f"{addr_detail}_iter_{iteration}")

                    policy_name_str = f"TEST_{iteration}"
                    policy_name, policy_ok, policy_detail = add_firewall_policy(policy_name_str, session_id)
                    if policy_ok:
                        all_results["success"].append(f"{policy_name}_iter_{iteration}")
                    else:
                        all_results["failed"].append(f"{policy_name}_iter_{iteration}")
                    all_results["details"].append(f"{policy_detail}_iter_{iteration}")

                    # Commit changes
                    commit_name, commit_ok, commit_detail = commit_changes(session_id)
                    if commit_ok:
                        all_results["success"].append(f"{commit_name}_iter_{iteration}")
                    else:
                        all_results["failed"].append(f"{commit_name}_iter_{iteration}")
                    all_results["details"].append(f"{commit_detail}_iter_{iteration}")

                    # Unlock ADOM
                    unlock_name, unlock_ok, unlock_detail = unlock_adom(session_id)
                    if unlock_ok:
                        all_results["success"].append(f"{unlock_name}_iter_{iteration}")
                    else:
                        all_results["failed"].append(f"{unlock_name}_iter_{iteration}")
                    all_results["details"].append(f"{unlock_detail}_iter_{iteration}")

            except Exception as e:
                error_msg = f"Error in iteration {iteration}: {str(e)}"
                all_results["failed"].append(f"iteration_{iteration}_error")
                all_results["details"].append(error_msg)
                print(error_msg)
            test = crud.get_test(local_db, test_id)
            test.results = all_results
            local_db.commit()

        logout_name, logout_ok, logout_detail = logout(session_id)
        if logout_ok:
            all_results["success"].append(logout_name)
        else:
            all_results["failed"].append(logout_name)
        all_results["details"].append(logout_detail)

        test = crud.get_test(local_db, test_id)
        test.results = all_results
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
