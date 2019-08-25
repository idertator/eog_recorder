from typing import Optional, Union, List

from saccrec.core import BoardTypes, BoardModes, SampleRates


_BOARD_FIELD = 'board'
_BOARD_MODE_FIELD = 'mode'
_SAMPLE_RATE_FIELD = 'sample_rate'
_CHANNELS_FIELDS = 'channels'


class Hardware:
    
    def __init__(
        self, 
        board: Optional[Union[BoardTypes, str]] = None,
        mode: Optional[Union[BoardModes, str]] = None,
        sample_rate: Optional[Union[SampleRates, str]] = None,
        channels: List[dict] = list()
    ):
        if isinstance(board, str):
            self._board = BoardTypes(board)
        else:
            self._board = board

        if isinstance(mode, str):
            self._mode = BoardModes(mode)
        else:
            self._mode = mode

        if isinstance(sample_rate, int):
            self._sample_rate = SampleRates(sample_rate)
        else:
            self._sample_rate = sample_rate

        self._channels = channels

    @property
    def board(self) -> Optional[BoardTypes]:
        return self._board

    @board.setter
    def board(self, value: Optional[Union[BoardTypes, str]]):
        if isinstance(value, str):
            self._board = BoardTypes(value)
        else:
            self._board = value

    @property
    def mode(self) -> Optional[BoardModes]:
        return self._mode

    @mode.setter
    def mode(self, value: Optional[Union[BoardModes, str]]):
        if isinstance(value, str):
            self._mode = BoardModes(value)
        else:
            self._mode = value

    @property
    def sample_rate(self) -> Optional[SampleRates]:
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value: Optional[Union[SampleRates, int]]):
        if isinstance(value, int):
            self._sample_rate = SampleRates(value)
        else:
            self._sample_rate = value

    @property
    def channels(self) -> List[dict]:
        return self._channels

    @channels.setter
    def channels(self, value: List[dict]):
        self._channels = value

    @property
    def json(self) -> dict:
        return {
            _BOARD_FIELD: self._board.value if self._board is not None else None,
            _BOARD_MODE_FIELD: self._mode.value if self._mode is not None else None,
            _SAMPLE_RATE_FIELD: self._sample_rate.value if self._sample_rate is not None else None,
            _CHANNELS_FIELDS: self._channels,
        }

    @classmethod
    def from_json(cls, json: dict) -> 'Hardware':
        return Hardware(
            board=json.get(_BOARD_FIELD, None),
            mode=json.get(_BOARD_MODE_FIELD, None),
            sample_rate=json.get(_SAMPLE_RATE_FIELD, None),
            channels=json.get(_CHANNELS_FIELDS, [])
        )
