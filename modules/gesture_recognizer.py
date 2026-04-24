import cv2
import mediapipe as mp
import numpy as np

class GestureRecognizer:
    """
    Detects hand gestures from an image and maps them to letters A-Z.
    Uses MediaPipe for hand landmark detection.
    """

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        # Finger tip landmark IDs in MediaPipe
        self.tip_ids = [4, 8, 12, 16, 20]

    def get_finger_states(self, landmarks):
        """
        Returns a list of 5 values — 1 if finger is up, 0 if down.
        Order: [Thumb, Index, Middle, Ring, Pinky]
        """
        fingers = []

        # Thumb — compare x position (left/right)
        if landmarks[self.tip_ids[0]].x < landmarks[self.tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other 4 fingers — compare y position (up/down)
        for i in range(1, 5):
            if landmarks[self.tip_ids[i]].y < landmarks[self.tip_ids[i] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def fingers_to_letter(self, fingers, landmarks):
        """
        Maps finger combinations to letters A-Z.
        fingers = [Thumb, Index, Middle, Ring, Pinky]
        """
        total = sum(fingers)

        # Basic gesture-to-letter mapping
        mapping = {
            (0, 0, 0, 0, 0): "BACKSPACE",   # Fist
            (0, 1, 0, 0, 0): "A",            # Index only
            (0, 1, 1, 0, 0): "B",            # Index + Middle
            (0, 1, 1, 1, 0): "C",            # 3 fingers
            (0, 1, 1, 1, 1): "D",            # 4 fingers (no thumb)
            (1, 1, 1, 1, 1): "SPACE",        # All fingers open
            (1, 0, 0, 0, 0): "E",            # Thumb only
            (1, 1, 0, 0, 0): "F",            # Thumb + Index
            (1, 0, 0, 0, 1): "G",            # Thumb + Pinky
            (0, 0, 0, 0, 1): "H",            # Pinky only
            (0, 1, 0, 0, 1): "I",            # Index + Pinky
            (1, 1, 1, 0, 0): "J",            # Thumb + Index + Middle
            (0, 0, 1, 0, 0): "K",            # Middle only
            (0, 0, 1, 1, 0): "L",            # Middle + Ring
            (0, 0, 0, 1, 0): "M",            # Ring only
            (0, 0, 0, 1, 1): "N",            # Ring + Pinky
            (1, 0, 1, 0, 0): "O",            # Thumb + Middle
            (1, 0, 0, 1, 0): "P",            # Thumb + Ring
            (1, 0, 1, 1, 0): "Q",            # Thumb + Middle + Ring
            (1, 1, 0, 1, 0): "R",            # Thumb + Index + Ring
            (1, 0, 0, 1, 1): "S",            # Thumb + Ring + Pinky
            (1, 1, 0, 0, 1): "T",            # Thumb + Index + Pinky
            (1, 0, 1, 0, 1): "U",            # Thumb + Middle + Pinky
            (0, 1, 0, 1, 0): "V",            # Index + Ring
            (1, 1, 0, 1, 1): "W",            # Thumb + Index + Ring + Pinky
            (1, 1, 1, 0, 1): "X",            # Thumb + Index + Middle + Pinky
            (0, 1, 1, 0, 1): "Y",            # Index + Middle + Pinky
            (1, 1, 1, 1, 0): "Z",            # All except Pinky
        }

        return mapping.get(tuple(fingers), "?")

    def predict(self, image_rgb):
        """
        Takes an RGB image, detects hand, returns (letter, annotated_image).
        """
        results = self.hands.process(image_rgb)
        annotated = image_rgb.copy()

        if not results.multi_hand_landmarks:
            return None, None

        hand_landmarks = results.multi_hand_landmarks[0]

        # Draw landmarks on image
        self.mp_draw.draw_landmarks(
            annotated,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
            self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
        )

        fingers = self.get_finger_states(hand_landmarks.landmark)
        letter = self.fingers_to_letter(fingers, hand_landmarks.landmark)

        # Draw letter on image
        h, w, _ = annotated.shape
        cv2.putText(annotated, f"Gesture: {letter}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (75, 0, 130), 3)

        return letter, annotated
