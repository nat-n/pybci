
class Source(object):

    _default_config = {}

    def __init__(self, **kwargs):
        self._children = []
        self.config = dict(self._default_config)
        self.config.update(kwargs)
        self.name = 'source:unnamed'
        self.streaming = False

    def register(self, new_child):
        new_child._link(self)
        self._children.append(new_child)

    def configure(self, cnfg):
        self.config.update(cnfg)

    def _on_data(self, data):
        for c in self._children:
            c._on_data(data)

    def start(self):
        # to be overriden by subclass
        pass

    def stop(self):
        # to be overriden by subclass
        pass