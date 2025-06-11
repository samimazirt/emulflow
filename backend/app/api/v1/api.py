from fastapi import APIRouter
from .endpoints import appliances

api_router = APIRouter()
api_router.include_router(appliances.router, prefix="/appliances", tags=["appliances"]) 