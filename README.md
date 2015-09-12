Python package for various streaming tasks with OpenBCI data.

The default config serves a webpage which graphs the data coming from the OpenBCI.

## Features
  - JSON configured streaming pipeline
  - Connection to an OpenBCI board
  - Save and playback of streamed data from disk or STDIO
  - Streaming over web sockets for web based visualisation
  - Baseline correction filter
  - 50hz or 60hz Notch filter

TODO:
  - Bandpass filters
  - FFT analysis
  - control UI
  - user control for scale adjustment
  - improve error handing and exception recovery accross threads
