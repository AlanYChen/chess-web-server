import sys
import threading
import os
import shutil
import datetime

_LOGGING = True
LOGS_DIRECTORY_PATH = "logs"
OLD_THRESHOLD = 3

# Reset logs at start of the program
shutil.rmtree("logs")

def remove_old_log_files():
    cutoff_time = datetime.datetime.now() - datetime.timedelta(days=OLD_THRESHOLD)

    for filename in os.listdir(LOGS_DIRECTORY_PATH):
        file_path = os.path.join(LOGS_DIRECTORY_PATH, filename)
        if not os.path.isfile(file_path): continue

        modification_timestamp = os.path.getmtime(file_path)
        modification_datetime = datetime.datetime.fromtimestamp(modification_timestamp)

        if modification_datetime < cutoff_time:
            try:
                os.remove(file_path)
                print(f"Removed: {file_path}")
            except OSError as e:
                print(f"Error removing {file_path}: {e}")

def log(msg):
    if not _LOGGING:
        return
    
    # Write to file as well
    original_stdout = sys.stdout
    try:
        current_thread_name = threading.current_thread().name

        filename = LOGS_DIRECTORY_PATH + "/" + current_thread_name + "_log.txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "a") as f:
            sys.stdout = f
            print(msg)
    finally:
        sys.stdout = original_stdout

    remove_old_log_files()