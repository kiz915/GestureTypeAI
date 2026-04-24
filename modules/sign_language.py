import cv2
import mediapipe as mp
import numpy as np

class SignLanguageDetector:
    """
    Detects ASL (American Sign Language) hand signs A-Z from images.
    Uses MediaPipe landmarks + rule-based classification.
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
        self.pip_ids = [3, 6, 10, 14, 18]  # Second joints

    def get_landmark_array(self, landmarks):
        """Convert landmarks to numpy array for easier math."""
        return np.array([[lm.x, lm.y, lm.z] for lm in landmarks])

    def get_finger_angles(self, lm_array):
        """Calculate bend angles for each finger."""
        angles = []
        finger_joints = [
            [1, 2, 4],    # Thumb
            [5, 6, 8],    # Index
            [9, 10, 12],  # Middle
            [13, 14, 16], # Ring
            [17, 18, 20], # Pinky
        ]
        for base, mid, tip in finger_joints:
            v1 = lm_array[mid] - lm_array[base]
            v2 = lm_array[tip] - lm_array[mid]
            cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
            angle = np.degrees(np.arccos(np.clip(cos_angle, -1, 1)))
            angles.append(angle)
        return angles

    def classify_asl(self, landmarks):
        """
        Rule-based ASL A-Z classification using finger states and angles.
        Returns detected letter.
        """
        lm = landmarks
        tip = self.tip_ids
        pip = self.pip_ids

        # Finger up/down states
        fingers = []
        # Thumb
        fingers.append(1 if lm[tip[0]].x < lm[tip[0]-1].x else 0)
        # Other fingers
        for i in range(1, 5):
            fingers.append(1 if lm[tip[i]].y < lm[pip[i]].y else 0)

        total_up = sum(fingers)

        # ASL Letter Rules
        # A - Fist with thumb on side
        if fingers == [1, 0, 0, 0, 0]:
            return "A"
        # B - Four fingers up, thumb tucked
        elif fingers == [0, 1, 1, 1, 1]:
            return "B"
        # C - Curved hand (all fingers slightly bent)
        elif total_up == 0 and lm[8].y < lm[5].y:
            return "C"
        # D - Index up, others curved with thumb
        elif fingers == [1, 1, 0, 0, 0]:
            return "D"
        # E - All fingers bent/curled
        elif total_up == 0:
            return "E"
        # F - Index and thumb touching, others up
        elif fingers == [0, 0, 1, 1, 1]:
            return "F"
        # G - Index pointing sideways, thumb out
        elif fingers == [1, 1, 0, 0, 0] and lm[8].x > lm[5].x:
            return "G"
        # H - Index and middle pointing sideways
        elif fingers == [0, 1, 1, 0, 0]:
            return "H"
        # I - Pinky only up
        elif fingers == [0, 0, 0, 0, 1]:
            return "I"
        # K - Index and middle up, thumb out
        elif fingers == [1, 1, 1, 0, 0]:
            return "K"
        # L - L shape - thumb and index up
        elif fingers == [1, 1, 0, 0, 0] and lm[4].y < lm[3].y:
            return "L"
        # M - Three fingers over thumb
        elif fingers == [0, 1, 1, 1, 0]:
            return "M"
        # N - Two fingers over thumb
        elif fingers == [0, 1, 1, 0, 0] and lm[8].y > lm[6].y:
            return "N"
        # O - All fingers curved to make O
        elif total_up == 0 and abs(lm[4].x - lm[8].x) < 0.05:
            return "O"
        # P - Index pointing down, middle out
        elif fingers == [1, 1, 1, 0, 0] and lm[8].y > lm[5].y:
            return "P"
        # R - Index and middle crossed
        elif fingers == [0, 1, 1, 0, 0] and abs(lm[8].x - lm[12].x) < 0.03:
            return "R"
        # S - Fist with thumb over fingers
        elif total_up == 0 and lm[4].x > lm[8].x:
            return "S"
        # T - Thumb between index and middle
        elif fingers == [0, 0, 0, 0, 0] and lm[4].y < lm[8].y:
            return "T"
        # U - Index and middle up together
        elif fingers == [0, 1, 1, 0, 0] and abs(lm[8].x - lm[12].x) < 0.04:
            return "U"
        # V - Index and middle up apart (peace sign)
        elif fingers == [0, 1, 1, 0, 0] and abs(lm[8].x - lm[12].x) > 0.04:
            return "V"
        # W - Three fingers up
        elif fingers == [0, 1, 1, 1, 0]:
            return "W"
        # X - Index finger hooked/bent
        elif fingers == [0, 0, 0, 0, 0] and lm[8].y < lm[7].y:
            return "X"
        # Y - Thumb and pinky out
        elif fingers == [1, 0, 0, 0, 1]:
            return "Y"
        # Z - Index pointing, draw Z (simplified to index up)
        elif fingers == [0, 1, 0, 0, 0]:
            return "Z"
        # J - Pinky up (simplified)
        elif fingers == [0, 0, 0, 0, 1] and lm[20].x < lm[17].x:
            return "J"
        # SPACE - Open palm
        elif total_up == 5:
            return "SPACE"
        else:
            return "?"

    def detect(self, image_rgb):
        """
        Takes an RGB image, detects ASL sign, returns (letter, annotated_image).
        """
        results = self.hands.process(image_rgb)
        annotated = image_rgb.copy()

        if not results.multi_hand_landmarks:
            return None, None

        hand_landmarks = results.multi_hand_landmarks[0]

        # Draw landmarks
        mp.solutions.drawing_utils.draw_landmarks(
            annotated,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            mp.solutions.drawing_utils.DrawingSpec(color=(255, 165, 0), thickness=2, circle_radius=4),
            mp.solutions.drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=2)
        )

        letter = self.classify_asl(hand_landmarks.landmark)

        cv2.putText(annotated, f"ASL: {letter}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 69, 0), 3)

        return letter, annotated
