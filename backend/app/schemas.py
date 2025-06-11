from pydantic import BaseModel, IPvAnyAddress
from typing import Optional
from .models import ApplianceType, ApplianceFamily

# Shared properties
class ApplianceBase(BaseModel):
    name: str
    ip_address: IPvAnyAddress
    appliance_type: ApplianceType
    appliance_family: ApplianceFamily
    username: str

# Properties to receive on item creation
class ApplianceCreate(ApplianceBase):
    password: str

# Properties to receive on item update
class ApplianceUpdate(ApplianceBase):
    password: Optional[str] = None

# Properties shared by models stored in DB
class ApplianceInDBBase(ApplianceBase):
    id: int

    class Config:
        orm_mode = True

# Properties to return to client
class Appliance(ApplianceInDBBase):
    pass

# Properties stored in DB
class ApplianceInDB(ApplianceInDBBase):
    password: str 