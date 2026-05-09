
# Pyros Performance

A high-performance Python library for benchmarking and profiling your code. it can be used for both ros2 
functions and non-ros2 functions. project is part of the pyros library.

## Installation

```bash
pip install pyros-performance
```

## Quick Start

```python
from pyros_performance import profiler, render
import threading

@profiler()
def sum_numbers(*args):
    total = 0
    for _ in range(200000):
        for v in args:
            total += v
        total *= 1
    return total


@profiler()
def heavy_math():
    x = 0
    for i in range(300000):
        x += i * 0.5
        x = x % 100000
    return x

if __name__ == "__main__":

    # start dashboard thread
    t = threading.Thread(target=render, daemon=True)
    t.start()

    # simulate workload
    while True:
        sum_numbers(1, 2, 3)
        heavy_math()
        time.sleep(0.2)
```
## Example Output

```text
============================================================
           ROS2 LIGHTWEIGHT PROFILER
============================================================

SYSTEM
------------------------------------------------------------
CPU Total: 6.9%
Memory RSS: 13.31 MB

Per-Core CPU:
Core 00:                      2.0%
Core 01:                      4.0%
Core 02: ██                   11.8%
Core 03:                      2.0%
Core 04: █                    6.1%
Core 05: ██                   13.7%
Core 06: ██████               31.4%
Core 07:                      0.0%
Core 08: █                    6.0%
Core 09: █                    6.0%
Core 10:                      0.0%
Core 11:                      4.0%
Core 12:                      4.0%
Core 13: █                    5.9%
Core 14: █                    6.0%
Core 15:                      3.9%

FUNCTIONS
------------------------------------------------------------

sum_numbers
  calls     : 5
  wall avg  : 15.630 ms
  cpu avg   : 16.000 ms
  last wall : 14.789 ms
  last cpu  : 20.000 ms

heavy_math
  calls     : 5
  wall avg  : 13.479 ms
  cpu avg   : 12.000 ms
  last wall : 12.910 ms
  last cpu  : 10.000 ms

============================================================

```
## Features

- **Easy benchmarking** - Simple API for measuring execution time
- **Memory profiling** - Track memory usage during execution
- **Performance reports** - Generate detailed performance metrics
- **Low overhead** - Minimal impact on your code performance

## Documentation

For detailed documentation, visit [GitHub](https://github.com/erfantbtb/pyros_performance).

## Requirements

- Python 3.8+

## License

MIT

## Contributing

Contributions welcome! Please submit pull requests or issues on GitHub.
