from .source import Source
import sys, json, select, tty, termios, threading, time

# THIS SOLUTION FOR NON-BLOCKING READ FROM STDIN WON'T WORK ON WINDOWS

# TODO: USE pygame OR msvcrt SHIM FOR CROSS PLATFORM SOLUTION

class StdIn(Source):

    def __init__(self, **kwargs):
        super(StdIn, self).__init__(**kwargs)
        self.name = 'source:stdin'
        self.streaming = False
        self.thread = threading.Thread(target=self._stdInListener)

    def start(self):
        self.streaming = True
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.streaming = False
        self.thread = threading.Thread(target=self._stdInListener)
        time.sleep(0.1)

    def _stdInListener(self):
        while self.streaming:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                line = sys.stdin.readline()
                if len(line) > 0:
                    try:
                        data = json.loads(line)
                    except Exception:
                        print "ERROR: couldn't parse: " + line
                    self._on_data(data)
