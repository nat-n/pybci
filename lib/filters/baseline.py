from .filter import Filter
from collections import deque

class Baseline(Filter):
    """
    Maintains a deque for each channel of the previous 125 (~500ms) samples
    divided by 125, and returns the present sample minus the average of the
    previous 125.
    """
    name = 'filter:baseline'
    _default_config = {
        'buffer_size': 125
    }
    channel_buffers = [
        deque(), deque(), deque(), deque(),
        deque(), deque(), deque(), deque(),
        deque(), deque(), deque(), deque(),
        deque(), deque(), deque(), deque()
    ]
    rolling_averages = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, **kwargs):
        super(Baseline, self).__init__(**kwargs)

    def _process(self, data):
        data['channel_data'] = [self._apply(c, x) for c, x in enumerate(data['channel_data'])]
        return data

    def _apply(self, channel_num, sample_value):
        """
        Apply baseline correction to a single sample value
        """
        dsample = sample_value / self.config['buffer_size']
        self.channel_buffers[channel_num].append(dsample)

        if len(self.channel_buffers[channel_num]) > self.config['buffer_size']:
            old_sample = self.channel_buffers[channel_num].popleft()
        else:
            old_sample = 0

        self.rolling_averages[channel_num] += (dsample - old_sample)

        return sample_value - self.rolling_averages[channel_num]
