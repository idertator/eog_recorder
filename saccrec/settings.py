GENRES = (
    (0, 'Masculino'),
    (1, 'Femenino'),
)

SUBJECT_STATUSES = (
    (0, 'Desconocido'),
    (1, 'Control'),
    (2, 'Presintomático'),
    (3, 'SCA2'),
)

GENRES_DICT = {value: index for index, (value, _) in enumerate(GENRES)}
SUBJECT_STATUSES_DICT = {value: index for index, (value, _) in enumerate(SUBJECT_STATUSES)}
