from typing import List

from saccrec.core import SaccadicTest, Saccade
from saccrec.core.enums import Channel
from saccrec.engine.processing import identify_kmeans


def identify_saccades(test: SaccadicTest, channel: Channel = Channel.Horizontal) -> List[Saccade]:
    saccades = []
    channel_samples = test.channel_samples(channel)

    for onset, offset in identify_kmeans(
        channel=channel_samples,
        sampling_interval=test.study.sampling_interval
    ):
        saccades.append(
            Saccade(
                onset=onset,
                offset=offset,
                channel=channel,
                test=test
            )
        )

    return saccades
