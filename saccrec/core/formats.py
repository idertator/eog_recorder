from eoglib.models import Study, Test, Subject, Protocol, Recorder, Board

from saccrec import settings


def create_study(
    subject: Subject,
    protocol: Protocol,
    light_intensity: int,
    output_path: str,
    filenames: list[str]
) -> Study:
    study = Study(
        recorder=Recorder(
            board=Board.OpenBCI_Cyton,
            sample_rate=settings.hardware.sample_rate,
            channels=settings.hardware.channels.to_json()
        ),
        subject=subject,
        protocol_name=protocol.name,
        light_intensity=light_intensity,
        filenames=filenames
    )

    for stimulus in protocol:
        test = Test(
            stimulus=stimulus,
            study=study
        )

        study.append(test)

    return study


# from datetime import datetime
# from io import BytesIO
# from json import dumps
# from os.path import join
# from zipfile import ZipFile

# from numpy import array, int32, mean, savez_compressed

# from eoglib.models import Subject

# from saccrec import settings
# from saccrec.core.study import Hardware


# _CURRENT_VERSION = 1


# class Record:

#     def __init__(
#         self,
#         subject: Subject,
#         hardware: Hardware
#     ):
#         self._datetime = datetime.now()
#         self._subject = subject
#         self._hardware = hardware

#         self._tests = []

#     def add_test(
#         self,
#         filename: str,
#         **properties
#     ):
#         self._tests.append({
#             'filename': filename,
#             'properties': properties,
#         })

#     @property
#     def manifest_json(self) -> dict:
#         return {
#             'version': _CURRENT_VERSION,
#             'record': {
#                 'datetime': self._datetime.strftime(settings.DATETIME_FORMAT)
#             },
#             'subject': self._subject.json,
#             'hardware': self._hardware.json,
#             'tests': self._tests,
#         }

#     def _read_openbci_sd_file(path: str) -> tuple[array, array, array]:
#         def mV(sample: str) -> int:
#             return int(f'0x{sample}', 0)

#         current_stimulus = 2

#         horizontal, vertical, stimulus = [], [], []
#         with open(path, 'rt') as f:
#             for line in f:
#                 components = line.strip().split(',')
#                 if len(components) == 12:
#                     horizontal.append(mV(components[1]))
#                     vertical.append(mV(components[2]))

#                     sample_stimulus = components[-3]
#                     if sample_stimulus[-1] != '0':
#                         current_stimulus = int(sample_stimulus[-1])

#                     stimulus.append({
#                         1: 1,
#                         2: 0,
#                         3: -1,
#                     }[current_stimulus])

#         horizontal = array(horizontal, dtype=int32)[1:]
#         horizontal -= int(mean(horizontal))

#         vertical = array(vertical, dtype=int32)[1:]
#         vertical -= int(mean(vertical))

#         stimulus = array(stimulus, dtype=int32)[1:]
#         stimulus *= max((horizontal.max(), abs(horizontal.min())))

#         return horizontal, vertical, stimulus

#     def save(self, filepath: str, sd_path: str = None):
#         if sd_path is not None:
#             channels = []
#             for index, test in enumerate(self._tests):
#                 sd_file_path = join(sd_path, test['filename'])
#                 horizontal, vertical, stimulus = self._read_openbci_sd_file(sd_file_path)

#                 channels.append({
#                     'horizontal': horizontal,
#                     'vertical': vertical,
#                     'stimulus': stimulus,
#                 })

#                 test['channels'] = {
#                     'horizontal': f'{index:02}/horizontal.npz',
#                     'vertical': f'{index:02}/vertical.npz',
#                     'stimulus': f'{index:02}/stimulus.npz',
#                 }

#         with ZipFile(filepath, mode='w') as out:
#             manifest = dumps(self.manifest_json, indent=4)
#             out.writestr('manifest.json', manifest)

#             if sd_path is not None:
#                 for test, test_channels in zip(self._tests, channels):
#                     for channel, channel_path in test['channels'].items():
#                         channel_buffer = BytesIO()
#                         savez_compressed(channel_buffer, data=test_channels[channel])
#                         out.writestr(channel_path, channel_buffer.read())
