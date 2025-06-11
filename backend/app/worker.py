import os
import time
import requests
from celery import Celery
from dotenv import load_dotenv

from app.database import SessionLocal
from app import crud, schemas, models


load_dotenv()

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

@celery.task(name="run_test")
def run_test(test_id: int):
    """
    Celery task to run a load test.
    """
    db = SessionLocal()
    try:
        test = crud.get_test(db, test_id)
        if not test:
            # Maybe log this?
            return

        # 1. Set status to RUNNING
        crud.update_test(db, test_id, schemas.TestUpdate(status=models.TestStatus.RUNNING))

        # 2. Simulate the test
        duration = 30  # seconds
        start_time = time.time()
        results = {"success": 0, "failed": 0, "details": []}
        
        while time.time() - start_time < duration:
            for appliance in test.appliances:
                try:
                    # Perform a real, lightweight HTTP HEAD request to check reachability.
                    # A 2-second timeout prevents the worker from hanging on an unresponsive IP.
                    response = requests.head(f"http://{appliance.ip_address}", timeout=2)
                    
                    if response.ok:
                        results["success"] += 1
                        results["details"].append(f"SUCCESS: Reached {appliance.name} ({appliance.ip_address})")
                    else:
                        results["failed"] += 1
                        results["details"].append(f"FAILED: Reached {appliance.name} ({appliance.ip_address}) but got status {response.status_code}")

                except requests.exceptions.RequestException as e:
                    results["failed"] += 1
                    results["details"].append(f"ERROR: Could not reach {appliance.name} ({appliance.ip_address}): {type(e).__name__}")
                
                # Control the rate based on intensity
                time.sleep(max(0, 1 / test.intensity))


        # 3. Mark as COMPLETED and save results
        crud.update_test(db, test_id, schemas.TestUpdate(
            status=models.TestStatus.COMPLETED,
            results=results
        ))

    except Exception as e:
        # Mark as FAILED
        crud.update_test(db, test_id, schemas.TestUpdate(
            status=models.TestStatus.FAILED,
            results={"error": str(e)}
        ))
    finally:
        db.close()

    return True 