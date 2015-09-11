from ..sources import Source

class Output(object):

    _default_config = {}

    def __init__(self, **kwargs):
        self.config = dict(self._default_config)
        self.config.update(kwargs)
        self.name = 'output:unnamed'
        self.source = None

    def _link(self, source):
        """
        Should only be called inside the register method of Source or Filter
        """
        self.source = source

    def unlink():
        """
        Disconnect this Output from it's parent node
        """
        self.source._children.remove(self)
        self.source = None

    def configure(self, cnfg):
        self.config.update(cnfg)

    def _on_data(self, data):
        # to be implemented by subclass
        pass

    def path(self):
        path = [self.source]
        while not isinstance(path[-1], Source) and path[-1] is not None:
            path.append(path[-1].source)
        return path
