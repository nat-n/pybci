import atexit, time, threading, sys
from .source import Source
import open_bci_v3 as bci

DEACTIVATE = ["1", "2", "3", "4", "5", "6", "7", "8",
              "q", "w", "e", "r", "t", "y", "u", "i"]
ACTIVATE = ["!", "@", "#", "$", "%", "^", "&", "*",
            "Q", "W", "E", "R", "T", "Y", "U", "I"]

class OpenBCI(Source):
    # TODO: attach other info from the board, e.g. status changes?

    _default_config = {
        'port': '/dev/tty.usbserial-DN0093NU',
        'active_channels': [0, 1, 2, 3, 4, 5, 6, 7],
        'timeout': -1
    }

    def __init__(self, **kwargs):
        super(OpenBCI, self).__init__(**kwargs)
        self.name = 'source:bciboard'
        # self.config['port'] = kwargs.get('port', "/dev/tty.usbserial-DN0093NU")
        # self.config['channels'] = kwargs.get('channels', [0,1,2,3,4,5,6,7])
        # self.config['timeout'] = kwargs.get('timeout', -1)

        # initialise the bci
        self.bci = bci.OpenBCIBoard(port=self.config['port'])
        # register callback to disconnect the bci on quit
        atexit.register(self._boardEndCallback)
        time.sleep(1)

        # init channels
        self._reset_channels()
        time.sleep(1)

        # Start streaming from device in a daemonised thread
        self.bciboard_thread = threading.Thread(target=self.bci.start_streaming,
                                                args=[self._on_sample,
                                                      self._boardEndCallback])#,
                                                      # self._boardTimeoutCallback,
                                                      # self.config['timeout']])
        self.bciboard_thread.daemon = True

    def start(self):
        self.streaming = True
        self.bciboard_thread.start()

    def stop(self):
        self.streaming = False
        self.bci.stop()

    def configure(self, cnfg):
        active_channels = self.config['channels']
        super(OpenBCI, self).configure(cnfg)
        if active_channels != self.config['channels']:
            self._reset_channels()

    def _on_sample(self, sample):
        self._on_data({
            "packet_id": sample.id,
            "channel_data": sample.channel_data,
            "aux_data": sample.aux_data,
        })

    def _reset_channels(self):
        # print ("resetting channels", self.config['channels'])
        # for i in range(16):
        #     # self.bci.ser.write(DEACTIVATE[i])
        #     self.bci.set_channel(i+1, 0)
        #     if i in self.config['channels']:
        #         sys.stderr.write(("activating %i" % i) + "\n")
        #         # self.bci.ser.write(ACTIVATE[i])
        pass

    def _boardEndCallback(self):
        self.bci.disconnect()

    def _boardTimeoutCallback(self):
        sys.stderr.write("*** BCI timed out. *** \n")
