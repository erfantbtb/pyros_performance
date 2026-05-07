import functools
import time
import tracemalloc


def performance_logger(
    save_path=None,
    save_format=None,
    log_in_console=True, 
    log_in_ros=False, 
    ):
    def decorator(func):
        """Decorator that logs execution time and memory usage of a function."""
        @functools.wraps(func) 
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            
            t0 = time.time()
            result = func(*args, **kwargs)
            t1 = time.time()
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            
            if log_in_console:
                print(f"Function Name: {func.__name__}")
                print(f"Arguments: args={args}, kwargs={kwargs}")
                print(f"Time Taken: {t1 - t0:.6f} seconds")
                print(f"Current Memory Usage: {current / 1024 / 1024:.2f} MB")
                print(f"Peak Memory Usage: {peak / 1024 / 1024:.2f} MB")
                print("*************************************************")
        
        return wrapper
    
    return decorator
