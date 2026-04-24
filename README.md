# 🤚 GestureType AI

### ✨ Hand Gesture Based Typing System

**By Kishore | IT Engineering Student**

GestureType AI is a computer vision-based project that allows users to type letters using hand gestures. It uses AI-powered hand tracking to detect finger positions and convert them into text.

---

## 🚀 Features

* 🖐️ Detects 21 hand landmarks using MediaPipe
* ✌️ Identifies which fingers are up/down
* 🔤 Converts gestures into letters (A–Z mapping)
* 📷 Works with uploaded images
* 🧠 Simple rule-based gesture recognition
* 🧩 Modular and beginner-friendly code

---

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy
* Pillow
* Matplotlib
* Streamlit (for deployment)

---

## 📂 Project Structure

```
GestureTypeAI/
│── modules/
│   ├── gesture_recognizer.py
│   ├── sign_language.py
│
│── notebook/
│   └── GestureTypeAI.ipynb
│
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/GestureTypeAI.git
cd GestureTypeAI
pip install -r requirements.txt
```

---

## ▶️ How to Run

### 🔹 Option 1: Google Colab

1. Open the notebook
2. Run each cell step-by-step
3. Upload a hand gesture image

---

### 🔹 Option 2: Local Machine

```bash
python main.py
```

---

## 🖐️ How It Works

1. Image is captured/uploaded 📷
2. MediaPipe detects hand landmarks 🤖
3. Finger positions are analyzed ✌️
4. Pattern is matched with predefined gestures 🔤
5. Output letter is displayed

---

## 🔢 Example Gesture Mapping

| Finger State | Output    |
| ------------ | --------- |
| (0,1,0,0,0)  | A         |
| (0,1,1,0,0)  | B         |
| (0,1,1,1,0)  | C         |
| (1,1,1,1,1)  | SPACE     |
| (0,0,0,0,0)  | BACKSPACE |

---

## ⚠️ Limitations

* ❌ Limited gesture-to-letter mapping
* ❌ Works only on static images
* ❌ Thumb detection may vary (left/right hand issue)
* ❌ Not fully accurate in low lighting

---

## 💡 Future Improvements

* 🎥 Real-time webcam support
* 🧠 Machine Learning model for better accuracy
* 🔤 Full A–Z gesture support
* 🌐 Web app deployment using Streamlit
* 📱 Mobile app integration

---

## 🎓 Learning Outcomes

* Computer Vision basics
* Hand landmark detection
* Gesture recognition logic
* Python project structuring
* AI-based interaction systems

---

## 📌 Use Cases

* Assistive technology for disabled users
* Touchless typing systems
* Human-computer interaction projects
* Educational AI demos

---

## 📜 License

This project is open-source and free to use for educational purposes.

---

## 🙌 Acknowledgment

* MediaPipe by Google
* OpenCV community

---

## ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🍴 Fork it
* 📢 Share with others
