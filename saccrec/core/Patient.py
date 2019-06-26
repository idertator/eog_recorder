class Patient:

    def __init__(self, full_name, born_date, genre, state):
        self._full_name = full_name
        self._born_date = born_date
        self._genre = genre
        self._state = state

    @property
    def full_name(self):
        return self._full_name

    @property
    def born_date(self):
        return self._born_date

    @property
    def genre(self):
        return self._genre

    @property
    def state(self):
        return self._state