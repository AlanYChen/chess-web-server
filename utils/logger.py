import sys
import threading

_LOGGING = True

def log(msg):
    if not _LOGGING:
        return
    
    print(msg)

    # Write to file as well
    original_stdout = sys.stdout
    try:
        current_thread_name = threading.current_thread().name

        with open("~/logs/" + current_thread_name + "_log.txt", "w") as f:
            sys.stdout = f
            print(msg)
    finally:
        sys.stdout = original_stdout