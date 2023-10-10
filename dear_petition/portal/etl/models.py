import datetime as dt
import logging
from typing import List, Union

from pydantic import BaseModel, field_validator

logger = logging.getLogger(__name__)


class CaseSummary(BaseModel):
    case_number: str
    county: str
    court: str


class Charge(BaseModel):
    number: Union[int, None]
    offense: str
    statute: str
    degree: str
    offense_date: Union[dt.date, None]
    filed_date: Union[dt.date, None]

    @field_validator("offense_date", "filed_date", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            return dt.datetime.strptime(v, "%m/%d/%Y")
        return v


class CaseInfo(BaseModel):
    case_type: str
    case_status: str
    case_status_date: Union[dt.date, None]
    charges: List[Charge]

    @field_validator("case_status_date", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            return dt.datetime.strptime(v, "%m/%d/%Y")
        return v


class PartyInfo(BaseModel):
    defendant_name: str


class PortalRecord(BaseModel):
    case_summary: CaseSummary
    case_info: CaseInfo
    party_info: PartyInfo
