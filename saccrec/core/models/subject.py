from typing import Optional, Union

from datetime import date

from saccrec.core.enums import Genre, SubjectStatus


class Subject:
    
    def __init__(
        self,
        full_name: str = '',
        genre: Optional[Union[Genre, int]] = None,
        borndate: date = None,
        status: Optional[Union[SubjectStatus, int]] = None
    ):
        self._full_name = full_name

        if isinstance(genre, int):
            self._genre = Genre(genre)
        else:
            self._genre = genre

        self._borndate = borndate

        if isinstance(status, int):
            self._status = SubjectStatus(status)
        else:
            self._status = status

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str):
        self._full_name = full_name
    
    @property
    def genre(self) -> Optional[Genre]:
        return self._genre

    @genre.setter
    def genre(self, value: Optional[Union[Genre, int]]):
        if isinstance(value, int):
            self._genre = Genre(value)
        else:
            self._genre = value

    @property
    def borndate(self) -> Optional[date]:
        return self._borndate

    @borndate.setter
    def borndate(self, value: date):
        self._borndate = borndate

    @property
    def status(self) -> Optional[SubjectStatus]:
        return self._status

    @status.setter
    def status(self, value: Optional[Union[SubjectStatus, int]]):
        if isinstance(value, int):
            self._status = SubjectStatus(value)
        else:
            self._status = value

    @property
    def json(self) -> dict:
        return {
            'full_name': self.full_name,
            'genre': self._genre.value if self._genre is not None else None,
            'borndate': self.borndate.strftime('%d/%m/%Y'),
            'status': self.status.value if self._status is not None else None,
        }
    