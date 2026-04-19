import socket
import random
import time

host = "127.0.0.1"
port = 5000

client = socket.socket()
client.connect((host, port))

print("🚗 Vehicle B connected!")

while True:
    # Receive from A
    data = client.recv(1024).decode()
    print(f"\n📡 From Vehicle A: {data}")

    # Simulated data
    distance = random.randint(5, 100)
    speed = random.randint(20, 80)

    # Collision logic
    if distance < 20:
        alert = "DANGER 🚨"
    elif distance < 50:
        alert = "WARNING ⚠️"
    else:
        alert = "SAFE ✅"

    message = f"B | Dist:{distance} | Speed:{speed} | {alert}"
    client.send(message.encode())

    print(f"📤 Sent: {message}")
    print("----------------------")

    time.sleep(2)