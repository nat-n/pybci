from .output import Output

class OutputFile(Output):

    def __init__(self, file_path, **kwargs):
        super(OutputFile, self).__init__(**kwargs)
        self.name = 'output:file'
        self.file_path = file_path

    def _link(self, source):
        """
        Should only be called inside the register method of Source or Filter
        """
        super().link(self)
        self.open_file = open(self.file_path, 'w')

    def unlink(self):
        """
        Disconnect this Output from it's parent node
        """
        super().unlink(self)
        self.source = None
        self.open_file.close()

    def _on_data(self, data):
        self.open_file.write(json.dumps(data))
