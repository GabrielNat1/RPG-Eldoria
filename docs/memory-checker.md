# Memory Check Utility (`memory_check.py`)

## 📌 Overview
`memory_check.py` provides tools for monitoring memory usage in Python applications.  
Originally designed for the **RPG Eldoria** project, it can be used in any Python program.  

It uses Python’s built-in **`tracemalloc`** library to track memory allocations and report the parts of the code consuming the most resources.

---

## ✨ Features
- 🔴 **Live Monitoring** – continuously tracks memory usage at runtime  
- 📸 **Snapshots** – capture and compare memory states  
- 🧩 **Detailed Tracebacks** – shows file, line number, and traceback of allocations  
- 📊 **Current & Peak Usage** – reports both current and peak memory in KiB  
- 🧪 **Demo Included** – a simple function to test memory tracking  

---

## 🚀 Usage

### Run the demo
```bash
python code/memory_check.py
```

### Enable live monitoring in your project
In `main.py`, import the monitor after your other imports:

```python
from memory_check import monitor_memory
import threading
```

Start the monitor before creating your `Game` instance:

```python
if __name__ == '__main__':
    threading.Thread(target=monitor_memory, args=(5,), daemon=True).start()
    game = Game()
    game.run()
```

This enables background memory monitoring while your game is running.

---

## 🔍 Example Output
```shell
Memory monitoring started...

[ Top 10 memory allocation locations ]

File: code/chunk_manager.py:104
  61.2 KiB allocated
  Traceback:
    File "code/chunk_manager.py", line 104

Current memory: 2061.1 KiB; Peak: 3198.6 KiB
----------------------------------------
```

---

## 🛠️ When to Use
- Detecting **memory leaks**  
- Profiling **memory hotspots**  
- Optimizing **resource management** in large projects  

---

## 📦 Requirements
- Python **3.4+**  
- No external dependencies (uses only the standard library)  

---

## 📝 Notes
- The monitor is **non-intrusive** and can safely run in the background  
- Best used during **gameplay** or **heavy resource loading phases**  
