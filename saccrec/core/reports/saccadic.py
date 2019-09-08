from numpy import mean, std
from tablib import Databook, Dataset

from saccrec.core import Study, SaccadicTest
from saccrec.core.enums import Channel
from saccrec.engine.calibration import calibrate

_HEADERS = ['#', 'Onset', 'Offset', 'Amplitud', 'Duración', 'Velocidad Máxima']


def excel_saccadic_report(study: Study, output_path: str):
    if abs(study.horizontal_calibration - 1) < 0.00001:
        study.horizontal_calibration = calibrate(study, channel=Channel.Horizontal)

    databook = Databook()
    for idx, test in enumerate(study.filter(test_cls=SaccadicTest)):
        saccades = test.horizontal_saccades

        amplitudes = [x.amplitude for x in saccades]
        durations = [x.duration for x in saccades]
        max_velocities = [x.max_velocity for x in saccades]

        dataset = Dataset(
            headers=_HEADERS, 
            title=f'{idx:02}. Saccadic {test.angle}' + (' Calibration' if test.is_calibration else '')
        )

        for index, saccade in enumerate(saccades):
            dataset.append([
                index + 1, 
                saccade.onset,
                saccade.offset,
                saccade.amplitude,
                saccade.duration,
                saccade.max_velocity
            ])

        dataset.append(['', '', '', '', '', ''])
        dataset.append(['', '', 'Media:',
            mean(amplitudes),
            mean(durations),
            mean(max_velocities)
        ])
        dataset.append(['', '', 'Desv. Típica:',
            std(amplitudes),
            std(durations),
            std(max_velocities)
        ])

        databook.add_sheet(dataset)

    with open(output_path, 'wb') as f:
        f.write(databook.export('xls'))


if __name__ == '__main__':
    study = Study.open('/Users/idertator/Recordings/rgb20190831_12.rec')
    excel_saccadic_report(study, '/Users/idertator/Recordings/rgb20190831_12.xls')
    study.save('/Users/idertator/Recordings/rgb20190831_12_saccades.rec')
