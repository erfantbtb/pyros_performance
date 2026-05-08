
# Pyros Performance

A high-performance Python library for benchmarking and profiling your code. it can be used for both ros2 
functions and non-ros2 functions. project is part of the pyros library.

## Installation

```bash
pip install pyros-performance
```

## Quick Start

```python
from pyros_performance import profiler

@profiler(log_in_console=True, log_in_ros=False)
def sum_numbers(*args, **kwargs):
    total = 0

    for value in args:
        total += value

    for value in kwargs.values():
        total += value

    return total
```
## Example Output

```text
Function Name: sum_numbers
Time Taken: 0.000008 sec
Current Memory: 0.00 MB
Peak Memory: 0.00 MB
CPU Usage: 0.00%
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
