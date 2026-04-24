# GestureType AI

Convert hand gestures to text, control your PC, and type A–Z using AI-powered sign language recognition.

## Project Structure

```
gesturetype-ai/
├── app.py                        # Flask entry point
├── requirements.txt
├── README.md
├── templates/
│   └── index.html                # Main page (Jinja2)
├── static/
│   ├── css/
│   │   └── styles.css            # All styles
│   └── js/
│       ├── main.js               # UI logic (theme, tabs, animations)
│       └── socket-backend.js     # Socket.IO ↔ backend bridge
└── backend/
    ├── __init__.py
    ├── gesture_engine.py         # MediaPipe + OpenCV + pyautogui
    └── socket_events.py          # Flask-SocketIO event handlers
```

## Setup

```bash
# 1. Clone
git clone https://github.com/yourusername/gesturetype-ai.git
cd gesturetype-ai

# 2. Virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py
# Open http://localhost:5000
```

## Usage Modes

| Mode | Command |
|------|---------|
| Typing (A–Z) | `python app.py` then select Typing mode in the UI |
| Sign Language | Select Sign Language mode in the UI |
| PC Control | Select PC Control mode in the UI |

## Custom Gesture Training

```bash
python collect_data.py --gesture "thumbs_up" --samples 200
python train.py --epochs 50 --model custom_gestures
python evaluate.py --model custom_gestures
```

## API

```python
from backend.gesture_engine import GestureEngine

engine = GestureEngine(mode="typing", camera_id=0)

@engine.on_gesture
def on_gesture(gesture, confidence):
    print(f"Detected: {gesture} ({confidence:.0%})")

engine.start()
```
