import time

def log_event(message):
    timestamp = time.strftime("%H:%M:%S")
    with open("v2v_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")