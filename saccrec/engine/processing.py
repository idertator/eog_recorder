from numba import njit, stencil
from numpy import array
from scipy.signal import medfilt
from sklearn.cluster import KMeans


@njit(fastmath=True, parallel=True)
def differentiate(data: array, step: float) -> array:
    return stencil(
        lambda f, h: (f[1] - f[-1] + 2 * (f[2] - f[-2]) + 3 * (f[3] - f[-3]) + 4 * (f[4] - f[-4]) + 5 * (f[5] - f[-5])) / (110 * h)
    )(data, step)


def identify_kmeans(
    channel: array,
    sampling_interval: float,
    join_threshold: int = 0,
    amplitude_threshold: float = 0
):
    """Identify impulses from velocity profiles in eye movement signals

    This method identify impulses using the KMeans clustering algorithm.
    The idea behind this method is try to separate high velocity samples from low velocity ones into 2 clusters using KMeans.

    Contrary to Nyström approach we set the onset and offset points when the velocity cannot decrease no more, so there is no
    need for thresholds.

    Args:
        channel: Signal profile
        join_threshold: How many samples are considered close to merge two impulses
        amplitude_threshold: How many microvolts difference is needed to be considered a correct impulse
    Yields:
        (int, int): Onset and offset impulse points
    """
    velocity = medfilt(differentiate(channel, sampling_interval), 9)
    estimator = KMeans(n_clusters=2)
    X = abs(velocity.reshape((len(velocity), 1)))
    labels = estimator.fit_predict(X)

    high = 1 if X[labels == 1].mean() > X[labels == 0].mean() else 0

    ranges = []
    start = -1
    for index, label in enumerate(labels):
        if label == high and start == -1:
            start = index
        if label != high and start != -1:
            ranges.append((start, index - 1))
            start = -1

    last_range = None
    window = None
    for start, end in ranges:
        while start > 0 and X[start - 1] < X[start]:
            start -= 1
        while end < len(X) - 1 and X[end + 1] < X[end]:
            end += 1

        if last_range is None:
            last_range = [start, end]
        else:
            if start - last_range[1] > join_threshold:
                window = channel[last_range[0]:last_range[1]]
                if max(window) - min(window) >= amplitude_threshold:
                    yield last_range
                last_range = [start, end]
            else:
                last_range[1] = end

    if window is not None and last_range is not None and max(window) - min(window) >= amplitude_threshold:
        yield last_range
