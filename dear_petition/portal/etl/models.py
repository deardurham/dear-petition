import datetime as dt
from typing import List, Union

from pydantic import BaseModel, field_validator


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

    @property
    def severity(self):
        """Attempt to convert Portal's degree to CIPRS severity"""
        severity = self.degree
        if self.degree in ("FH", "FNC"):
            severity = "FELONY"
        elif self.degree in ("MNC",):
            severity = "MISDEMEANOR"
        return severity


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


class Disposition(BaseModel):
    event_date: Union[dt.date, None]
    event: str
    charge_number: int
    charge_offense: str
    criminal_disposition: str

    @field_validator("event_date", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            return dt.datetime.strptime(v, "%m/%d/%Y")
        return v


class PortalRecord(BaseModel):
    case_summary: CaseSummary
    case_info: CaseInfo
    party_info: PartyInfo
    dispositions: List[Disposition]

    def get_charge_by_number(self, charge_number: int):
        """Return matching CaseInfo.charges Charge by charge_number"""
        for charge in self.case_info.charges:
            if charge.number == charge_number:
                return charge
