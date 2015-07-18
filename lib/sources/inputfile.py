from .source import Source
import json

class InputFile(Source):
    # TODO: configure encoding, e.g. json, or csv with specific template

    def __init__(self, file_path, **kwargs):
        super(InputFile, self).__init__(**kwargs)
        self.name = 'source:stdin'
        self.file_path = file_path
        self.open_file = open(self.file_path, 'r')
        self.config['loop'] = self.config.get('loop', True)
        self.bookmark = 0

    def start(self):
        self.streaming = True
        with self.open_file as f:
            for i in xrange(self.bookmark):
                f.next()
            for line in f:
                if self.streaming == False:
                    break
                data = json.loads(line)
                # TODO: interpret timestamp and throttle accordingly
                self._on_data(data)
                self.bookmark += 1

    def stop(self):
        self.streaming = False
