# GOAL: maximum decoupling between websockets, other web services, data aquisition, etc

# Modules:
# - dashboard App (web pages etc)
# - streamer (stream over websockets)
# - recorder (stream to file/stdout)
# - playback (source from file/stdin)
# - sourcer (source from device)
# - processors? (filtering, FFT)
# ... and main which handles options and init etc

import os, sys, json, atexit, time
import lib.webservice as webservice
from lib.sources import SOURCES
from lib.filters import FILTERS
from lib.outputs import OUTPUTS

from tornado.options import options, define

# # example, none of the properties are required
# stream_object = {
#     "timestamp": 0,
#     "packet_id": 255,
#     "channel_data": [],
#     "frequencies": {},
#     "config": {},
#     "path": [],
# }

class Pipeline():
    # TODO: Allow nodes to be declared as only initialisable once in the pipeline
    # TODO: move this class out into lib

    def __init__(self, config):
        self.loop = self._default_loop
        self.config = config
        self.root = self.load_config(config)

    def log(self, msg):
        sys.stderr.write(str(msg) + "\n")

    def _default_loop(self):
        """This may be overridden during pipeline Initialization"""
        while True:
            time.sleep(10)

    def load_config(self, config):
        pipeline_name = config.keys()[0]
        pipeline_cnfg = config[pipeline_name]
        pipeline_root = self._init_pipeline_node(pipeline_cnfg)

        return pipeline_root

    def _init_pipeline_node(self, cnfg):
        args = []
        node_type, node_subtype = cnfg['type'].split(':')
        node_class = None
        if node_type == 'source':
            node_class = SOURCES[node_subtype]
        elif node_type == 'filter':
            node_class = FILTERS[node_subtype]
        elif node_type == 'output':
            node_class = OUTPUTS[node_subtype]

        self.log("Initialising node: " + node_class.__name__)

        if node_class.__name__ == 'WebSocketClients':
            # init WebSocket server and get clients list to pass in args
            self.loop = webservice.create(port=cnfg['config']['http-port'],
                                          dashboard=cnfg['config']['dashboard'])
            args.append(webservice.Links['clients'])
            new_node = node_class(*args, **cnfg['config'])
            webservice.Links['pipeline_node'] = new_node
        else:
            new_node = node_class(*args, **cnfg['config'])

        if node_type in ['source', 'filter']:
            for child in cnfg['children']:
                new_node.register(self._init_pipeline_node(child))
        return new_node


    def start(self):
        self.root.start()
        self.loop()


if __name__ == '__main__':
    define('config', default='config2.json', help="Pipeline config file", type=str) # TODO: document how to use this
    options.parse_command_line()

    DIRECTORY_ROOT = os.path.dirname(__file__)
    CONFIG_PATH = os.path.join(DIRECTORY_ROOT, options.config)
    with open(CONFIG_PATH) as config_file:
        CONFIG = json.load(config_file)

    pipeline = Pipeline(CONFIG)
    pipeline.start()
