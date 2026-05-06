import csv
import os
import time

file_exists = os.path.isfile("data/log.csv")

def log_event(data):
    with open("data/log.csv", "a", newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["time", "vehicle", "distance", "ttc", "risk"])

        writer.writerow([
            time.strftime("%H:%M:%S"),
            data["id"],
            data["distance"],
            data["ttc"],
            data["risk"]
        ])