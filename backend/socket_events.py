"""
GestureType AI — Socket.IO Event Handlers
Bridges the Flask-SocketIO server with the GestureEngine.
Matches the events expected by static/js/socket-backend.js
"""

from flask_socketio import emit


def register_socket_events(socketio, gesture_engine):
    """Register all Socket.IO events on the given socketio instance."""

    @socketio.on('connect')
    def on_connect():
        emit('status', {'connected': True, 'message': 'Backend connected'})

    @socketio.on('disconnect')
    def on_disconnect():
        gesture_engine.stop()

    @socketio.on('start_camera')
    def on_start_camera(data=None):
        """Client requests camera + gesture recognition to start."""
        mode = (data or {}).get('mode', 'typing')
        gesture_engine.mode = mode
        gesture_engine.start()

        # Wire up gesture callback to emit events back to this client
        @gesture_engine.on_gesture
        def forward_gesture(gesture, confidence):
            socketio.emit('gesture', {'gesture': gesture, 'confidence': confidence})

        emit('camera_started', {'mode': mode})

    @socketio.on('stop_camera')
    def on_stop_camera():
        """Client requests camera to stop."""
        gesture_engine.stop()
        emit('camera_stopped', {})

    @socketio.on('request_frame')
    def on_request_frame():
        """Client requests a single JPEG frame for preview."""
        frame_b64 = gesture_engine.get_frame_base64()
        if frame_b64:
            emit('frame', {'image': frame_b64})

    @socketio.on('set_mode')
    def on_set_mode(data):
        """Switch gesture recognition mode."""
        mode = data.get('mode', 'typing')
        if mode in gesture_engine.MODES:
            gesture_engine.mode = mode
            emit('mode_changed', {'mode': mode})
        else:
            emit('error', {'message': f'Unknown mode: {mode}'})
