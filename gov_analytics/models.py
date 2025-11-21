from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from .db import Base


class BaseScheme(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    state_code = Column(String(10), index=True)
    state_name = Column(String(100), index=True)
    year = Column(Integer, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PMAY(BaseScheme):
    __tablename__ = "pmay"
    beneficiaries = Column(Integer, nullable=True)
    houses_completed = Column(Integer, nullable=True)
    funds_released = Column(Float, nullable=True)


class MNREGA(BaseScheme):
    __tablename__ = "mnrega"
    person_days_generated = Column(Integer, nullable=True)
    job_cards = Column(Integer, nullable=True)
    funds_spent = Column(Float, nullable=True)


class StartupIndia(BaseScheme):
    __tablename__ = "startup_india"
    startups_supported = Column(Integer, nullable=True)
    funds_allocated = Column(Float, nullable=True)


class Saubhagya(BaseScheme):
    __tablename__ = "saubhagya"
    households_electrified = Column(Integer, nullable=True)
    percent_coverage = Column(Float, nullable=True)


__all__ = ["PMAY", "MNREGA", "StartupIndia", "Saubhagya"]
