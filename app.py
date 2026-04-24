from flask import Flask, render_template
from flask_socketio import SocketIO
from backend.gesture_engine import GestureEngine
from backend.socket_events import register_socket_events
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gesturetype-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

gesture_engine = GestureEngine()
register_socket_events(socketio, gesture_engine)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
