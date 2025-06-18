from fastapi import APIRouter
from .endpoints import appliances
from app.api.v1.endpoints import tests
from app.api.v1.endpoints.http_stress import fortimanager
from app.api.v1.endpoints import stats

api_router = APIRouter()
api_router.include_router(appliances.router, prefix="/appliances", tags=["appliances"])
api_router.include_router(tests.router, prefix="/tests", tags=["tests"]) 
api_router.include_router(fortimanager.router, prefix="/fortimanager", tags=["fortimanager"]) 
api_router.include_router(stats.router, prefix="/stats", tags=["stats"]) 