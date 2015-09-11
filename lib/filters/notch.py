from .filter import Filter
from time import sleep

from threading import Thread, Lock
import numpy as np
from scipy import signal

# TODO: consider whether it would be faster to use fixed numpy arrays for buffers and
#       maintain a cursor.

class Notch(Filter):
    """
    Filters out a specific frequency from the signal.
    """

    _default_config = {
        'channels': [0, 1, 2, 3, 4, 5, 6, 7],
        'frequency': 50,
        'buffer_size': 125,
        'min_buffer_head': 10
    }

    filters = {
        "50": {
            "a": np.array([1.0       , -1.21449348, 2.29780334, -1.17207163, 0.93138168]),
            "b": np.array([0.96508099, -1.19328255, 2.29902305, -1.19328255, 0.96508099])
        },
        "60": {
            "a": np.array([ 1.0       , -0.24677826, 1.94417178, -0.23815838, 0.93138168]),
            "b": np.array([ 0.96508099, -0.24246832, 1.94539149, -0.24246832, 0.96508099])
        }
    }

    _packet_buffer = []
    _packet_buffer_lock = Lock()
    # maintain a buffer for samples from each
    _channel_buffers = []
    # channel buffers are accessed from multiple threads so should be locked
    _channel_buffer_locks = []
    streaming = True

    _prev_len = 0

    def __init__(self, **kwargs):
        super(Notch, self).__init__(**kwargs)
        self.name = 'filter:notch'


        if not 'frequency' in self.config:
            self.config['frequency'] = DEFAULT_CONFIG
        if not 'channels' in self.config:
            self.config['channels'] = DEFAULT_CHANNELS
        self.filter_config = self.filters[str(self.config['frequency'])]

        for c in self.config['channels']:
            self._channel_buffers.append([])
            self._channel_buffer_locks.append(Lock())

        # hereby the buffer builds up to a certain length before being flushed
        self._prev_len = self.config['buffer_size']

        self.loop_thread = Thread(target=self._loop)
        self.loop_thread.daemon = True # not sure about this...
        self.loop_thread.start()

    def _loop(self):
        while self.streaming:
            max_len = self._prev_len + self.config['min_buffer_head']
            sleep(0.001)
            if len(self._packet_buffer) > max_len:
                self._flush()

    def _push_to_buffers(self, data):
        for c, d in enumerate(data['channel_data']):
            cBuffer = self._channel_buffers[c]
            with self._channel_buffer_locks[c]:
                cBuffer.append(d)
        with self._packet_buffer_lock:
            self._packet_buffer.append(data)

    def _flush(self):
        with self._packet_buffer_lock:
            head = len(self._packet_buffer) - self._prev_len
            filtered_buffers = []
            for c in self.config['channels']:
                cBuffer = self._channel_buffers[c]
                with self._channel_buffer_locks[c]:
                    filtered_buffers.append(list(self._fliter(cBuffer)))
                    del cBuffer[:head]

            # Pass processed samples on to children maintaining order
            buffer_len = len(self._packet_buffer)
            for i in xrange(buffer_len - head, buffer_len):
                packet = self._packet_buffer[i]
                # replace channel_data in with filtered values
                for j, fbuffer in enumerate(filtered_buffers):
                    packet['channel_data'][j] = fbuffer[i]
                # send original data packet dict
                for c in self._children:
                    c._on_data(packet)
            # clear forwarded packets from the buffer
            del self._packet_buffer[:head]
            self._prev_len = len(self._packet_buffer)

    def _on_data(self, data):
        self._push_to_buffers(data)

    def _fliter(self, cBuffer):
        return signal.lfilter(self.filter_config["b"],
                              self.filter_config["a"],
                              cBuffer)
