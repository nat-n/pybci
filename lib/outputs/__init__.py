from .output import Output
from .outputfile import OutputFile
from .stdout import StdOut
from .websocketclients import WebSocketClients

OUTPUTS = {
  "outputfile": OutputFile,
  "stdout": StdOut,
  "websockets": WebSocketClients,
}