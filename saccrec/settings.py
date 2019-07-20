# Subject Parameters

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

# Stimulus Parameters

STIMULUS_DEFAULT_ANGLE = 30
STIMULUS_MINIMUM_ANGLE = 10
STIMULUS_MAXIMUM_ANGLE = 60

STIMULUS_DEFAULT_DURATION = 3.0
STIMULUS_DEFAULT_VARIABILITY = 50.0

STIMULUS_DEFAULT_SACCADES = 10
STIMULUS_MINUMUM_SACCADES = 5
STIMULUS_MAXIMUM_SACCADES = 100
