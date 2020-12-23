from typing import Optional

from eoglib.models import Subject, Protocol


class Workspace:

    def __init__(self):
        self._subject = Subject()
        self._protocol = None
        self._filepath = None

    def reset_workspace(self):
        self._subject = Subject()
        self._protocol = None
        self._filepath = None
        self._new_record_wizard.reset()

    @property
    def subject(self) -> Subject:
        return self._subject

    @property
    def protocol(self) -> Protocol:
        return self._protocol

    @protocol.setter
    def protocol(self, value: Protocol):
        assert isinstance(value, Protocol)
        self._protocol = value

    @property
    def filepath(self) -> Optional[str]:
        return self._filepath

    @filepath.setter
    def filepath(self, value: str):
        self._filepath = value

    @property
    def html_overview(self) -> str:
        from saccrec.core.templating import render
        return render(
            'overview',
            subject=self._subject,
            protocol=self._protocol
        )
