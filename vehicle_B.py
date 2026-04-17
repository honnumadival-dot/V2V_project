import socket

HOST = '127.0.0.1'
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Vehicle B Waiting for data...")

conn, addr = server.accept()

while True:
    data = conn.recv(1024).decode()
    if not data:
        break

    speed, distance = data.split(",")

    speed = int(speed)
    distance = int(distance)

    print("Received Speed:", speed)
    print("Received Distance:", distance)

    if distance < 20:
        print("🚨 HIGH ALERT")
    elif distance < 40:
        print("⚠️ MEDIUM ALERT")
    else:
        print("✅ SAFE")