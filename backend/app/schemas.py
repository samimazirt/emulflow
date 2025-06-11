from pydantic import BaseModel, IPvAnyAddress
from typing import Optional, List
from .models import ApplianceType, ApplianceFamily, TestStatus
from datetime import datetime

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

class TestBase(BaseModel):
    intensity: Optional[int] = 10

class TestCreate(TestBase):
    appliance_ids: List[int]

class TestUpdate(BaseModel):
    status: Optional[TestStatus] = None
    results: Optional[dict] = None
    end_time: Optional[datetime] = None

# Properties shared by models stored in DB
class ApplianceInDBBase(ApplianceBase):
    id: int
    class Config:
        orm_mode = True

# To break the circular dependency, we create schemas specifically for nested responses.

class ApplianceInTestDetail(ApplianceInDBBase):
    # This version of Appliance does NOT include the 'tests' field
    # to avoid the recursion loop when it's nested inside a Test response.
    pass

class TestInApplianceDetail(TestBase):
    # This version of Test does NOT include the 'appliances' field.
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    status: TestStatus
    results: Optional[dict] = None
    class Config:
        orm_mode = True

# --- Top-level schemas to be returned to client ---

class Appliance(ApplianceInDBBase):
    tests: List[TestInApplianceDetail] = []

class Test(TestBase):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    status: TestStatus
    results: Optional[dict] = None
    appliances: List[ApplianceInTestDetail] = []
    class Config:
        orm_mode = True

# Properties stored in DB
class ApplianceInDB(ApplianceInDBBase):
    password: str