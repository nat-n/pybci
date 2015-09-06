from .filter import Filter
from collections import deque

BUFFER_SIZE = 125

class Baseline(Filter):
    """
    Maintains a deque for each channel of the previous 125 (~500ms) samples
    divided by 125, and returns the present sample minus the average of the
    previous 125.
    """
    channel_buffers = [
        deque(), deque(), deque(), deque(),
        deque(), deque(), deque(), deque(),
        deque(), deque(), deque(), deque(),
        deque(), deque(), deque(), deque()
    ]
    rolling_averages = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def _process(self, data):
        # print "----"
        # print data['channel_data']
        data['channel_data'] = [self._apply(c, x) for c, x in enumerate(data['channel_data'])]
        # print data['channel_data']
        return data

    def _apply(self, channel_num, sample_value):
        """
        Apply baseline correction to a single sample value
        """
        dsample = sample_value / BUFFER_SIZE
        self.channel_buffers[channel_num].append(dsample)

        if len(self.channel_buffers[channel_num]) > BUFFER_SIZE:
            old_sample = self.channel_buffers[channel_num].popleft()
        else:
            old_sample = 0

        self.rolling_averages[channel_num] += (dsample - old_sample)

        return sample_value - self.rolling_averages[channel_num]
