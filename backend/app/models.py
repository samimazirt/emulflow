from sqlalchemy import Column, Integer, String, Enum, DateTime, JSON, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum
import datetime

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

class TestStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"

test_appliance_association = Table(
    'test_appliance_association', Base.metadata,
    Column('test_id', Integer, ForeignKey('tests.id')),
    Column('appliance_id', Integer, ForeignKey('appliances.id'))
)

class Appliance(Base):
    __tablename__ = "appliances"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ip_address = Column(String, unique=True, index=True)
    appliance_type = Column(Enum(ApplianceType))
    appliance_family = Column(Enum(ApplianceFamily))
    username = Column(String)
    password = Column(String) # Note: In a real app, this should be encrypted

    tests = relationship("Test", secondary=test_appliance_association, back_populates="appliances")

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(Enum(TestStatus), default=TestStatus.PENDING)
    intensity = Column(Integer, default=10)
    results = Column(JSON, nullable=True)

    appliances = relationship("Appliance", secondary=test_appliance_association, back_populates="tests") 