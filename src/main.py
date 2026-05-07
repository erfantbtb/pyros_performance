import functools
import time
import tracemalloc
import psutil


process = psutil.Process()

def func_performance(
    log_in_console=True,
    log_in_ros=False,
    ):
    
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            ros_logger = None

            if log_in_ros and len(args) > 0:
                obj = args[0]
                if hasattr(obj, "get_logger"):
                    ros_logger = obj.get_logger()

            tracemalloc.start()
            t0 = time.time()

            try:
                result = func(*args, **kwargs)

            except Exception as e:
                if ros_logger:
                    ros_logger.error(
                        f"Error in function '{func.__name__}': {str(e)}"
                    )
                else:
                    print(f"Error in function '{func.__name__}': {str(e)}")

                tracemalloc.stop()
                raise

            t1 = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            cpu = process.cpu_percent()
            

            msg = (
                f"\nFunction Name: {func.__name__}\n"
                f"Time Taken: {t1 - t0:.6f} sec\n"
                f"Current Memory: {current / 1024 / 1024:.2f} MB\n"
                f"Peak Memory: {peak / 1024 / 1024:.2f} MB\n"
                f"CPU Usage: {cpu:.2f}%\n"
            )
            
            if len(args) > 0 and hasattr(args[0], "get_name"):
                msg += f"Node Name: {args[0].get_name()}\n"
                msg += f"----------------------------------- \n"

            if log_in_console:
                print(msg)

            if ros_logger and log_in_ros:
                ros_logger.info(msg)
                

            return result

        return wrapper

    return decorator


from rclpy.node import Node
class TestNode(Node):
    def __init__(self):
        super().__init__("test_node")
        
    @func_performance(log_in_ros=True)
    def callback(self):
        x = [i for i in range(100000)] 
        
        
if __name__ == "__main__": 
    import rclpy
    rclpy.init()
    node = TestNode()
    node.callback()
    rclpy.shutdown()
