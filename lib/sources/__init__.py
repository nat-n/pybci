from .source import Source
from .inputfile import InputFile
from .openbci import OpenBCI
from .stdin import StdIn

SOURCES = {
  "inputfile": InputFile,
  "bciboard": OpenBCI,
  "stdin": StdIn,
}
