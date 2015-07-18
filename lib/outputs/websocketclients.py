from .output import Output

class WebSocketClients(Output):

    def __init__(self, clients_list, **kwargs):
        Output.__init__(self, **kwargs)
        self.name = 'output:websockets'
        self.clients_list = clients_list

    def _on_data(self, data):
        for c in self.clients_list:
            c.write_message(data)

    def _on_message(self, data):
        # route config from client to appropriate node in path
        path = self.path()

        print ([n.name for n in path], data, data.get('config', {}))

        for name in data.get('config', {}):
            for node in path:
                print [node.name, name, node.name == name]
                if node.name == name:
                    node.configure(data['config'][name])
