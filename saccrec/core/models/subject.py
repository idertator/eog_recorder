from typing import Optional, Union

from datetime import date, datetime

from saccrec.core import Gender, SubjectStatus
from saccrec.settings import DATE_FORMAT


_FULL_NAME_FIELD = 'full_name'
_GENDER_FIELD = 'gender'
_BORNDATE_FIELD = 'borndate'
_STATUS_FIELD = 'status'


class Subject:

    def __init__(
        self,
        full_name: str = '',
        gender: Optional[Union[Gender, int]] = None,
        borndate: [date, str] = None,
        status: Optional[Union[SubjectStatus, str]] = None
    ):
        self._full_name = full_name

        if isinstance(gender, int):
            self._gender = Gender(gender)
        else:
            self._gender = gender

        if isinstance(borndate, str):
            self._gender = datetime.strptime(borndate, DATE_FORMAT)
        else:
            self._borndate = borndate

        if isinstance(status, str):
            self._status = SubjectStatus(status)
        else:
            self._status = status

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str):
        self._full_name = value

    @property
    def gender(self) -> Optional[Gender]:
        return self._gender

    @gender.setter
    def gender(self, value: Optional[Union[Gender, str]]):
        if isinstance(value, str):
            self._gender = Gender(value)
        else:
            self._gender = value

    @property
    def borndate(self) -> Optional[date]:
        return self._borndate

    @borndate.setter
    def borndate(self, value: date):
        self._borndate = value

    @property
    def status(self) -> Optional[SubjectStatus]:
        return self._status

    @status.setter
    def status(self, value: Optional[Union[SubjectStatus, str]]):
        if isinstance(value, str):
            self._status = SubjectStatus(value)
        else:
            self._status = value

    @property
    def json(self) -> dict:
        return {
            _FULL_NAME_FIELD: self.full_name,
            _GENDER_FIELD: self._gender.value if self._gender is not None else None,
            _BORNDATE_FIELD: self.borndate.strftime(DATE_FORMAT),
            _STATUS_FIELD: self.status.value if self._status is not None else None,
        }

    @classmethod
    def from_json(cls, json: dict) -> 'Subject':
        return Subject(
            full_name=json.get(_FULL_NAME_FIELD, 'Unknown'),
            gender=json.get(_GENDER_FIELD, Gender.Unknown),
            borndate=json.get(_BORNDATE_FIELD, None),
            status=json.get(_STATUS_FIELD, SubjectStatus.Unknown)
        )
