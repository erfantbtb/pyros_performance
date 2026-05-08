from .profiler import profiler
from importlib.metadata import version

__all__ = ["profiler"]
__version__ = version("pyros-performance")