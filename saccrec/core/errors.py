class NotEnoughDataError(Exception):

    def __init__(self, buffer, count: int):
        self._buffer = buffer
        self._count = count

    def __str__(self) -> str:
        return f'The buffer only contains {len(self._buffer)} samples, {self._count} requested'
