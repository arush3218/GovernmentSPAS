from pydantic import BaseModel, Field, validator
from typing import Optional


class BaseRecord(BaseModel):
    state_code: str = Field(..., max_length=10)
    state_name: str
    year: int

    @validator("year")
    def check_year(cls, v):
        if v < 2000 or v > 2100:
            raise ValueError("year out of realistic range")
        return v


class PMAYRecord(BaseRecord):
    beneficiaries: Optional[int]
    houses_completed: Optional[int]
    funds_released: Optional[float]


class MNREGARecord(BaseRecord):
    person_days_generated: Optional[int]
    job_cards: Optional[int]
    funds_spent: Optional[float]


class StartupRecord(BaseRecord):
    startups_supported: Optional[int]
    funds_allocated: Optional[float]


class SaubhagyaRecord(BaseRecord):
    households_electrified: Optional[int]
    percent_coverage: Optional[float]


SCHEMAS = {
    "pmay": PMAYRecord,
    "mnrega": MNREGARecord,
    "startup_india": StartupRecord,
    "saubhagya": SaubhagyaRecord,
}
