import time
import threading
from config import VEHICLE_ID, SEND_INTERVAL
import communication as comm

print(f"🚗 Vehicle {VEHICLE_ID} STARTED")

def sender():
    counter = 0
    while True:
        data = {
            "id": VEHICLE_ID,
            "distance": 50 + counter,
            "speed": 30
        }

        comm.send(data)
        print(f"[TX] Sent: {data}")

        counter += 1
        time.sleep(SEND_INTERVAL)

def receiver():
    while True:
        msg = comm.receive()
        if msg and msg["id"] != VEHICLE_ID:
            print(f"[RX] From Vehicle {msg['id']}: {msg}")

        time.sleep(0.1)

threading.Thread(target=sender, daemon=True).start()
threading.Thread(target=receiver, daemon=True).start()

while True:
    pass