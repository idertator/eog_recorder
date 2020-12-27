from eoglib.io import save_eog
from eoglib.models import Board, Protocol, Recorder, Study, Subject, Test

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

    save_eog(output_path, study)

    return study
