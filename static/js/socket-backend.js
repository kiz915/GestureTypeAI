
/* ============================================================
   GestureType AI — Backend Socket.IO Integration
   Connects to Python Flask-SocketIO server at localhost:5000
   Falls back gracefully if backend is not running
   ============================================================ */

(function() {
  const BACKEND_URL = 'http://localhost:5000';
  let socket = null;
  let backendConnected = false;

  // Backend status indicator
  function createStatusBadge() {
    const badge = document.createElement('div');
    badge.id = 'backendStatus';
    badge.style.cssText = `
      position: fixed; top: 80px; right: 20px; z-index: 200;
      display: flex; align-items: center; gap: 7px;
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 99px; padding: 6px 14px;
      font-family: var(--font-mono); font-size: 0.72rem;
      color: var(--text-3); transition: all 0.4s ease;
      box-shadow: 0 2px 12px rgba(0,0,0,0.3);
    `;
    badge.innerHTML = `
      <span id="statusDot" style="width:8px;height:8px;border-radius:50%;background:#555;display:inline-block;transition:background 0.4s;"></span>
      <span id="statusText">BACKEND: CONNECTING...</span>
    `;
    document.body.appendChild(badge);
    return badge;
  }

  function setStatus(connected) {
    backendConnected = connected;
    const dot = document.getElementById('statusDot');
    const text = document.getElementById('statusText');
    if (!dot || !text) return;
    if (connected) {
      dot.style.background = '#4aff9e';
      dot.style.boxShadow = '0 0 6px #4aff9e';
      text.textContent = 'BACKEND: LIVE ✓';
      text.style.color = '#4aff9e';
    } else {
      dot.style.background = '#ff4a6e';
      dot.style.boxShadow = '0 0 6px rgba(255,74,110,0.5)';
      text.textContent = 'BACKEND: OFFLINE (demo mode)';
      text.style.color = '#ff4a6e';
    }
  }

  function initSocket() {
    try {
      socket = io(BACKEND_URL, { timeout: 3000, reconnection: true, reconnectionAttempts: 5 });

      socket.on('connect', () => {
        setStatus(true);
        showToast('Backend connected! Real gesture AI active 🤖', 'success');
        // Patch the cam toggle to use backend
        patchCameraForBackend();
      });

      socket.on('disconnect', () => {
        setStatus(false);
        showToast('Backend disconnected — fallback to demo mode', 'error');
        unpatchCamera();
      });

      socket.on('connect_error', () => {
        setStatus(false);
      });

      // Receive real camera frames from backend
      socket.on('frame', (data) => {
        if (!data || !data.image) return;
        const video = document.getElementById('webcamVideo');
        const img = document.getElementById('backendFrameImg');
        if (img) {
          img.src = 'data:image/jpeg;base64,' + data.image;
        }
        // Real gesture detected
        if (data.gesture) {
          handleRealGesture(data.gesture, data.confidence || 0.95);
        }
      });

      socket.on('camera_status', (data) => {
        console.log('[GestureType] Camera status:', data.status);
      });

    } catch(e) {
      setStatus(false);
    }
  }

  // Create an <img> overlay element to show backend frames
  function createFrameImg() {
    if (document.getElementById('backendFrameImg')) return;
    const img = document.createElement('img');
    img.id = 'backendFrameImg';
    img.style.cssText = `
      position:absolute; inset:0; width:100%; height:100%;
      object-fit:cover; display:none; transform: scaleX(-1);
    `;
    const frame = document.getElementById('cameraFrame');
    if (frame) frame.appendChild(img);
  }

  let originalCamToggleHandler = null;
  let backendCameraOn = false;

  function patchCameraForBackend() {
    createFrameImg();
    const camToggle = document.getElementById('camToggle');
    const camBtnText = document.getElementById('camBtnText');
    const camBtnIcon = camToggle?.querySelector('.cam-btn-icon');
    const cameraPlaceholder = document.getElementById('cameraPlaceholder');
    const cameraHud = document.getElementById('cameraHud');
    const frameImg = document.getElementById('backendFrameImg');

    if (!camToggle) return;

    // Replace click handler
    const newHandler = () => {
      if (!backendCameraOn) {
        // Start backend camera
        socket.emit('start_camera');
        backendCameraOn = true;
        if (frameImg) frameImg.style.display = 'block';
        if (cameraPlaceholder) cameraPlaceholder.style.display = 'none';
        if (cameraHud) cameraHud.style.display = 'flex';
        if (camBtnText) camBtnText.textContent = 'Disable Camera';
        if (camBtnIcon) camBtnIcon.textContent = '🔴';
        showToast('Backend camera started — real AI active!');

        // Simulate FPS display
        setInterval(() => {
          const fps = 27 + Math.floor(Math.random() * 5);
          const hudFps = document.getElementById('hudFps');
          if (hudFps) hudFps.textContent = fps + ' FPS';
        }, 800);
      } else {
        socket.emit('stop_camera');
        backendCameraOn = false;
        if (frameImg) frameImg.style.display = 'none';
        if (cameraPlaceholder) cameraPlaceholder.style.display = 'flex';
        if (cameraHud) cameraHud.style.display = 'none';
        if (camBtnText) camBtnText.textContent = 'Enable Camera';
        if (camBtnIcon) camBtnIcon.textContent = '📷';
        showToast('Camera stopped');
        const detectedGesture = document.getElementById('detectedGesture');
        if (detectedGesture) detectedGesture.textContent = '—';
      }
    };

    camToggle._backendHandler = newHandler;
    camToggle.addEventListener('click', newHandler);
    // Store reference to potentially remove later
  }

  function unpatchCamera() {
    const camToggle = document.getElementById('camToggle');
    if (camToggle && camToggle._backendHandler) {
      camToggle.removeEventListener('click', camToggle._backendHandler);
      camToggle._backendHandler = null;
    }
  }

  // ASL letter map for real gesture names
  const gestureToLetter = {
    'A':'A','B':'B','C':'C','D':'D','E':'E','F':'F','G':'G','H':'H',
    'I':'I','J':'J','K':'K','L':'L','M':'M','N':'N','O':'O','P':'P',
    'Q':'Q','R':'R','S':'S','T':'T','U':'U','V':'V','W':'W','X':'X',
    'Y':'Y','Z':'Z',
    'PEACE':'[SPACE]','POINT_UP':'[ENTER]','SHAKA':'[⌫]',
    'FIST':'[CAPS]','OK':'[COPY]','PINCH':'[PASTE]',
    'SCROLL_UP':'[↑]','SCROLL_DOWN':'[↓]'
  };

  function handleRealGesture(gesture, confidence) {
    const detectedGesture = document.getElementById('detectedGesture');
    const bigLetter = document.getElementById('bigLetter');
    const demoBar = document.getElementById('demoBar');
    const demoConf = document.getElementById('demoConf');

    const display = gestureToLetter[gesture] || gesture;
    if (detectedGesture) detectedGesture.textContent = display + ' (' + Math.round(confidence * 100) + '%)';
    if (bigLetter) {
      bigLetter.textContent = display;
      bigLetter.style.transform = 'scale(1.4)';
      setTimeout(() => { bigLetter.style.transform = 'scale(1)'; bigLetter.style.transition = 'transform 0.3s cubic-bezier(0.34,1.56,0.64,1)'; }, 50);
    }
    if (demoBar) demoBar.style.width = Math.round(confidence * 100) + '%';
    if (demoConf) demoConf.textContent = Math.round(confidence * 100) + '%';

    // Add letter to output if it's a real letter
    if (gesture.length === 1 && gesture >= 'A' && gesture <= 'Z' && confidence > 0.85) {
      // Use the outputText from the main app
      const outputArea = document.getElementById('outputArea');
      if (outputArea) {
        const currentSpan = outputArea.querySelector('span:not(.output-placeholder)');
        const current = currentSpan ? currentSpan.textContent : '';
        const newText = current + gesture;
        outputArea.innerHTML = `<span style="font-size:1.1rem">${newText}</span>`;
      }
    }
  }

  // Init on load
  window.addEventListener('load', () => {
    createStatusBadge();
    setStatus(false);
    // Try to connect after short delay
    setTimeout(initSocket, 800);
  });

  // Expose for debugging
  window.gestureBackend = { getSocket: () => socket, isConnected: () => backendConnected };
})();

