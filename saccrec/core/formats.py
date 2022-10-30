from eoglib.io import save_eog
from eoglib.models import Board, Protocol, Recorder, Study, Subject, Test

from saccrec import settings


def create_study(
    subject: Subject,
    protocol: Protocol,
    light_intensity: int,
    output_path: str,
    source_filename: str,
) -> Study:
    study = Study(
        recorder=Recorder(
            board=Board.OpenBCI_Cyton,
            sample_rate=settings.hardware.sampling_rate,
            channels=settings.hardware.channels.json,
        ),
        subject=subject,
        protocol_name=protocol.name,
        light_intensity=light_intensity,
        obci_filename=source_filename,
    )

    for stimulus in protocol:
        test = Test(stimulus=stimulus, study=study)

        study.append(test)

    save_eog(output_path, study)

    return study
