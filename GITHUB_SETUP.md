# 🤚 GestureType AI

> **Type letters, convert sign language to text, and control your PC — all using just hand gestures and a camera.**

Built with Python, MediaPipe, OpenCV & Streamlit | By Kishore | IT Engineering Student

---

## 🎯 What This Project Does

| Feature | Description |
|---|---|
| ✍️ **Gesture Typing** | Show hand gestures to type A-Z letters |
| 🧏 **Sign Language to Text** | ASL hand signs detected and converted to text |
| 🖥️ **PC Control** | Gestures trigger Copy, Paste, Scroll, Screenshot |

---

## 🛠️ Tech Stack

- **Python 3.11** — Core language
- **MediaPipe** — Google's AI for 21-point hand landmark detection
- **OpenCV** — Image processing and camera feed
- **scikit-learn** — ML classifier for gestures
- **PyAutoGUI** — PC control automation
- **Streamlit** — Web UI

---

## 📁 Project Structure

```
GestureTypeAI/
│
├── app.py                    ← Main Streamlit app (run this)
├── requirements.txt          ← All dependencies
├── GestureTypeAI_Colab.ipynb ← Google Colab learning notebook
│
├── modules/
│   ├── __init__.py
│   ├── gesture_recognizer.py ← A-Z gesture typing logic
│   ├── sign_language.py      ← ASL sign language detector
│   ├── pc_controller.py      ← PC control via gestures
│   └── virtual_keyboard.py   ← Text tracking and keyboard state
│
├── dataset/                  ← Store your gesture training images here
├── models/                   ← Saved ML models go here
├── utils/                    ← Helper functions
└── assets/                   ← Images and demo files
```

---

## 🚀 How to Run

### Option 1: Google Colab (Recommended for beginners)
1. Open `GestureTypeAI_Colab.ipynb` in Google Colab
2. Run each cell step by step
3. Upload hand gesture images to test

### Option 2: Local Machine
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/GestureTypeAI.git
cd GestureTypeAI

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Option 3: Streamlit Cloud (Live deployment)
1. Push this repo to GitHub
2. Go to share.streamlit.io
3. Connect your GitHub repo
4. Deploy for free!

---

## 🤚 Gesture Guide

### Typing Mode (A-Z)
| Gesture | Letter |
|---|---|
| ☝️ Index finger only | A |
| ✌️ Index + Middle | B |
| 🤟 3 fingers | C |
| 🖖 4 fingers | D |
| 🖐️ Open palm (all 5) | SPACE |
| ✊ Fist (all closed) | BACKSPACE |

### PC Control Mode
| Gesture | Action |
|---|---|
| ✊ Fist | Copy (Ctrl+C) |
| ✌️ Peace sign | Paste (Ctrl+V) |
| ☝️ Index up | Scroll Up |
| 🖐️ Open palm | Screenshot |
| 👍 Thumb up | Volume Up |

---

## 📊 How It Works

```
📷 Camera/Image Input
        ↓
🤖 MediaPipe Hand Detection
        ↓
📍 21 Landmark Points Extracted
        ↓
✌️ Finger State Analysis
(Which fingers are up/down?)
        ↓
🔤 Gesture Classification
(Map to Letter / Command)
        ↓
⌨️ Output: Type / Control / Sign
```

---

## 🏆 Skills Demonstrated

- ✅ Computer Vision with OpenCV
- ✅ AI/ML with MediaPipe & scikit-learn
- ✅ Python OOP (classes and modules)
- ✅ Real-world problem solving
- ✅ Web deployment with Streamlit
- ✅ GitHub version control

---

## 📈 Future Improvements

- [ ] Live webcam real-time detection
- [ ] Custom gesture training (record your own)
- [ ] Mobile app version
- [ ] Telugu/Tamil sign language support
- [ ] Voice output for sign language

---

## 👨‍💻 About

Built during summer vacation as a learning project.
**Kishore** | IT Engineering — 1st Year | Tamil Nadu, India

*This project was built to learn Python, Computer Vision, and AI/ML from scratch in 30 days.*

---

## 📄 License
MIT License — Free to use and modify
