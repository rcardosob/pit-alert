import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', () => {
  initTelemetryClock();
  initAudioTrigger();
  initSceneAnimations();
});

function initTelemetryClock() {
  const clockEl = document.getElementById('tel-clock');
  if (!clockEl) return;
  
  setInterval(() => {
    const now = new Date();
    const hrs = String(now.getHours()).padStart(2, '0');
    const mins = String(now.getMinutes()).padStart(2, '0');
    const secs = String(now.getSeconds()).padStart(2, '0');
    const ms = String(now.getMilliseconds()).padStart(3, '0').slice(0, 2);
    clockEl.textContent = `${hrs}:${mins}:${secs}.${ms}`;
  }, 40);
}

function initAudioTrigger() {
  const pitAudio = new Audio('./pit_stop.wav');
  const returnAudio = new Audio('./two_minutes__engine_fire_up_.wav');
  
  let audioPlayedScene3 = false;
  let audioPlayedScene6 = false;
  let audioEnabled = false;

  const headerStatus = document.querySelector('.header-status');
  const statusText = document.querySelector('.status-text');

  if (headerStatus && statusText) {
    // Estado inicial: Apagado (OFF)
    statusText.textContent = 'PIT WALL / OFF';
    headerStatus.classList.remove('active');

    headerStatus.addEventListener('click', () => {
      audioEnabled = !audioEnabled;
      if (audioEnabled) {
        statusText.textContent = 'PIT WALL / ON';
        headerStatus.classList.add('active');

        // Desbloquear contexto de audio en navegadores web (User Gesture bypass)
        pitAudio.play().then(() => {
          pitAudio.pause();
          pitAudio.currentTime = 0;
        }).catch((e) => console.log('Audio 1 preload unlock failed:', e));

        returnAudio.play().then(() => {
          returnAudio.pause();
          returnAudio.currentTime = 0;
        }).catch((e) => console.log('Audio 2 preload unlock failed:', e));
      } else {
        statusText.textContent = 'PIT WALL / OFF';
        headerStatus.classList.remove('active');
      }
    });
  }

  // Alerta de Escena 3
  ScrollTrigger.create({
    trigger: '#scene-03',
    start: 'top 40%',
    onEnter: () => {
      if (audioEnabled && !audioPlayedScene3) {
        pitAudio.play().catch((e) => console.log('Audio 1 play failed:', e));
        audioPlayedScene3 = true;
      }
    },
    onLeaveBack: () => {
      audioPlayedScene3 = false;
    }
  });

  // Alerta de Escena 6
  ScrollTrigger.create({
    trigger: '#scene-06',
    start: 'top 40%',
    onEnter: () => {
      if (audioEnabled && !audioPlayedScene6) {
        returnAudio.play().catch((e) => console.log('Audio 2 play failed:', e));
        audioPlayedScene6 = true;
      }
    },
    onLeaveBack: () => {
      audioPlayedScene6 = false;
    }
  });
}

function initSceneAnimations() {
  const countdownEl = document.getElementById('countdown');
  const heroPart2 = document.getElementById('hero-part-2');
  
  // Scene 01: Reveal "is leaving the track." as user scrolls
  gsap.to(heroPart2, {
    scrollTrigger: {
      trigger: '#scene-01',
      start: 'top top',
      end: 'bottom 50%',
      scrub: true
    },
    opacity: 1,
    y: 0,
    ease: 'power2.out'
  });

  // Scene 03: Countdown sync with milliseconds (mm:ss.ms)
  if (countdownEl) {
    ScrollTrigger.create({
      trigger: '#scene-03',
      start: 'top center',
      end: 'bottom center',
      scrub: true,
      onUpdate: (self) => {
        const totalMs = Math.max(0, Math.floor(180000 * (1 - self.progress)));
        const m = String(Math.floor(totalMs / 60000)).padStart(2, '0');
        const s = String(Math.floor((totalMs % 60000) / 1000)).padStart(2, '0');
        const ms = String(Math.floor((totalMs % 1000) / 10)).padStart(2, '0');
        countdownEl.textContent = `${m}:${s}.${ms}`;
      }
    });
  }

  // Scene 05: Product Hotspots reveal
  gsap.to(['#hotspot-1', '#hotspot-2', '#hotspot-3'], {
    scrollTrigger: {
      trigger: '#scene-05',
      start: 'top 60%',
      end: 'bottom 80%',
      scrub: 1
    },
    opacity: 1,
    y: 0,
    stagger: 0.3
  });
}
