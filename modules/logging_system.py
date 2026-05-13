import csv
import os
import time

LOG_FILE = "data/log.csv"

def log_event(message):

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Time",
                "Message"
            ])

        writer.writerow([
            time.strftime("%H:%M:%S"),
            message
        ])