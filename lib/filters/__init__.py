from .filter import Filter
from .baseline import Baseline
from .noop import Noop
from .notch import Notch

FILTERS = {
  "baseline": Baseline,
  "notch": Notch,
  "noop": Noop
}