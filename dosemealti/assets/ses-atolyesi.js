import { compose, createPlayer } from './ses-atolyesi-audio.js?v=1';

const WORLDS = {
  stars: { label: 'Yıldız Tozu', seed: 2083714, tone: 'bell', tempo: 72, echo: 48 },
  forest: { label: 'Masal Ormanı', seed: 2081769, tone: 'harp', tempo: 76, echo: 33 },
  lullaby: { label: 'Ay Işığı', seed: 2081380, tone: 'felt', tempo: 67, echo: 24 },
  dawn: { label: 'Gün Doğumu', seed: 2084103, tone: 'soft', tempo: 86, echo: 29 },
};
const TONES = ['bell', 'harp', 'felt', 'soft', 'aurora'];
const STORAGE = 'harika-ses-atolyesi-v1';
const $ = id => document.getElementById(id);
const controls = {
  tone: $('sound-tone'), tempo: $('sound-tempo'), echo: $('sound-echo'), volume: $('sound-volume'),
};
const playButton = $('sound-play');
const remixButton = $('sound-remix');
const shareButton = $('sound-share');
const sky = $('sound-sky');
const stars = [...$('sound-stars').querySelectorAll('button')];
const worldChoices = [...document.querySelectorAll('input[name="world"]')];
const player = createPlayer();

function parseMelody(code) {
  const match = /^ses=v1\.([a-z]+)\.([0-9a-z]{1,7})\.([a-z]+)\.(\d{2,3})\.(\d{1,2})$/.exec(code);
  if (!match) return null;
  const [, world, encodedSeed, tone, encodedTempo, encodedEcho] = match;
  const seed = Number.parseInt(encodedSeed, 36);
  const tempo = Number(encodedTempo);
  const echo = Number(encodedEcho);
  if (!Object.hasOwn(WORLDS, world) || !TONES.includes(tone) || seed > 0xffffffff
      || tempo < 50 || tempo > 132 || echo > 80) return null;
  return { world, seed, tone, tempo, echo };
}

function getDefault(world) {
  const { seed, tone, tempo, echo } = WORLDS[world];
  return { world, seed, tone, tempo, echo };
}

function readSaved() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE)) || {};
  } catch {
    return {};
  }
}

const saved = readSaved();
const incoming = parseMelody(location.hash.slice(1));
let state = incoming || parseMelody(saved.melody) || getDefault('stars');
let volume = Number.isInteger(saved.volume) && saved.volume >= 0 && saved.volume <= 100 ? saved.volume : 46;
let composition = compose(state.world, state.seed);
let running = false;
let starting = false;
let intent = 0;
let timer;
let cursor = 0;
let next = 0;
const lightTimers = new Set();
const lightOffTimers = new Map();

function melodyCode() {
  const { world, seed, tone, tempo, echo } = state;
  return `ses=v1.${world}.${seed.toString(36)}.${tone}.${tempo}.${echo}`;
}

function remember() {
  try {
    localStorage.setItem(STORAGE, JSON.stringify({ melody: melodyCode(), volume }));
  } catch {
    // Playback and link sharing also work with browser storage disabled.
  }
}

function status(message) {
  $('sound-status').textContent = message;
}

function syncMixLabels() {
  $('sound-tempo-value').textContent = `${state.tempo} BPM`;
  $('sound-echo-value').textContent = `%${state.echo}`;
  $('sound-volume-value').textContent = `%${volume}`;
}

function syncWorld() {
  for (const choice of worldChoices) choice.checked = choice.value === state.world;
  sky.dataset.world = state.world;
  $('sound-sky-world').textContent = WORLDS[state.world].label;
  controls.tone.value = state.tone;
  controls.tempo.value = state.tempo;
  controls.echo.value = state.echo;
  controls.volume.value = volume;
  syncMixLabels();
}

function syncPlayback() {
  $('sound-play-icon').textContent = running ? '■' : '▶';
  $('sound-play-label').textContent = starting ? 'İptal et' : running ? 'Melodiyi durdur' : 'Melodiyi çal';
}

function flash(star) {
  clearTimeout(lightOffTimers.get(star));
  star.classList.add('is-lit');
  lightOffTimers.set(star, setTimeout(() => {
    star.classList.remove('is-lit');
    lightOffTimers.delete(star);
  }, 230));
}

function stop() {
  intent += 1;
  running = false;
  starting = false;
  clearInterval(timer);
  for (const timeout of lightTimers) clearTimeout(timeout);
  lightTimers.clear();
  for (const [star, timeout] of lightOffTimers) {
    clearTimeout(timeout);
    star.classList.remove('is-lit');
  }
  lightOffTimers.clear();
  player.silence();
  syncPlayback();
}

function tick() {
  const now = player.now();
  if (next < now - .15) next = now + .02;
  while (next < now + .11) {
    const event = composition.events[cursor];
    const beatSeconds = 60 / state.tempo;
    if (event.beat === 0) {
      composition.chords[event.bar].forEach((note, index) => {
        player.play(note, next + index * .08, 2.5 * beatSeconds, .38 * composition.harmony, 'felt');
      });
    }
    if (event.note !== undefined) {
      const length = Math.max(.08, (event.beats - event.gap) * beatSeconds * .84);
      player.play(event.note, next, length, event.velocity * .83, state.tone);
      const star = stars[event.note % stars.length];
      const timeout = setTimeout(() => {
        lightTimers.delete(timeout);
        flash(star);
      }, Math.max(0, (next - now) * 1000));
      lightTimers.add(timeout);
    }
    next += event.beats * beatSeconds;
    cursor = (cursor + 1) % composition.events.length;
  }
}

async function start() {
  if (running || starting) return;
  const request = ++intent;
  starting = true;
  syncPlayback();
  try {
    await player.ready();
    if (request !== intent || document.hidden) return;
    starting = false;
    running = true;
    cursor = 0;
    player.open(volume, state.echo);
    next = player.now() + .035;
    tick();
    timer = setInterval(tick, 25);
    status('Melodi çalıyor.');
    syncPlayback();
  } catch {
    if (request !== intent) return;
    stop();
    status('Ses başlatılamadı. Bu tarayıcıda sesi yeniden açmayı dene.');
  }
}

function useMelody(settings, play = false) {
  const resume = play || running || starting;
  stop();
  state = settings;
  composition = compose(state.world, state.seed);
  syncWorld();
  remember();
  if (resume) void start();
}

async function playStar(index) {
  const request = intent;
  try {
    await player.ready();
    if (request !== intent || document.hidden) return;
    player.open(volume, state.echo);
    player.play(composition.starNotes[index], player.now(), .41, .72, state.tone);
    flash(stars[index]);
  } catch {
    if (request === intent) status('Yıldızın sesi açılamadı. Bir kez daha dokunmayı dene.');
  }
}

playButton.addEventListener('click', () => {
  if (running || starting) {
    stop();
    status('Melodi durduruldu.');
  } else {
    void start();
  }
});

for (const choice of worldChoices) {
  choice.addEventListener('change', () => {
    useMelody(getDefault(choice.value));
    if (!starting) status(`${WORLDS[state.world].label} seçildi.`);
  });
}

remixButton.addEventListener('click', () => {
  const seed = crypto.getRandomValues(new Uint32Array(1))[0];
  useMelody({ ...state, seed: seed === state.seed ? (seed + 1) >>> 0 : seed }, true);
});

stars.forEach((star, index) => star.addEventListener('click', () => { void playStar(index); }));
for (const [setting, control] of Object.entries(controls)) {
  control.addEventListener('input', () => {
    const value = setting === 'tone' ? control.value : Number(control.value);
    if (setting === 'volume') volume = value;
    else state[setting] = value;
    syncMixLabels();
    player.mix(volume, state.echo);
    remember();
  });
}

const dialog = $('sound-share-dialog');
const shareUrl = $('sound-share-url');
const dialogStatus = $('sound-dialog-status');

shareButton.addEventListener('click', () => {
  const url = new URL(location.href);
  url.hash = melodyCode();
  shareUrl.value = url.href;
  dialogStatus.textContent = '';
  dialog.showModal();
  shareUrl.select();
});

$('sound-copy').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(shareUrl.value);
    dialogStatus.textContent = 'Bağlantı kopyalandı.';
  } catch {
    shareUrl.focus();
    shareUrl.select();
    dialogStatus.textContent = 'Bağlantıyı seçili alandan kopyalayabilirsin.';
  }
});

window.addEventListener('hashchange', () => {
  const melody = parseMelody(location.hash.slice(1));
  if (melody) {
    useMelody(melody);
    if (!starting) status('Paylaşılan melodi hazır.');
  }
});
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    if (running || starting) status('Melodi duraklatıldı.');
    stop();
  }
});
window.addEventListener('pagehide', stop);

// Only the artwork moves. The note buttons and page layout stay fixed.
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let pointer = null;
let parallaxFrame = 0;
function paintDepth() {
  parallaxFrame = 0;
  const bounds = sky.getBoundingClientRect();
  const height = window.innerHeight;
  if (reduceMotion.matches || bounds.bottom < 0 || bounds.top > height) return;
  const center = bounds.top + bounds.height / 2;
  const scroll = Math.max(-1, Math.min(1, (height / 2 - center) / (height / 2)));
  const depth = pointer ? pointer.strength : 0;
  const x = pointer ? ((pointer.x - bounds.left) / bounds.width - .5) * -30 * depth : 0;
  const y = pointer ? ((pointer.y - bounds.top) / bounds.height - .5) * -26 * depth : 0;
  sky.style.setProperty('--sound-x', `${Math.max(-18, Math.min(18, x)).toFixed(2)}px`);
  sky.style.setProperty('--sound-y', `${Math.max(-18, Math.min(18, y + scroll * 9)).toFixed(2)}px`);
}
function scheduleDepth() {
  if (!parallaxFrame && !reduceMotion.matches) parallaxFrame = requestAnimationFrame(paintDepth);
}
function moveDepth(event) {
  const { clientX: x, clientY: y, pointerType, pressure } = event;
  const strength = pointerType === 'mouse' ? 1 : .68 + pressure * .45;
  pointer = { x, y, strength };
  scheduleDepth();
}
function clearDepth() {
  pointer = null;
  scheduleDepth();
}
sky.addEventListener('pointerdown', moveDepth, { passive: true });
sky.addEventListener('pointermove', moveDepth, { passive: true });
sky.addEventListener('pointerleave', clearDepth);
sky.addEventListener('pointercancel', clearDepth);
sky.addEventListener('pointerup', event => {
  if (event.pointerType !== 'mouse') clearDepth();
});
window.addEventListener('scroll', scheduleDepth, { passive: true });
window.addEventListener('resize', scheduleDepth);
reduceMotion.addEventListener('change', clearDepth);

syncWorld();
scheduleDepth();
if (incoming) {
  status('Paylaşılan melodi hazır.');
  remember();
}
for (const button of [playButton, remixButton, shareButton, ...stars]) button.disabled = false;
