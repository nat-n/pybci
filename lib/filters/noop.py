from .filter import Filter


class Noop(Filter):
    _name = 'filter:noop'
    _default_config = {}

    def __init__(self, **kwargs):
        super(Noop, self).__init__(**kwargs)

    def _process(self, data):
        # do nothing!
        return data
