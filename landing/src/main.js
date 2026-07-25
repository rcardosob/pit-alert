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
  const pitAudio = new Audio('/pit_stop.wav');
  let audioPlayed = false;

  ScrollTrigger.create({
    trigger: '#scene-03',
    start: 'top 40%',
    onEnter: () => {
      if (!audioPlayed) {
        pitAudio.play().catch(() => {});
        audioPlayed = true;
      }
    },
    onLeaveBack: () => {
      audioPlayed = false;
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

  // Scene 03: Countdown sync
  if (countdownEl) {
    ScrollTrigger.create({
      trigger: '#scene-03',
      start: 'top center',
      end: 'bottom center',
      scrub: true,
      onUpdate: (self) => {
        const totalSeconds = Math.max(0, Math.floor(180 * (1 - self.progress)));
        const m = String(Math.floor(totalSeconds / 60)).padStart(2, '0');
        const s = String(totalSeconds % 60).padStart(2, '0');
        countdownEl.textContent = `${m}:${s}`;
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
