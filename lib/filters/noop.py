from .filter import Filter


class Noop(Filter):
    def _process(self, data):
        # do nothing!
        return data
