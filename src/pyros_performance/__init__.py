from .profiler import profiler, render
from importlib.metadata import version

__all__ = ["profiler", "render"]
__version__ = version("pyros-performance")