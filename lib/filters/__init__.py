from .filter import Filter
from .baseline import Baseline
from .noop import Noop

FILTERS = {
  "baseline": Baseline,
  "noop": Noop
}