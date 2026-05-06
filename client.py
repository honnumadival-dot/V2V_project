import socketio
import time
import random

sio = socketio.Client()

sio.connect('http://localhost:5000')

vehicle_id = random.randint(1, 100)

distance = 100
speed = 30

while True:
    data = {
        "id": vehicle_id,
        "distance": distance,
        "speed": speed
    }

    sio.emit('vehicle_data', data)
    print("Sent:", data)

    distance -= random.randint(1, 3)
    time.sleep(1)