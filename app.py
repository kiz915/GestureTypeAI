import streamlit as st
import cv2
import numpy as np
from PIL import Image
import mediapipe as mp
import pickle
import os
from modules.gesture_recognizer import GestureRecognizer
from modules.sign_language import SignLanguageDetector
from modules.pc_controller import PCController
from modules.virtual_keyboard import VirtualKeyboard

st.set_page_config(
    page_title="GestureType AI",
    page_icon="🤚",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: 700; color: #4F46E5; text-align: center; }
    .subtitle { font-size: 1.1rem; color: #6B7280; text-align: center; margin-bottom: 2rem; }
    .result-box { background: #F0FDF4; border: 2px solid #22C55E; border-radius: 12px; padding: 1rem; text-align: center; font-size: 2rem; font-weight: 700; color: #16A34A; }
    .typed-text { background: #EEF2FF; border: 2px solid #6366F1; border-radius: 12px; padding: 1rem; font-size: 1.2rem; color: #3730A3; min-height: 60px; }
    .info-box { background: #FFF7ED; border: 1px solid #FB923C; border-radius: 8px; padding: 0.75rem; font-size: 0.9rem; color: #9A3412; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤚 GestureType AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Type, Sign & Control your PC using Hand Gestures</div>', unsafe_allow_html=True)

# Sidebar
mode = st.sidebar.selectbox("Select Mode", [
    "✍️ Gesture Typing (A-Z)",
    "🧏 Sign Language to Text",
    "🖥️ PC Control Mode"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤚 Gesture Guide")
if "Typing" in mode:
    st.sidebar.markdown("""
    - ☝️ Index up = A
    - ✌️ Two fingers = B  
    - 🤟 Three fingers = C
    - 🖖 Four fingers = D
    - 🖐️ Open palm = Space
    - ✊ Fist = Backspace
    """)
elif "Sign" in mode:
    st.sidebar.markdown("""
    - Uses ASL (American Sign Language)
    - Show gesture clearly to camera
    - Hold for 1 second for detection
    """)
else:
    st.sidebar.markdown("""
    - ✊ Fist = Copy (Ctrl+C)
    - ✌️ Peace = Paste (Ctrl+V)
    - ☝️ One finger up = Scroll Up
    - 👇 One finger down = Scroll Down
    - 🖐️ Open palm = Screenshot
    """)

# Initialize session state
if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""
if "last_gesture" not in st.session_state:
    st.session_state.last_gesture = ""

# Main content
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📷 Upload Image or Use Camera")
    input_method = st.radio("Input Method", ["Upload Image", "Take Photo"], horizontal=True)

    uploaded_image = None
    if input_method == "Upload Image":
        uploaded_file = st.file_uploader("Upload hand gesture image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    else:
        camera_image = st.camera_input("Take a photo of your hand gesture")
        if camera_image:
            uploaded_image = Image.open(camera_image)

    if uploaded_image and st.button("🔍 Detect Gesture", type="primary", use_container_width=True):
        img_array = np.array(uploaded_image.convert("RGB"))

        recognizer = GestureRecognizer()
        sign_detector = SignLanguageDetector()
        pc_controller = PCController()

        with st.spinner("Analyzing gesture..."):
            if "Typing" in mode:
                result, annotated = recognizer.predict(img_array)
                if result:
                    if result == "SPACE":
                        st.session_state.typed_text += " "
                    elif result == "BACKSPACE":
                        st.session_state.typed_text = st.session_state.typed_text[:-1]
                    else:
                        st.session_state.typed_text += result
                    st.session_state.last_gesture = result

            elif "Sign" in mode:
                result, annotated = sign_detector.detect(img_array)
                if result:
                    st.session_state.typed_text += result
                    st.session_state.last_gesture = result

            else:
                result, annotated, action = pc_controller.detect_and_execute(img_array)
                st.session_state.last_gesture = result

            if annotated is not None:
                st.image(annotated, caption="Detected Landmarks", use_column_width=True)

with col2:
    st.subheader("🎯 Detection Result")

    if st.session_state.last_gesture:
        st.markdown(f'<div class="result-box">{st.session_state.last_gesture}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-box" style="color:#9CA3AF; background:#F9FAFB; border-color:#E5E7EB;">No gesture yet</div>', unsafe_allow_html=True)

    st.markdown("---")

    if "Typing" in mode or "Sign" in mode:
        st.subheader("📝 Typed Text")
        st.markdown(f'<div class="typed-text">{st.session_state.typed_text if st.session_state.typed_text else "Start gesturing to type..."}</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🗑️ Clear Text", use_container_width=True):
                st.session_state.typed_text = ""
                st.session_state.last_gesture = ""
                st.rerun()
        with col_b:
            if st.button("📋 Copy Text", use_container_width=True):
                st.code(st.session_state.typed_text)

    else:
        st.subheader("🖥️ PC Control Log")
        st.markdown('<div class="info-box">⚠️ PC Control mode executes real keyboard/mouse actions. Use carefully!</div>', unsafe_allow_html=True)
        if st.session_state.last_gesture:
            st.success(f"Last action: {st.session_state.last_gesture}")

    st.markdown("---")
    st.subheader("📊 Hand Landmarks")
    st.markdown("""
    MediaPipe detects **21 landmarks** on your hand:
    - 🔵 Wrist (point 0)
    - 🟢 Finger tips (4,8,12,16,20)
    - 🟡 Knuckles & joints
    """)

st.markdown("---")
st.markdown("**GestureType AI** | Built with Python, MediaPipe, OpenCV & Streamlit | by Kishore")

