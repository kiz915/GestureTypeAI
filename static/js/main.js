// ============================================================
// GestureType AI — Main JavaScript (Corrected Version)
// ============================================================

// ---------- SAFE GET ELEMENT ----------
const $ = (id) => document.getElementById(id);

// ---------- THEME TOGGLE ----------
const themeToggle = $('themeToggle');
const html = document.documentElement;

function setTheme(theme) {
  html.setAttribute('data-theme', theme);
  localStorage.setItem('gt-theme', theme);
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    setTheme(current === 'dark' ? 'light' : 'dark');
  });
}

setTheme(localStorage.getItem('gt-theme') || 'dark');

// ---------- NAVBAR SCROLL ----------
const navbar = $('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 30);
  });
}

// ---------- MOBILE MENU ----------
const hamburger = $('hamburger');
const mobileMenu = $('mobileMenu');

if (hamburger && mobileMenu) {
  hamburger.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
  });

  mobileMenu.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => mobileMenu.classList.remove('open'));
  });
}

// ---------- HERO ANIMATION ----------
const heroHands = [
  { emoji: '🤟', label: 'I Love You', output: 'I ❤ U', conf: 97 },
  { emoji: '✋', label: 'Hello', output: 'HELLO', conf: 95 },
  { emoji: '✌', label: 'Space', output: '[SPACE]', conf: 98 }
];

let heroIdx = 0;

function cycleHeroHand() {
  const emojiEl = document.querySelector('.hand-emoji');
  const labelEl = document.querySelector('.hand-label');

  if (!emojiEl || !labelEl) return;

  heroIdx = (heroIdx + 1) % heroHands.length;
  const h = heroHands[heroIdx];

  emojiEl.textContent = h.emoji;
  labelEl.textContent = h.label;
}

setInterval(cycleHeroHand, 3000);

// ---------- CAMERA ----------
const camToggle = $('camToggle');
const video = $('webcamVideo');

let cameraStream = null;
let cameraOn = false;

if (camToggle && video) {
  camToggle.addEventListener('click', async () => {
    if (!cameraOn) {
      try {
        cameraStream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = cameraStream;
        video.style.display = 'block';
        cameraOn = true;
        showToast('Camera enabled');
      } catch (err) {
        showToast('Camera permission denied', 'error');
      }
    } else {
      cameraStream?.getTracks().forEach(t => t.stop());
      video.style.display = 'none';
      cameraOn = false;
      showToast('Camera disabled');
    }
  });
}

// ---------- OUTPUT ----------
let outputText = '';

function updateOutput() {
  const outputArea = $('outputArea');
  if (!outputArea) return;

  outputArea.textContent = outputText || 'Your text will appear here...';
}

// ---------- COPY ----------
const copyBtn = $('copyOutput');
if (copyBtn) {
  copyBtn.addEventListener('click', () => {
    if (!outputText) return;
    navigator.clipboard.writeText(outputText);
    showToast('Copied!');
  });
}

// ---------- CLEAR ----------
const clearBtn = $('clearOutput');
if (clearBtn) {
  clearBtn.addEventListener('click', () => {
    outputText = '';
    updateOutput();
  });
}

// ---------- TOAST ----------
function showToast(msg, type = 'success') {
  const toast = document.createElement('div');
  toast.textContent = msg;

  toast.style.cssText = `
    position: fixed;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    background: ${type === 'error' ? 'red' : 'green'};
    color: white;
    padding: 10px 20px;
    border-radius: 20px;
    z-index: 9999;
  `;

  document.body.appendChild(toast);

  setTimeout(() => toast.remove(), 2000);
}

// ---------- CHATBOT ----------
const chatInput = $('chatInput');
const chatSend = $('chatSend');
const chatMessages = $('chatbotMessages');

function addMessage(text, role) {
  if (!chatMessages) return;

  const div = document.createElement('div');
  div.textContent = text;
  div.style.textAlign = role === 'user' ? 'right' : 'left';
  chatMessages.appendChild(div);
}

function botReply(text) {
  if (text.includes('camera')) return 'Click enable camera button';
  return 'Ask about camera, gestures, or setup';
}

function sendChat(text) {
  if (!text.trim()) return;

  addMessage(text, 'user');

  setTimeout(() => {
    addMessage(botReply(text), 'bot');
  }, 800);
}

if (chatSend && chatInput) {
  chatSend.addEventListener('click', () => sendChat(chatInput.value));
  chatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') sendChat(chatInput.value);
  });
}

// ---------- SCROLL ANIMATION ----------
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
    }
  });
});

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
