{
 "nbformat": 4,
 "nbformat_minor": 0,
 "metadata": {
  "colab": { "provenance": [], "name": "GestureTypeAI.ipynb" },
  "kernelspec": { "name": "python3", "display_name": "Python 3" }
 },
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🤚 GestureType AI — Google Colab Notebook\n",
    "### By Kishore | IT Engineering Student\n",
    "This notebook teaches you every concept used in the project, step by step.\n",
    "Run each cell one by one and understand what's happening."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["## 📦 Step 1: Install all required libraries"]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "# Install all libraries needed for GestureType AI\n",
    "!pip install opencv-python mediapipe streamlit Pillow scikit-learn pyautogui -q\n",
    "print('✅ All libraries installed successfully!')"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["## 📚 Step 2: Import Libraries and Understand What Each Does"]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "import cv2                          # OpenCV: for reading and processing images\n",
    "import mediapipe as mp              # MediaPipe: Google's AI for hand detection\n",
    "import numpy as np                  # NumPy: for math operations on arrays\n",
    "from PIL import Image               # Pillow: for opening image files\n",
    "import matplotlib.pyplot as plt     # For displaying images in Colab\n",
    "\n",
    "print('✅ All imports successful!')\n",
    "print(f'OpenCV version: {cv2.__version__}')\n",
    "print(f'MediaPipe version: {mp.__version__}')"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 🖐️ Step 3: Understand Hand Landmarks\n",
    "MediaPipe detects 21 specific points on your hand called **landmarks**.\n",
    "Each landmark has an x, y, z coordinate.\n",
    "- Point 0 = Wrist\n",
    "- Points 1-4 = Thumb (tip is point 4)\n",
    "- Points 5-8 = Index finger (tip is point 8)\n",
    "- Points 9-12 = Middle finger (tip is point 12)\n",
    "- Points 13-16 = Ring finger (tip is point 16)\n",
    "- Points 17-20 = Pinky (tip is point 20)"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "# Let's initialize MediaPipe hands\n",
    "mp_hands = mp.solutions.hands\n",
    "mp_draw = mp.solutions.drawing_utils\n",
    "\n",
    "# Create hand detector\n",
    "# static_image_mode=True means we process one image at a time (not video)\n",
    "# min_detection_confidence=0.7 means 70% sure there's a hand before detecting\n",
    "hands_detector = mp_hands.Hands(\n",
    "    static_image_mode=True,\n",
    "    max_num_hands=1,\n",
    "    min_detection_confidence=0.7\n",
    ")\n",
    "\n",
    "print('✅ MediaPipe hand detector ready!')\n",
    "print('Finger tip landmark IDs: Thumb=4, Index=8, Middle=12, Ring=16, Pinky=20')"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["## 📷 Step 4: Upload a Hand Gesture Image and Detect Landmarks"]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "from google.colab import files\n",
    "\n",
    "# Upload your hand gesture image\n",
    "print('Please upload a clear image of your hand gesture:')\n",
    "uploaded = files.upload()\n",
    "filename = list(uploaded.keys())[0]\n",
    "print(f'✅ Uploaded: {filename}')"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "# Load and process the image\n",
    "image = cv2.imread(filename)\n",
    "image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB\n",
    "\n",
    "# Process with MediaPipe\n",
    "results = hands_detector.process(image_rgb)\n",
    "\n",
    "if results.multi_hand_landmarks:\n",
    "    print(f'✅ Hand detected! Found {len(results.multi_hand_landmarks)} hand(s)')\n",
    "    hand = results.multi_hand_landmarks[0]\n",
    "    print(f'Total landmarks detected: {len(hand.landmark)}')\n",
    "    print(f'Wrist position: x={hand.landmark[0].x:.3f}, y={hand.landmark[0].y:.3f}')\n",
    "    print(f'Index fingertip: x={hand.landmark[8].x:.3f}, y={hand.landmark[8].y:.3f}')\n",
    "else:\n",
    "    print('❌ No hand detected. Try a clearer image with good lighting.')"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "# Draw the landmarks on the image and display\n",
    "annotated = image_rgb.copy()\n",
    "\n",
    "if results.multi_hand_landmarks:\n",
    "    for hand_landmarks in results.multi_hand_landmarks:\n",
    "        mp_draw.draw_landmarks(\n",
    "            annotated,\n",
    "            hand_landmarks,\n",
    "            mp_hands.HAND_CONNECTIONS,\n",
    "            mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),\n",
    "            mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)\n",
    "        )\n",
    "\n",
    "plt.figure(figsize=(10, 8))\n",
    "plt.subplot(1, 2, 1)\n",
    "plt.imshow(image_rgb)\n",
    "plt.title('Original Image')\n",
    "plt.axis('off')\n",
    "\n",
    "plt.subplot(1, 2, 2)\n",
    "plt.imshow(annotated)\n",
    "plt.title('Hand Landmarks Detected')\n",
    "plt.axis('off')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "print('✅ Landmarks drawn on image!')"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["## ✌️ Step 5: Detect Which Fingers Are Up"]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "def get_finger_states(landmarks):\n",
    "    \"\"\"\n",
    "    Returns list of 5 values: 1 = finger up, 0 = finger down\n",
    "    Order: [Thumb, Index, Middle, Ring, Pinky]\n",
    "    \"\"\"\n",
    "    tip_ids = [4, 8, 12, 16, 20]   # Fingertip landmark IDs\n",
    "    fingers = []\n",
    "\n",
    "    # Thumb: compare x positions (left-right movement)\n",
    "    if landmarks[tip_ids[0]].x < landmarks[tip_ids[0] - 1].x:\n",
    "        fingers.append(1)  # Thumb is up/out\n",
    "    else:\n",
    "        fingers.append(0)  # Thumb is in\n",
    "\n",
    "    # Other 4 fingers: compare y positions (up-down movement)\n",
    "    # Remember: in image coordinates, smaller y = higher up on screen\n",
    "    for i in range(1, 5):\n",
    "        if landmarks[tip_ids[i]].y < landmarks[tip_ids[i] - 2].y:\n",
    "            fingers.append(1)  # Finger tip is above its base = finger is up\n",
    "        else:\n",
    "            fingers.append(0)  # Finger is down/closed\n",
    "\n",
    "    return fingers\n",
    "\n",
    "if results.multi_hand_landmarks:\n",
    "    hand = results.multi_hand_landmarks[0]\n",
    "    fingers = get_finger_states(hand.landmark)\n",
    "    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']\n",
    "\n",
    "    print('🖐️ Finger States:')\n",
    "    for name, state in zip(finger_names, fingers):\n",
    "        status = '☝️ UP' if state == 1 else '✊ DOWN'\n",
    "        print(f'  {name}: {status}')\n",
    "    print(f'\\nTotal fingers up: {sum(fingers)}')\n",
    "    print(f'Finger state array: {fingers}')"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["## 🔤 Step 6: Map Finger States to Letters A-Z"]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "def fingers_to_letter(fingers):\n",
    "    \"\"\"Maps finger combination to a letter.\"\"\"\n",
    "    gesture_map = {\n",
    "        (0, 0, 0, 0, 0): 'BACKSPACE',  # Fist\n",
    "        (0, 1, 0, 0, 0): 'A',           # Index only\n",
    "        (0, 1, 1, 0, 0): 'B',           # Index + Middle\n",
    "        (0, 1, 1, 1, 0): 'C',           # 3 fingers\n",
    "        (0, 1, 1, 1, 1): 'D',           # 4 fingers\n",
    "        (1, 1, 1, 1, 1): 'SPACE',       # Open palm\n",
    "        (1, 0, 0, 0, 0): 'E',           # Thumb only\n",
    "        (1, 1, 0, 0, 0): 'F',           # Thumb + Index\n",
    "        (1, 0, 0, 0, 1): 'G',           # Thumb + Pinky\n",
    "        (0, 0, 0, 0, 1): 'H',           # Pinky only\n",
    "        (0, 1, 0, 0, 1): 'I',           # Index + Pinky\n",
    "        (1, 0, 0, 0, 1): 'Y',           # Thumb + Pinky (Shaka)\n",
    "    }\n",
    "    return gesture_map.get(tuple(fingers), '?')\n",
    "\n",
    "if results.multi_hand_landmarks:\n",
    "    letter = fingers_to_letter(fingers)\n",
    "    print(f'🔤 Detected gesture maps to: \"{letter}\"')\n",
    "\n",
    "    # Add letter label to image\n",
    "    labeled = annotated.copy()\n",
    "    cv2.putText(labeled, f'Letter: {letter}', (30, 80),\n",
    "                cv2.FONT_HERSHEY_SIMPLEX, 2, (75, 0, 130), 4)\n",
    "\n",
    "    plt.figure(figsize=(6, 6))\n",
    "    plt.imshow(labeled)\n",
    "    plt.title(f'Detected: {letter}', fontsize=16)\n",
    "    plt.axis('off')\n",
    "    plt.show()"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["## 🚀 Step 7: Full GestureType AI Pipeline (All modules together)"]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "# Clone the full project from GitHub\n",
    "!git clone https://github.com/YOUR_USERNAME/GestureTypeAI.git\n",
    "%cd GestureTypeAI\n",
    "!pip install -r requirements.txt -q\n",
    "print('✅ Project cloned and dependencies installed!')"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "# Test the full GestureRecognizer module\n",
    "import sys\n",
    "sys.path.insert(0, '/content/GestureTypeAI')\n",
    "\n",
    "from modules.gesture_recognizer import GestureRecognizer\n",
    "from modules.sign_language import SignLanguageDetector\n",
    "\n",
    "# Initialize recognizers\n",
    "recognizer = GestureRecognizer()\n",
    "sign_detector = SignLanguageDetector()\n",
    "\n",
    "print('✅ All modules loaded!')\n",
    "print('Now upload your gesture image to test the full pipeline:')"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "from google.colab import files\n",
    "import numpy as np\n",
    "from PIL import Image\n",
    "\n",
    "uploaded = files.upload()\n",
    "fname = list(uploaded.keys())[0]\n",
    "\n",
    "img = Image.open(fname).convert('RGB')\n",
    "img_array = np.array(img)\n",
    "\n",
    "# Test Gesture Typing\n",
    "letter, annotated_img = recognizer.predict(img_array)\n",
    "print(f'\\n🔤 Gesture Typing Result: {letter}')\n",
    "\n",
    "# Test Sign Language\n",
    "sign, annotated_sign = sign_detector.detect(img_array)\n",
    "print(f'🧏 Sign Language Result: {sign}')\n",
    "\n",
    "if annotated_img is not None:\n",
    "    plt.figure(figsize=(12, 5))\n",
    "    plt.subplot(1, 2, 1)\n",
    "    plt.imshow(annotated_img)\n",
    "    plt.title(f'Gesture Typing: {letter}')\n",
    "    plt.axis('off')\n",
    "    plt.subplot(1, 2, 2)\n",
    "    plt.imshow(annotated_sign if annotated_sign is not None else img_array)\n",
    "    plt.title(f'Sign Language: {sign}')\n",
    "    plt.axis('off')\n",
    "    plt.tight_layout()\n",
    "    plt.show()"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 🎉 Congratulations!\n",
    "You've built GestureType AI. Here's what you learned:\n",
    "- ✅ Python fundamentals (functions, lists, dicts)\n",
    "- ✅ OpenCV for image processing\n",
    "- ✅ MediaPipe for AI hand detection\n",
    "- ✅ Building a gesture-to-letter mapping\n",
    "- ✅ Modular project structure\n",
    "- ✅ Google Colab workflow\n",
    "\n",
    "**Next steps:**\n",
    "1. Push this to GitHub\n",
    "2. Deploy on Streamlit Cloud\n",
    "3. Add this to your resume and internship applications\n",
    "4. Submit to hackathons!"
   ]
  }
 ]
}
