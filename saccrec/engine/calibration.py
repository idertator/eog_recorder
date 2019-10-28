from typing import Optional, List

from saccrec.core import Study, SaccadicTest, Saccade
from saccrec.core.enums import Channel
from saccrec.engine.processing import identify_kmeans

from numpy import mean


def _filter_amplitudes(amplitudes: List[float], threshold: float) -> List[float]:
    amplitudes_mean = mean(amplitudes)
    min_value = amplitudes_mean * (1.0 - threshold)
    max_value = amplitudes_mean * (1.0 + threshold)
    return [amp for amp in amplitudes if min_value <= amp <= max_value]


def calibrate(study: Study, channel: Channel = Channel.Horizontal) -> Optional[float]:
    tests = study.filter(test_cls=SaccadicTest, calibration=True)

    if len(tests) >= 2:
        saccades = {}
        for index in 0, -1:
            test = tests[index]
            saccades[index] = [
                Saccade(
                    onset=onset,
                    offset=offset,
                    test=test,
                    channel=channel,
                    ignore_calibration=True
                ) for onset, offset in identify_kmeans(
                    channel=test.horizontal,
                    sampling_interval=study.sampling_interval
                )
            ]

        first_amplitudes = [saccade.amplitude for saccade in saccades[0]]
        first_mean = mean(first_amplitudes)

        last_amplitudes = [saccade.amplitude for saccade in saccades[-1]]
        last_mean = mean(last_amplitudes)

        # TODO: Calibration quality check

        return float(tests[0].angle) / ((first_mean + last_mean) / 2.0)

    return None

if __name__ == '__main__':
    study = Study.open('/Users/idertator/Recordings/rgb20190831_12.rec')

    horizontal_calibration = calibrate(study)

    print(f'Horizontal Calibration: {horizontal_calibration}')
