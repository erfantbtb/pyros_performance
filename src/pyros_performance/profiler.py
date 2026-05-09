import time
import threading
import functools
import psutil
from collections import defaultdict, deque


process = psutil.Process()

class Stats:
    def __init__(self, maxlen=100):
        self.wall = deque(maxlen=maxlen)
        self.cpu = deque(maxlen=maxlen)
        self.count = 0
        self.last_wall = 0.0
        self.last_cpu = 0.0

    def update(self, wall, cpu):
        self.wall.append(wall)
        self.cpu.append(cpu)
        self.count += 1
        self.last_wall = wall
        self.last_cpu = cpu

    def avg_wall(self):
        return sum(self.wall) / len(self.wall) if self.wall else 0

    def avg_cpu(self):
        return sum(self.cpu) / len(self.cpu) if self.cpu else 0


class ProfilerCore:
    def __init__(self):
        self.functions = defaultdict(Stats)
        self.lock = threading.Lock()

        self.cpu_per_core = []
        self.total_cpu = 0.0
        self.rss_mem = 0.0

        self.running = True

    def record(self, name, wall, cpu):
        with self.lock:
            self.functions[name].update(wall, cpu)

    def sample_system(self):
        while self.running:
            self.cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
            self.total_cpu = psutil.cpu_percent(interval=None)
            self.rss_mem = process.memory_info().rss / (1024 * 1024)
            time.sleep(0.5)

    def start(self):
        t = threading.Thread(target=self.sample_system, daemon=True)
        t.start()


profiler_core = ProfilerCore()
profiler_core.start()

def profiler(log_in_console=True):

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            t0 = time.perf_counter()
            cpu_before = process.cpu_times()

            try:
                result = func(*args, **kwargs)
            finally:
                t1 = time.perf_counter()
                cpu_after = process.cpu_times()

                wall = t1 - t0
                cpu = (cpu_after.user - cpu_before.user) + \
                      (cpu_after.system - cpu_before.system)

                profiler_core.record(func.__name__, wall, cpu)

            return result

        return wrapper

    return decorator

# ================================
# DASHBOARD RENDERER
# ================================

def clear():
    print("\033[H\033[J", end="")

def render():

    while True:
        clear()

        print("=" * 60)
        print("           ROS2 LIGHTWEIGHT PROFILER")
        print("=" * 60)

        # SYSTEM
        print("\nSYSTEM")
        print("-" * 60)
        print(f"CPU Total: {profiler_core.total_cpu:.1f}%")
        print(f"Memory RSS: {profiler_core.rss_mem:.2f} MB")

        print("\nPer-Core CPU:")
        for i, c in enumerate(profiler_core.cpu_per_core):
            bar = "█" * int(c // 5)
            print(f"Core {i:02d}: {bar:<20} {c:.1f}%")

        # FUNCTIONS
        print("\nFUNCTIONS")
        print("-" * 60)

        with profiler_core.lock:
            for name, s in profiler_core.functions.items():

                print(f"\n{name}")
                print(f"  calls     : {s.count}")
                print(f"  wall avg  : {s.avg_wall()*1000:.3f} ms")
                print(f"  cpu avg   : {s.avg_cpu()*1000:.3f} ms")
                print(f"  last wall : {s.last_wall*1000:.3f} ms")
                print(f"  last cpu  : {s.last_cpu*1000:.3f} ms")

        print("\n" + "=" * 60)

        time.sleep(0.5)

