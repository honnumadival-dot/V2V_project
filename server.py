from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

vehicles = {}

@app.route('/')
def index():
    return render_template('index.html')

# ---------------- RECEIVE VEHICLE DATA ----------------
@socketio.on('vehicle_data')
def handle_data(data):
    vid = data['id']
    vehicles[vid] = data

    # broadcast to all clients
    emit('update', vehicles, broadcast=True)

# ---------------- RUN SERVER ----------------
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)