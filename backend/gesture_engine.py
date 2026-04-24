import cv2
import mediapipe as mp
import numpy as np
import threading
import base64
import os

# Disable pyautogui in server environments (no GUI support)
IS_SERVER = os.environ.get("RENDER") or os.environ.get("GITHUB") or os.environ.get("CI")

if not IS_SERVER:
    import pyautogui


class GestureEngine:
    """
    Core gesture recognition engine using MediaPipe Hands.
    Safe for both local and deployment environments.
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

        self._gesture_callback = None

    def on_gesture(self, fn):
        """Decorator to register a gesture callback."""
        self._gesture_callback = fn
        return fn

    def _emit_gesture(self, gesture, confidence):
        if self._gesture_callback:
            try:
                self._gesture_callback(gesture, confidence)
            except Exception as e:
                print("Callback error:", e)

    def start(self):
        """Start camera safely."""
        try:
            self.cap = cv2.VideoCapture(self.camera_id)

            if not self.cap.isOpened():
                print("❌ Camera not accessible (likely server environment)")
                return

            self.running = True
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()

        except Exception as e:
            print("❌ Error starting engine:", e)

    def stop(self):
        """Stop recognition and release camera."""
        self.running = False
        if self.cap:
            self.cap.release()

    def get_frame_base64(self):
        """Return current frame as base64 (for frontend display)."""
        if not self.cap or not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None

        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        return base64.b64encode(buffer).decode('utf-8')

    def _loop(self):
        """Main gesture recognition loop."""
        try:
            while self.running and self.cap and self.cap.isOpened():
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

        except Exception as e:
            print("❌ Loop error:", e)

    def _classify(self, landmarks):
        """
        Placeholder classifier.
        Replace with ML model.
        """
        return None, 0.0

    def _handle_pc_control(self, gesture):
        """Map gestures to system actions (only works locally)."""
        if IS_SERVER:
            return  # Skip on server

        actions = {
            'swipe_right': lambda: pyautogui.hotkey('alt', 'right'),
            'swipe_left':  lambda: pyautogui.hotkey('alt', 'left'),
            'thumbs_up':   lambda: pyautogui.press('volumeup'),
            'thumbs_down': lambda: pyautogui.press('volumedown'),
            'open_palm':   lambda: pyautogui.hotkey('ctrl', 'space'),
        }

        action = actions.get(gesture)
        if action:
            try:
                action()
            except Exception as e:
                print("PC control error:", e)
