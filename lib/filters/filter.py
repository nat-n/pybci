
class Filter(object):
    name = 'filter:unnamed'
    _default_config = {}

    def __init__(self, **kwargs):
        self._children = []
        self.config = dict(self._default_config)
        self.config.update(kwargs)

    def register(self, new_child):
        new_child._link(self)
        self._children.append(new_child)

    def _link(self, source):
        """
        Should only be called inside the register method of Source or Filter
        """
        self.source = source

    def unlink(self):
        """
        Disconnect this Filter from it's parent node
        """
        self.source._children.remove(self)
        self.source = None

    def configure(self, cnfg):
        self.config.update(cnfg)

    def _on_data(self, data):
        result = self._process(data)
        for c in self._children:
            c._on_data(result)

    def path(self):
        path = [self.source]
        while not isinstance(path[-1], Source) and path[-1] is not None:
            path.append(path[-1].source)
        return path

    def _process(self, data):
        # to be implemented by subclass
        return data