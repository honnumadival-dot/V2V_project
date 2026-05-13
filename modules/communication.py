import socket
import json
from config import UDP_IP, UDP_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))

sock.setblocking(False)

ports = [5005, 5006, 5007]

def send(data):

    message = json.dumps(data).encode()

    for port in ports:

        if port != UDP_PORT:
            sock.sendto(message, (UDP_IP, port))

def receive():

    try:
        data, addr = sock.recvfrom(1024)
        return json.loads(data.decode())

    except:
        return None