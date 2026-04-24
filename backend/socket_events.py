from flask_socketio import emit


def register_socket_events(socketio, gesture_engine):
    """Register all Socket.IO events."""

    # Register gesture callback ONLY ONCE
    @gesture_engine.on_gesture
    def forward_gesture(gesture, confidence):
        socketio.emit('gesture', {
            'gesture': gesture,
            'confidence': confidence
        })

    @socketio.on('connect')
    def on_connect():
        emit('status', {
            'connected': True,
            'message': 'Backend connected'
        })

    @socketio.on('disconnect')
    def on_disconnect():
        gesture_engine.stop()

    @socketio.on('start_camera')
    def on_start_camera(data=None):
        """Start gesture recognition."""
        mode = (data or {}).get('mode', 'typing')

        if gesture_engine.running:
            emit('status', {'message': 'Camera already running'})
            return

        gesture_engine.mode = mode
        gesture_engine.start()

        emit('camera_started', {'mode': mode})

    @socketio.on('stop_camera')
    def on_stop_camera():
        """Stop camera."""
        gesture_engine.stop()
        emit('camera_stopped', {})

    @socketio.on('request_frame')
    def on_request_frame():
        """Send one frame."""
        try:
            frame_b64 = gesture_engine.get_frame_base64()
            if frame_b64:
                emit('frame', {'image': frame_b64})
            else:
                emit('error', {'message': 'No frame available'})
        except Exception as e:
            emit('error', {'message': str(e)})

    @socketio.on('set_mode')
    def on_set_mode(data):
        """Change mode."""
        mode = data.get('mode', 'typing')

        if mode in gesture_engine.MODES:
            gesture_engine.mode = mode
            emit('mode_changed', {'mode': mode})
        else:
            emit('error', {'message': f'Unknown mode: {mode}'})
