// ============================================================
//  GestureType AI — Main JavaScript
// ============================================================

/* ---- Theme Toggle ---- */
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

function setTheme(theme) {
  html.setAttribute('data-theme', theme);
  localStorage.setItem('gt-theme', theme);
}

themeToggle.addEventListener('click', () => {
  const current = html.getAttribute('data-theme');
  setTheme(current === 'dark' ? 'light' : 'dark');
});

// Load saved theme
const savedTheme = localStorage.getItem('gt-theme') || 'dark';
setTheme(savedTheme);

/* ---- Navbar Scroll ---- */
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 30);
});

/* ---- Mobile Menu ---- */
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');

hamburger.addEventListener('click', () => {
  mobileMenu.classList.toggle('open');
});

mobileMenu.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => mobileMenu.classList.remove('open'));
});

/* ---- Hero Hand Animation ---- */
const heroHands = [
  { emoji: '🤟', label: 'ASL — "I Love You"', output: 'I ❤ U', conf: 97 },
  { emoji: '✋', label: 'ASL — "Hello"', output: 'HELLO', conf: 95 },
  { emoji: '👊', label: 'Gesture — "Caps Lock"', output: '[CAPS]', conf: 93 },
  { emoji: '✌', label: 'Gesture — "Space"', output: '[ SPACE ]', conf: 98 },
  { emoji: '👌', label: 'Gesture — "OK / Copy"', output: '[COPY]', conf: 96 },
  { emoji: '🤙', label: 'Gesture — "Backspace"', output: '[⌫]', conf: 94 },
];
let heroIdx = 0;

function cycleHeroHand() {
  heroIdx = (heroIdx + 1) % heroHands.length;
  const h = heroHands[heroIdx];
  const emojiEl = document.querySelector('.hand-emoji');
  const labelEl = document.querySelector('.hand-label');
  const outputEl = document.getElementById('heroOutput');
  const barEl = document.getElementById('heroBar');
  const confEl = document.getElementById('heroConf');

  emojiEl.style.transform = 'scale(0.7) rotate(-10deg)';
  emojiEl.style.opacity = '0';
  setTimeout(() => {
    emojiEl.textContent = h.emoji;
    labelEl.textContent = h.label;
    outputEl.textContent = h.output;
    barEl.style.width = h.conf + '%';
    confEl.textContent = h.conf + '%';
    emojiEl.style.transform = 'scale(1) rotate(0deg)';
    emojiEl.style.opacity = '1';
    emojiEl.style.transition = 'all 0.5s cubic-bezier(0.34,1.56,0.64,1)';
  }, 200);
}

setInterval(cycleHeroHand, 2800);
// Animate bar on load
setTimeout(() => {
  document.getElementById('heroBar').style.width = '97%';
}, 600);

/* ---- Alphabet Grid (Simulator) ---- */
const aslEmojis = {
  A:'🤜', B:'✋', C:'🤌', D:'☝', E:'✊', F:'👌', G:'👉', H:'👉',
  I:'🤙', J:'🤙', K:'✌', L:'🤙', M:'✊', N:'✊', O:'🫳', P:'✌',
  Q:'👇', R:'✌', S:'✊', T:'✊', U:'✌', V:'✌', W:'🖖', X:'☝',
  Y:'🤙', Z:'☝'
};

const alphaGrid = document.getElementById('alphaGrid');
const outputArea = document.getElementById('outputArea');
const bigLetter = document.getElementById('bigLetter');
const demoBar = document.getElementById('demoBar');
const demoConf = document.getElementById('demoConf');

let outputText = '';

function updateOutput() {
  outputArea.innerHTML = outputText
    ? `<span style="font-size:1.1rem">${outputText}</span>`
    : `<span class="output-placeholder">Your typed text will appear here...</span>`;
}

'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach(letter => {
  const key = document.createElement('div');
  key.className = 'alpha-key';
  key.innerHTML = `<span class="key-emoji">${aslEmojis[letter] || '🤚'}</span><span class="key-letter">${letter}</span>`;
  key.addEventListener('click', () => {
    // Animate
    document.querySelectorAll('.alpha-key').forEach(k => k.classList.remove('active'));
    key.classList.add('active');
    setTimeout(() => key.classList.remove('active'), 400);

    // Update output
    outputText += letter;
    updateOutput();

    // Update big letter + confidence
    bigLetter.textContent = letter;
    bigLetter.style.transform = 'scale(1.4)';
    setTimeout(() => { bigLetter.style.transform = 'scale(1)'; bigLetter.style.transition = 'transform 0.3s cubic-bezier(0.34,1.56,0.64,1)'; }, 50);

    const conf = 88 + Math.floor(Math.random() * 11);
    demoBar.style.width = conf + '%';
    demoConf.textContent = conf + '%';
  });
  alphaGrid.appendChild(key);
});

/* ---- Output Buttons ---- */
document.getElementById('copyOutput').addEventListener('click', () => {
  if (outputText) {
    navigator.clipboard.writeText(outputText);
    showToast('Copied to clipboard!');
  }
});

document.getElementById('clearOutput').addEventListener('click', () => {
  outputText = '';
  updateOutput();
  bigLetter.textContent = '—';
  demoBar.style.width = '0%';
  demoConf.textContent = '—';
});

document.getElementById('speakOutput').addEventListener('click', () => {
  if (outputText && window.speechSynthesis) {
    const utt = new SpeechSynthesisUtterance(outputText);
    window.speechSynthesis.speak(utt);
  }
});

/* ---- Copy Code Buttons ---- */
document.querySelectorAll('.copy-code').forEach(btn => {
  btn.addEventListener('click', () => {
    const pre = btn.closest('.code-block').querySelector('pre');
    navigator.clipboard.writeText(pre.textContent.trim());
    btn.textContent = '✓ Copied';
    setTimeout(() => { btn.textContent = 'Copy'; }, 1800);
  });
});

/* ---- Camera Toggle ---- */
const camToggle = document.getElementById('camToggle');
const camBtnText = document.getElementById('camBtnText');
const camBtnIcon = camToggle.querySelector('.cam-btn-icon');
const video = document.getElementById('webcamVideo');
const cameraPlaceholder = document.getElementById('cameraPlaceholder');
const cameraHud = document.getElementById('cameraHud');
const detectedGesture = document.getElementById('detectedGesture');
let cameraStream = null;
let cameraOn = false;
let fpsInterval = null;
let facingMode = 'user';

// Simulated gestures for demo
const demoGestures = ['✊ — A', '✋ — B', '🤌 — C', '☝ — D', '✊ — E', '✌ — V', '🤙 — L', '👌 — OK'];
let gestureSimInterval = null;

camToggle.addEventListener('click', async () => {
  if (!cameraOn) {
    try {
      cameraStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode } });
      video.srcObject = cameraStream;
      video.style.display = 'block';
      cameraPlaceholder.style.display = 'none';
      cameraHud.style.display = 'flex';

      cameraOn = true;
      camBtnText.textContent = 'Disable Camera';
      camBtnIcon.textContent = '🔴';

      // Simulate FPS
      let fps = 28;
      fpsInterval = setInterval(() => {
        fps = 27 + Math.floor(Math.random() * 5);
        document.getElementById('hudFps').textContent = fps + ' FPS';
      }, 800);

      // Simulate gesture detection
      gestureSimInterval = setInterval(() => {
        const g = demoGestures[Math.floor(Math.random() * demoGestures.length)];
        detectedGesture.textContent = g;
      }, 1800);

      showToast('Camera enabled');
    } catch (err) {
      showToast('Camera access denied. Please allow camera permission.', 'error');
    }
  } else {
    if (cameraStream) {
      cameraStream.getTracks().forEach(t => t.stop());
      cameraStream = null;
    }
    video.style.display = 'none';
    cameraPlaceholder.style.display = 'flex';
    cameraHud.style.display = 'none';
    cameraOn = false;
    camBtnText.textContent = 'Enable Camera';
    camBtnIcon.textContent = '📷';
    clearInterval(fpsInterval);
    clearInterval(gestureSimInterval);
    detectedGesture.textContent = '—';
    showToast('Camera disabled');
  }
});

// Flip camera
document.getElementById('camFlip').addEventListener('click', async () => {
  if (cameraOn) {
    facingMode = facingMode === 'user' ? 'environment' : 'user';
    cameraStream?.getTracks().forEach(t => t.stop());
    try {
      cameraStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode } });
      video.srcObject = cameraStream;
    } catch (e) { /* no environment camera */ }
  }
});

// Snapshot
document.getElementById('camSnapshot').addEventListener('click', () => {
  if (!cameraOn) { showToast('Enable camera first', 'error'); return; }
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  const link = document.createElement('a');
  link.href = canvas.toDataURL('image/png');
  link.download = 'gesture-snapshot.png';
  link.click();
  showToast('Snapshot saved!');
});

/* ---- Mode Tabs ---- */
document.querySelectorAll('.mode-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.mode-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    showToast(`Switched to ${tab.dataset.mode} mode`);
  });
});

/* ---- Gesture Grid ---- */
const gestureData = [
  // Alphabet
  ...('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map((l, i) => ({
    emoji: aslEmojis[l] || '🤚', letter: l, name: 'ASL Letter', cat: 'alpha'
  }))),
  // PC Control
  { emoji: '✌', letter: 'SPC', name: 'Space', cat: 'control' },
  { emoji: '👆', letter: '↵', name: 'Enter', cat: 'control' },
  { emoji: '🤙', letter: '⌫', name: 'Backspace', cat: 'control' },
  { emoji: '👊', letter: 'CAP', name: 'Caps Lock', cat: 'control' },
  { emoji: '🖐', letter: '⏹', name: 'Stop', cat: 'control' },
  { emoji: '👌', letter: '⎘', name: 'Copy', cat: 'control' },
  { emoji: '🤏', letter: '📋', name: 'Paste', cat: 'control' },
  { emoji: '🖖', letter: '↑', name: 'Scroll Up', cat: 'control' },
  { emoji: '👇', letter: '↓', name: 'Scroll Down', cat: 'control' },
  // Special
  { emoji: '🤞', letter: '⌘C', name: 'Copy All', cat: 'special' },
  { emoji: '🫳', letter: '⌘V', name: 'Paste', cat: 'special' },
  { emoji: '🫲', letter: '←', name: 'Left', cat: 'special' },
  { emoji: '🫱', letter: '→', name: 'Right', cat: 'special' },
];

const gestureGrid = document.getElementById('gestureGrid');
const gestureSearch = document.getElementById('gestureSearch');
const gestureFilter = document.getElementById('gestureFilter');

function renderGestures(data) {
  gestureGrid.innerHTML = '';
  data.forEach(g => {
    const item = document.createElement('div');
    item.className = 'gesture-item';
    item.innerHTML = `
      <div class="g-emoji">${g.emoji}</div>
      <div class="g-letter">${g.letter}</div>
      <div class="g-name">${g.name}</div>
      <span class="gesture-cat-badge cat-${g.cat}">${g.cat}</span>
    `;
    item.addEventListener('click', () => {
      if (g.cat === 'alpha') {
        outputText += g.letter;
        updateOutput();
        bigLetter.textContent = g.letter;
        showToast(`Typed: ${g.letter}`);
      } else {
        showToast(`Gesture: ${g.name}`);
      }
    });
    gestureGrid.appendChild(item);
  });
}

function filterGestures() {
  const q = gestureSearch.value.toLowerCase();
  const cat = gestureFilter.value;
  const filtered = gestureData.filter(g => {
    const matchQ = g.letter.toLowerCase().includes(q) || g.name.toLowerCase().includes(q);
    const matchCat = cat === 'all' || g.cat === cat;
    return matchQ && matchCat;
  });
  renderGestures(filtered);
}

gestureSearch.addEventListener('input', filterGestures);
gestureFilter.addEventListener('change', filterGestures);
renderGestures(gestureData);

/* ---- Docs Tabs ---- */
document.querySelectorAll('.doc-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.doc-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.doc-panel').forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById('doc-' + tab.dataset.doc).classList.add('active');
  });
});

/* ---- Chatbot ---- */
const chatbotFab = document.getElementById('chatbotFab');
const chatbotWindow = document.getElementById('chatbotWindow');
const chatbotClose = document.getElementById('chatbotClose');
const chatInput = document.getElementById('chatInput');
const chatSend = document.getElementById('chatSend');
const chatMessages = document.getElementById('chatbotMessages');
const fabBadge = document.getElementById('fabBadge');
const chatSuggestions = document.getElementById('chatbotSuggestions');

const botKnowledge = {
  "camera": "To enable the camera, click the 📷 Enable Camera button in the Live Demo section. Your browser will ask for camera permission — just allow it! The system will then start detecting your hand gestures in real-time.",
  "install": "To install GestureType AI:\n1. Clone the repo: `git clone https://github.com/yourusername/gesturetype-ai.git`\n2. Create a virtual environment: `python -m venv venv`\n3. Install dependencies: `pip install -r requirements.txt`\n4. Run: `python main.py`",
  "letter": "Each letter A–Z is mapped to an ASL (American Sign Language) hand gesture. Click the 'Gestures' section or use the simulator in the demo to see each letter's gesture. You can also train custom gestures!",
  "sign": "Sign Language mode converts ASL hand signs to text in real-time. It recognizes full signs and words, not just individual letters. Enable the camera and switch to 'Sign Language' mode in the demo.",
  "pc control": "PC Control mode lets you control your computer with gestures:\n- ✌ Peace sign → Space\n- 👇 Point down → Scroll down\n- 🖖 Vulcan → Scroll up\n- 👌 OK → Copy\n- 🤏 Pinch → Paste",
  "accuracy": "GestureType AI achieves ~96–98% accuracy on standard ASL gestures under good lighting. Accuracy improves with custom training on your specific hand shape and camera setup.",
  "training": "You can train custom gestures using:\n`python collect_data.py --gesture my_gesture --samples 200`\nThen: `python train.py --model custom`\nThis lets you add any gesture you want!",
  "default": "Great question! GestureType AI uses MediaPipe for hand landmark detection and TensorFlow for gesture classification. You can ask me about: camera setup, letter gestures, sign language mode, PC control, installation, or custom training!"
};

function getBotReply(text) {
  const t = text.toLowerCase();
  if (t.includes('camera') || t.includes('webcam') || t.includes('enable')) return botKnowledge.camera;
  if (t.includes('install') || t.includes('setup') || t.includes('download')) return botKnowledge.install;
  if (t.includes('letter') || t.includes('type') || t.includes('alphabet') || t.includes('a-z')) return botKnowledge.letter;
  if (t.includes('sign') || t.includes('asl') || t.includes('language')) return botKnowledge.sign;
  if (t.includes('pc') || t.includes('control') || t.includes('scroll') || t.includes('copy') || t.includes('paste')) return botKnowledge["pc control"];
  if (t.includes('accurac')) return botKnowledge.accuracy;
  if (t.includes('train') || t.includes('custom')) return botKnowledge.training;
  return botKnowledge.default;
}

function addMessage(text, role = 'bot') {
  const msgDiv = document.createElement('div');
  msgDiv.className = role === 'bot' ? 'bot-message' : 'user-message';

  if (role === 'bot') {
    msgDiv.innerHTML = `
      <div class="bot-avatar">✦</div>
      <div class="message-bubble">${text.replace(/\n/g, '<br>')}</div>
    `;
  } else {
    msgDiv.innerHTML = `<div class="message-bubble">${text}</div>`;
  }
  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
  const div = document.createElement('div');
  div.className = 'bot-message typing-indicator';
  div.id = 'typingIndicator';
  div.innerHTML = `
    <div class="bot-avatar">✦</div>
    <div class="message-bubble">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>
  `;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTyping() {
  document.getElementById('typingIndicator')?.remove();
}

function sendChat(text) {
  if (!text.trim()) return;
  addMessage(text, 'user');
  chatInput.value = '';
  chatSuggestions.style.display = 'none';

  showTyping();
  setTimeout(() => {
    removeTyping();
    addMessage(getBotReply(text), 'bot');
  }, 900 + Math.random() * 600);
}

chatSend.addEventListener('click', () => sendChat(chatInput.value));
chatInput.addEventListener('keydown', e => { if (e.key === 'Enter') sendChat(chatInput.value); });

document.querySelectorAll('.suggestion-chip').forEach(chip => {
  chip.addEventListener('click', () => sendChat(chip.dataset.q));
});

chatbotFab.addEventListener('click', () => {
  const isOpen = chatbotWindow.style.display !== 'none';
  chatbotWindow.style.display = isOpen ? 'none' : 'flex';
  chatbotWindow.style.flexDirection = 'column';
  fabBadge.style.display = 'none';
  if (!isOpen) chatInput.focus();
});

chatbotClose.addEventListener('click', () => {
  chatbotWindow.style.display = 'none';
});

/* ---- Toast Notifications ---- */
function showToast(msg, type = 'success') {
  const existing = document.querySelector('.gt-toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'gt-toast';
  toast.textContent = msg;
  toast.style.cssText = `
    position: fixed; bottom: 100px; left: 50%; transform: translateX(-50%) translateY(20px);
    background: ${type === 'error' ? '#ff4a6e' : 'var(--accent)'};
    color: ${type === 'error' ? 'white' : '#0a0a0f'};
    padding: 10px 20px; border-radius: 99px; font-weight: 600; font-size: 0.875rem;
    z-index: 9999; opacity: 0; transition: all 0.3s ease; font-family: var(--font-display);
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    pointer-events: none;
  `;
  document.body.appendChild(toast);
  requestAnimationFrame(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';
  });
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(-50%) translateY(20px)';
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

/* ---- Scroll Fade-In ---- */
const fadeEls = document.querySelectorAll('.feature-card, .tech-card, .gesture-item, .shortcut, .arch-node');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

fadeEls.forEach(el => {
  el.classList.add('fade-in');
  observer.observe(el);
});

/* ---- Section header fade ---- */
document.querySelectorAll('.section-header').forEach(el => {
  el.classList.add('fade-in');
  observer.observe(el);
});

/* ---- Keyboard shortcuts ---- */
document.addEventListener('keydown', e => {
  // Toggle theme: Alt+T
  if (e.altKey && e.key === 't') themeToggle.click();
  // Open chatbot: Alt+C
  if (e.altKey && e.key === 'c') chatbotFab.click();
});

/* ---- Animate bar on hero load ---- */
window.addEventListener('load', () => {
  setTimeout(() => {
    const heroBar = document.getElementById('demoBar');
    if (heroBar) {
      heroBar.style.width = '0%';
    }
  }, 400);
});

