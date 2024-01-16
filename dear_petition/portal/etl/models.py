import datetime as dt
from typing import List, Union

from pydantic import BaseModel, field_validator

from dear_petition.petition import constants


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

    def transform_severity(self):
        """Attempt to convert Portal's degree to CIPRS severity"""
        severity = self.degree
        if self.degree in constants.CHARGED_DEGREE_FELONY:
            severity = constants.SEVERITY_FELONY
        elif self.degree in constants.CHARGED_DEGREE_MISDEMEANOR:
            severity = constants.SEVERITY_MISDEMEANOR
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
    defendant_race: str
    defendant_sex: str


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

    def is_dismissed(self) -> bool:
        return self.criminal_disposition in constants.DISMISSED_DISPOSITION_METHODS

    def transform_action(self) -> str:
        action = self.event
        if self.is_dismissed():
            action = constants.CHARGED
        return action

    def transform_disposition_method(self) -> str:
        if self.is_dismissed():
            return constants.DISTRICT_COURT_WITHOUT_DA_LEAVE
        return self.criminal_disposition


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

    def transform_offense_date(self) -> dt.date:
        offense_dates = [c.offense_date for c in self.case_info.charges]
        return min(offense_dates).isoformat()
