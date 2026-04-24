import cv2
import mediapipe as mp
import numpy as np

# Try importing pyautogui — may not work in cloud environments
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception:
    PYAUTOGUI_AVAILABLE = False


class PCController:
    """
    Detects control gestures and maps them to PC actions.
    Falls back to logging if PyAutoGUI not available (e.g., Google Colab).
    """

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        self.tip_ids = [4, 8, 12, 16, 20]
        self.pip_ids = [3, 6, 10, 14, 18]

        # Gesture → Action mapping
        self.gesture_actions = {
            "FIST":        ("Copy",        self._copy),
            "PEACE":       ("Paste",       self._paste),
            "ONE_UP":      ("Scroll Up",   self._scroll_up),
            "ONE_DOWN":    ("Scroll Down", self._scroll_down),
            "OPEN_PALM":   ("Screenshot",  self._screenshot),
            "THUMB_UP":    ("Volume Up",   self._volume_up),
            "THUMB_DOWN":  ("Volume Down", self._volume_down),
        }

    def get_finger_states(self, landmarks):
        fingers = []
        fingers.append(1 if landmarks[self.tip_ids[0]].x < landmarks[self.tip_ids[0]-1].x else 0)
        for i in range(1, 5):
            fingers.append(1 if landmarks[self.tip_ids[i]].y < landmarks[self.pip_ids[i]].y else 0)
        return fingers

    def classify_control_gesture(self, fingers, landmarks):
        total = sum(fingers)
        # All closed = Fist
        if total == 0:
            return "FIST"
        # All open = Open Palm
        elif total == 5:
            return "OPEN_PALM"
        # Index + Middle = Peace
        elif fingers == [0, 1, 1, 0, 0]:
            return "PEACE"
        # Only index up pointing up
        elif fingers == [0, 1, 0, 0, 0] and landmarks[8].y < landmarks[5].y:
            return "ONE_UP"
        # Only index pointing down
        elif fingers == [0, 1, 0, 0, 0] and landmarks[8].y > landmarks[5].y:
            return "ONE_DOWN"
        # Thumb only up
        elif fingers == [1, 0, 0, 0, 0] and landmarks[4].y < landmarks[3].y:
            return "THUMB_UP"
        # Thumb only down
        elif fingers == [1, 0, 0, 0, 0] and landmarks[4].y > landmarks[3].y:
            return "THUMB_DOWN"
        return "UNKNOWN"

    # --- PC Actions ---
    def _copy(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('ctrl', 'c')
        return "Ctrl+C executed"

    def _paste(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('ctrl', 'v')
        return "Ctrl+V executed"

    def _scroll_up(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.scroll(3)
        return "Scrolled Up"

    def _scroll_down(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.scroll(-3)
        return "Scrolled Down"

    def _screenshot(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.screenshot('gesture_screenshot.png')
        return "Screenshot taken"

    def _volume_up(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('volumeup')
        return "Volume Up"

    def _volume_down(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('volumedown')
        return "Volume Down"

    def detect_and_execute(self, image_rgb):
        """
        Detect gesture in image and execute corresponding PC action.
        Returns (gesture_name, annotated_image, action_result)
        """
        results = self.hands.process(image_rgb)
        annotated = image_rgb.copy()

        if not results.multi_hand_landmarks:
            return None, None, None

        hand_landmarks = results.multi_hand_landmarks[0]
        self.mp_draw.draw_landmarks(
            annotated, hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
            self.mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2)
        )

        fingers = self.get_finger_states(hand_landmarks.landmark)
        gesture = self.classify_control_gesture(fingers, hand_landmarks.landmark)

        action_result = "No action"
        action_label = gesture

        if gesture in self.gesture_actions:
            action_label, action_fn = self.gesture_actions[gesture]
            action_result = action_fn()

        display = f"{gesture} → {action_label}"
        if not PYAUTOGUI_AVAILABLE:
            display += " (simulated)"

        cv2.putText(annotated, display, (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

        return action_label, annotated, action_result
