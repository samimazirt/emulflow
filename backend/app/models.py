from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

class ApplianceType(str, enum.Enum):
    FIREWALL = "firewall"
    MANAGER = "manager"
    MANAGER_OF_MANAGER = "manager_of_manager"

class ApplianceFamily(str, enum.Enum):
    FORTIGATE = "fortigate"
    PALO_ALTO = "palo_alto"
    CHECKPOINT_GATEWAY = "checkpoint_gateway"
    MDS = "mds"
    PANORAMA = "panorama"
    FORTIMANAGER = "fortimanager"
    RULEBLADE = "ruleblade"

class Appliance(Base):
    __tablename__ = "appliances"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ip_address = Column(String, unique=True, index=True)
    appliance_type = Column(Enum(ApplianceType))
    appliance_family = Column(Enum(ApplianceFamily))
    username = Column(String)
    password = Column(String) # Note: In a real app, this should be encrypted 