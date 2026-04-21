import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

clients = []

def broadcast(data, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(data)
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"🚗 Connected: {addr}")
    clients.append(conn)

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            broadcast(data, conn)
        except:
            break

    print(f"❌ Disconnected: {addr}")
    clients.remove(conn)
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("🚦 Server running...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()