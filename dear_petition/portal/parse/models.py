import datetime as dt
import logging
from typing import List, Optional

from pydantic import BaseModel, field_validator

logger = logging.getLogger(__name__)


class Charge(BaseModel):
    number: int = None
    offense: Optional[str] = ""
    statute: Optional[str] = ""
    degree: Optional[str] = ""
    offense_date: dt.date = None
    filed_date: dt.date = None

    @field_validator("offense_date", "filed_date", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            return dt.datetime.strptime(v, "%m/%d/%Y")
        return v

    class Config:
        validate_assignment = True


class CaseInfo(BaseModel):
    charges: List[Charge]
    case_type: str
    case_status: str
    case_status_date: dt.date

    @field_validator("case_status_date", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            return dt.datetime.strptime(v, "%m/%d/%Y")
        return v
