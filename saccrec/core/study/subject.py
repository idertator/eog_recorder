from datetime import datetime, date
from typing import Union, Optional

from saccrec import settings
from saccrec.core.enums import Gender, SubjectStatus


class Subject:

    def __init__(
        self,
        name: str = 'Unknown',
        gender: Union[str, Gender] = Gender.Unknown,
        status: Union[str, SubjectStatus] = SubjectStatus.Unknown,
        borndate: Optional[Union[str, date, datetime]] = None
    ):
        if isinstance(name, str):
            self._name = name
        else:
            self._name = 'Unknown'

        if isinstance(gender, str):
            self._gender = Gender(gender)
        elif isinstance(gender, Gender):
            self._gender = gender
        else:
            self._gender = Gender.Unknown

        if isinstance(status, str):
            self._status = SubjectStatus(status)
        elif isinstance(status, SubjectStatus):
            self._status = status
        else:
            self._status = SubjectStatus.Unknown

        if isinstance(borndate, str):
            self._borndate = datetime.strptime(borndate, settings.DATE_FORMAT).date()
        elif isinstance(borndate, datetime):
            self._borndate = borndate.date()
        elif isinstance(borndate, date):
            self._borndate = borndate
        else:
            self._borndate = None

    def __str__(self) -> str:
        return self._name

    def __json__(self) -> dict:
        return {
            'full_name': self._name,
            'gender': self._gender.value,
            'status': self._status.value,
            'borndate': self._borndate.strftime(settings.DATE_FORMAT) if self._borndate is not None else None,
        }

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if isinstance(value, str):
            self._name = value
        else:
            raise AttributeError('name must be of type str')

    @property
    def gender(self) -> Gender:
        return self._gender

    @gender.setter
    def gender(self, value: Union[int, Gender]):
        if isinstance(value, int):
            self._gender = Gender(value)
        elif isinstance(value, Gender):
            self._gender = value
        else:
            raise AttributeError('gender must be of type str or type Gender')

    @property
    def status(self) -> SubjectStatus:
        return self._status

    @status.setter
    def status(self, value: Union[str, SubjectStatus]):
        if isinstance(value, str):
            self._status = SubjectStatus(value)
        elif isinstance(value, SubjectStatus):
            self._status = value
        else:
            raise AttributeError('status must be of type str or type SubjectStatus')

    @property
    def borndate(self) -> date:
        return self._borndate

    @borndate.setter
    def borndate(self, value: Optional[Union[str, date, datetime]]):
        if isinstance(value, str):
            self._borndate = datetime.strptime(value, settings.DATE_FORMAT).date()
        elif isinstance(value, datetime):
            self._borndate = value.date()
        elif isinstance(value, date):
            self._borndate = value
        else:
            raise AttributeError('borndate must be of type str, type datetime or type date')

    @property
    def age(self) -> int:
        today = date.today()
        if self._borndate is not None:
            years = today.year - self._borndate.year
            if today.month > self._borndate.month:
                return years + 1
            if today.month < self._borndate.year:
                return years
            if today.day >= self._borndate.day:
                return years + 1
            return years
        return 0
