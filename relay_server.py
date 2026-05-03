import socket
import threading
import json

HOST = "0.0.0.0"
PORT = 5000

clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("🚗 V2V Relay Server Running...")

def broadcast(data, sender):
    msg = json.dumps(data).encode()
    for c in clients:
        if c != sender:
            try:
                c.send(msg)
            except:
                pass

def handle(client):
    while True:
        try:
            data = json.loads(client.recv(1024).decode())
            broadcast(data, client)
        except:
            clients.remove(client)
            break

while True:
    c, addr = server.accept()
    clients.append(c)
    print("Connected:", addr)
    threading.Thread(target=handle, args=(c,), daemon=True).start()