import tracemalloc
import time

def monitor_memory(interval=5, top_n=10):
    print("Memory monitoring started...")
    tracemalloc.start()
    try:
        while True:
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('traceback')

            print("\n[ Top {} memory allocation locations ]".format(top_n))
            count = 0
            for stat in top_stats:
                for frame in stat.traceback:
                    if "rpgeldoria" in frame.filename:
                        print(f"\nFile: {frame.filename}:{frame.lineno}")
                        print(f"  {stat.size / 1024:.1f} KiB allocated")
                        print("  Traceback:")
                        for tb_frame in stat.traceback.format():
                            print("    " + tb_frame)
                        count += 1
                        break
                if count >= top_n:
                    break

            current, peak = tracemalloc.get_traced_memory()
            print(f"Current memory: {current / 1024:.1f} KiB; Peak: {peak / 1024:.1f} KiB")
            print("-" * 40)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Memory monitoring stopped.")
    finally:
        tracemalloc.stop()

def memory_usage_demo():
    print("Starting memory usage demo...")
    tracemalloc.start()
    
    data = [i ** 2 for i in range(10000)]
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)

    current, peak = tracemalloc.get_traced_memory()
    print(f"Memory usage: {current / 1024:.1f} KiB; Peak: {peak / 1024:.1f} KiB")

    tracemalloc.stop()

if __name__ == "__main__":
    memory_usage_demo()
