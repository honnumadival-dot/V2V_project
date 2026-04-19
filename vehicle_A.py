import socket
import random
import time

host = "127.0.0.1"
port = 5000

server = socket.socket()
server.bind((host, port))
server.listen(1)

print("🚗 Vehicle A waiting for connection...")

conn, addr = server.accept()
print(f"Connected to {addr}")

while True:
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

    message = f"A | Dist:{distance} | Speed:{speed} | {alert}"
    conn.send(message.encode())

    # Receive from B
    data = conn.recv(1024).decode()
    print(f"\n📡 From Vehicle B: {data}")

    print(f"📤 Sent: {message}")
    print("----------------------")

    time.sleep(2)