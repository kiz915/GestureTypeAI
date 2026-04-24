"""
GestureType AI — Flask Application Entry Point
Run: python app.py
Then open http://localhost:5000
"""

from flask import Flask, render_template
from flask_socketio import SocketIO
from backend.gesture_engine import GestureEngine
from backend.socket_events import register_socket_events

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gesturetype-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize gesture engine
gesture_engine = GestureEngine()

# Register all Socket.IO events
register_socket_events(socketio, gesture_engine)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
