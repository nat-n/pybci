from .output import Output
import sys, json

class StdOut(Output):
    # TODO: configure encoding, e.g. json, or csv with specific template

    def __init__(self, **kwargs):
        super(StdOut, self).__init__(**kwargs)
        self.name = 'output:stdout'

    def _on_data(self, data):
        sys.stdout.write(json.dumps(data) + "\n")
