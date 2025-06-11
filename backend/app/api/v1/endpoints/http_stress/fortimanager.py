from fastapi import APIRouter, Query
import asyncio
from app.core.http_stress import fortimanager

router = APIRouter()

@router.get("/forti_test")
async def forti_test(intensity: float = Query(1.0, gt=0)):
   
    async def loop_scripts():
        while True:
            await asyncio.to_thread(fortimanager.create_object)
            await asyncio.to_thread(fortimanager.create_rule)
            await asyncio.sleep(intensity)

    asyncio.create_task(loop_scripts())
    return {"status": "forti stress test strarte", "intensity_seconds": intensity}
