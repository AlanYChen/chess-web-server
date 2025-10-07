import sys
import threading
import os

_LOGGING = True

def log(msg):
    if not _LOGGING:
        return
    
    print(msg)

    # Write to file as well
    original_stdout = sys.stdout
    try:
        current_thread_name = threading.current_thread().name

        filename = "logs/" + current_thread_name + "_log.txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w") as f:
            sys.stdout = f
            print(msg)
    finally:
        sys.stdout = original_stdout