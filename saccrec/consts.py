# Subject Parameters
DEBUG = True

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

OPENBCI_BOARD_TYPES = (
    ('cyton', 'cyton'),
    ('ganglion', 'ganglion'),
    ('daisy', 'daisy'),
)

OPENBCI_SAMPLE_RATES = (
    (250, '250'),
    (500, '500'),
    (1000, '1000'),
    (2000, '2000'),
    (4000, '4000'),
    (8000, '8000'),
    (16000, '16000'),
)

OPENBCI_BOARD_MODES = (
    ('default', 'default'),
    ('debug', 'debug'),
    ('analog', 'analog'),
    ('digital', 'digital'),
    ('marker', 'marker'),
)

GENRES_DICT = {value: index for index, (value, _) in enumerate(GENRES)}
SUBJECT_STATUSES_DICT = {value: index for index, (value, _) in enumerate(SUBJECT_STATUSES)}
SUBJECT_STATUSES_LABELS = {value: label for value, label in SUBJECT_STATUSES}

# Stimulus Parameters
STIMULUS_DEFAULT_ANGLE = 30
STIMULUS_MINIMUM_ANGLE = 10
STIMULUS_MAXIMUM_ANGLE = 60

STIMULUS_DEFAULT_DURATION = 3.0
STIMULUS_DEFAULT_VARIABILITY = 50.0

STIMULUS_DEFAULT_SACCADES = 10
STIMULUS_MINUMUM_SACCADES = 5
STIMULUS_MAXIMUM_SACCADES = 100

SETTINGS_STIMULUS_SCREEN_WIDTH_MINIMUM = 10.0
SETTINGS_STIMULUS_SCREEN_WIDTH_MAXIMUM = 200.0

SETTINGS_STIMULUS_SCREEN_HEIGHT_MINIMUM = 10.0
SETTINGS_STIMULUS_SCREEN_HEIGHT_MAXIMUM = 200.0

SETTINGS_STIMULUS_SACCADIC_DISTANCE_MINIMUM = 5.0
SETTINGS_STIMULUS_SACCADIC_DISTANCE_MAXIMUM = SETTINGS_STIMULUS_SCREEN_WIDTH_MAXIMUM - 2

SETTINGS_SAMPLING_FREQUENCY_MINIMUM = 200   # TODO: Depecrated. Remove this
SETTINGS_SAMPLING_FREQUENCY_MAXIMUM = 1000  # TODO: Deprecated. Remove this

SETTINGS_OPENBCI_DEFAULT_BAUDRATE = 115200
SETTINGS_OPENBCI_DEFAULT_BAUDRATE_MINIMUM = 1
SETTINGS_OPENBCI_DEFAULT_BAUDRATE_MAXIMUM = 115200

SETTINGS_OPENBCI_DEFAULT_TIMEOUT = 0
SETTINGS_OPENBCI_DEFAULT_TIMEOUT_MINIMUM = 0
SETTINGS_OPENBCI_DEFAULT_TIMEOUT_MAXIMUM = 1000

SETTINGS_OPENBCI_DEFAULT_BOARD_TYPE = 'cyton'
SETTINGS_OPENBCI_DEFAULT_BOARD_MODE = 'default'
SETTINGS_OPENBCI_DEFAULT_SAMPLE_RATE = 250

SETTINGS_OPENBCI_DEFAULT_GAIN = 24
SETTINGS_OPENBCI_DEFAULT_CHANNEL_NUMBER = 8

SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS = 0.5
SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS_MINIMUM = 0.1
SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS_MAXIMUM = 1.0

SETTINGS_DEFAULT_STIMULUS_BALL_COLOR = '#ffffffff'
SETTINGS_DEFAULT_STIMULUS_BACKGROUND_COLOR = '#00000000'

