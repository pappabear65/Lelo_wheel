import gc
import time

def check_memory_status():
    gc.collect()
    free_memory = gc.mem_free()
    allocated_memory = gc.mem_alloc()
    total_memory = free_memory + allocated_memory

    print(f"Free memory: {free_memory} bytes")
    print(f"Allocated memory: {allocated_memory} bytes")
    print(f"Total memory: {total_memory} bytes" + "\n")

while True:
    check_memory_status()
    time.sleep(30)  # Check memory status every 10 seconds