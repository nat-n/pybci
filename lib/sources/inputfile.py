from .source import Source
from time import time, sleep
from threading import Thread
import json

SAMPLE_RATE = 250;

# WARNING: in theory having the filepath configurable from unauthenticated
#          network clients is a major security issue! BE CAREFUL!
# FIXME: see above.

class InputFile(Source):
    # TODO: configure encoding, e.g. json, or csv with specific template

    packet_buffer = []

    def __init__(self, **kwargs):
        super(InputFile, self).__init__(**kwargs)
        self.name = 'source:stdin'
        self.config['file_path']
        self.config['loop'] = self.config.get('loop', True)
        self.bookmark = 0
        self.open_file = None

    def start(self):
        self.streaming = True
        self._loop_thread = Thread(target=self._loop)
        self._loop_thread.daemon = True # not sure about this...
        self._loop_thread.start()

    def _loop(self):
        prev_tick = int(time()*1000) % SAMPLE_RATE
        with self._get_file() as f:
            end_of_file = False
            for i in xrange(self.bookmark):
                try:
                    f.next()
                except StopIteration:
                    self.bookmark = 0
                    end_of_file = True
                    break
            if end_of_file:
                self.stop()
                if self.config['loop']:
                    return self.start()

            while self.streaming:
                sleep(0.0005)
                # Release as many samples as should have been released since the
                # last tick.
                this_tick = int(time()*1000) % SAMPLE_RATE
                for i in xrange(this_tick - prev_tick):
                    try:
                        line = f.next()
                    except StopIteration:
                        if self.config['loop']:
                            self.bookmark = 0
                            self.stop()
                            return self.start()
                        else:
                            self.stop()
                    sample = json.loads(line)
                    self._on_data(sample)
                    self.bookmark += 1
                prev_tick = this_tick

    def stop(self):
        self.open_file.close()
        self.open_file = None
        self.streaming = False

    def _get_file(self):
        if self.open_file is None or self.open_file.closed:
            self.open_file = open(self.config['file_path'], 'r')
        return self.open_file
