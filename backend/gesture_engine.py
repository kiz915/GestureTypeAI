"""
GestureType AI — Gesture Recognition Engine
Handles MediaPipe hand detection, OpenCV camera feed,
and gesture-to-action mapping.
"""

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import threading
import base64


class GestureEngine:
    """
    Core gesture recognition engine.
    Uses MediaPipe Hands for landmark detection.
    """

    MODES = ['typing', 'sign-language', 'pc-control']

    def __init__(self, mode='typing', camera_id=0):
        self.mode = mode
        self.camera_id = camera_id
        self.running = False
        self.cap = None
        self.thread = None

        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        # Callback registered via @engine.on_gesture
        self._gesture_callback = None

    def on_gesture(self, fn):
        """Decorator to register a gesture callback."""
        self._gesture_callback = fn
        return fn

    def _emit_gesture(self, gesture, confidence):
        if self._gesture_callback:
            self._gesture_callback(gesture, confidence)

    def start(self):
        """Start camera capture and recognition loop in a background thread."""
        self.cap = cv2.VideoCapture(self.camera_id)
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop recognition and release camera."""
        self.running = False
        if self.cap:
            self.cap.release()

    def get_frame_base64(self):
        """Capture a single frame and return it as a base64 JPEG string."""
        if not self.cap or not self.cap.isOpened():
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        return base64.b64encode(buffer).decode('utf-8')

    def _loop(self):
        """Main recognition loop (runs in background thread)."""
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    gesture, confidence = self._classify(hand_landmarks)
                    if gesture:
                        self._emit_gesture(gesture, confidence)

                        if self.mode == 'pc-control':
                            self._handle_pc_control(gesture)

    def _classify(self, landmarks):
        """
        Placeholder classifier — replace with your trained model.
        Returns (gesture_name, confidence_float) or (None, 0).
        """
        # TODO: Load and run TensorFlow/scikit-learn model here
        return None, 0.0

    def _handle_pc_control(self, gesture):
        """Map gestures to pyautogui PC control actions."""
        actions = {
            'swipe_right': lambda: pyautogui.hotkey('alt', 'right'),
            'swipe_left':  lambda: pyautogui.hotkey('alt', 'left'),
            'thumbs_up':   lambda: pyautogui.press('volumeup'),
            'thumbs_down': lambda: pyautogui.press('volumedown'),
            'open_palm':   lambda: pyautogui.hotkey('ctrl', 'space'),
        }
        action = actions.get(gesture)
        if action:
            action()
