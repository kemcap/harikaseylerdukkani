// The Sound Lab v20 freestyle composer, with the public atelier's four styles
// and the original offline oscillator timbres. No samples are fetched.
const MAJOR = [0, 2, 4, 5, 7, 9, 11];
const STYLES = {
  stars: {
    tonic: 60, scale: MAJOR, rhythm: 'medium', rest: .17, harmony: .54,
    progressions: [[0, 5, 3, 4], [0, 4, 3, 0], [0, 3, 4, 0]],
  },
  forest: {
    tonic: 62, scale: MAJOR, rhythm: 'medium', rest: .14, harmony: .62,
    progressions: [[0, 3, 5, 4], [0, 4, 3, 0], [0, 5, 3, 4]],
  },
  lullaby: {
    tonic: 60, scale: MAJOR, rhythm: 'slow', rest: .2, harmony: .44,
    progressions: [[0, 4, 5, 3], [0, 3, 4, 0], [0, 5, 3, 4]],
  },
  dawn: {
    tonic: 65, scale: MAJOR, rhythm: 'medium', rest: .11, harmony: .52,
    progressions: [[0, 3, 5, 4], [0, 4, 3, 0], [0, 5, 3, 4]],
  },
};
const RHYTHMS = {
  slow: [[2, 1, 1], [1, 1, 2], [1.5, .5, 2], [1, .5, .5, 2], [2, 2]],
  medium: [[1, 1, 1, 1], [1.5, .5, 1, 1], [1, .5, .5, 1, 1], [1, 1, 2], [.5, .5, 1, 1, 1]],
};
const TIMBRES = {
  felt: { partials: [[1, 1], [2, .2], [3, .065], [4, .025]], release: .16, rise: .023, filter: 5200 },
  soft: { partials: [[1, 1], [2, .34], [3, .11], [4, .028]], release: .2, rise: .012, filter: 7100 },
  harp: { partials: [[1, 1], [2, .42], [3, .22], [4, .1], [5, .045]], release: .3, rise: .006, filter: 11000 },
  bell: { partials: [[1, 1], [2.004, .42], [3.89, .28], [5.37, .17]], release: .74, rise: .009, filter: 16000 },
  aurora: { partials: [[.5, .23], [1, 1], [1.004, .31], [2.008, .23], [3.006, .08]], release: 1.85, rise: .19, filter: 6300 },
};

function seededRandom(seed) {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6D2B79F5) | 0;
    let mixed = Math.imul(state ^ (state >>> 15), 1 | state);
    mixed ^= mixed + Math.imul(mixed ^ (mixed >>> 7), 61 | mixed);
    return ((mixed ^ (mixed >>> 14)) >>> 0) / 4294967296;
  };
}

export function compose(world, seed) {
  const { tonic, scale, harmony, rhythm, rest, progressions } = STYLES[world];
  const random = seededRandom(seed);
  const choose = values => values[Math.floor(random() * values.length)];
  const progression = choose(progressions);
  const alternate = choose(progressions);
  const degrees = [...progression, ...progression, ...alternate, ...progression];
  for (const bar of [3, 7, 11, 14]) degrees[bar] = 4;
  degrees[15] = 0;
  const pitch = step => tonic - 24 + scale[step % 7] + 12 * Math.floor(step / 7);
  const chords = degrees.map(degree => [pitch(degree), pitch(degree + 2), pitch(degree + 4)]);
  const motive = Array.from({ length: 10 }, () => choose([-2, -1, -1, 0, 0, 1, 1, 2]));
  const candidateNotes = Array.from({ length: 26 }, (_, index) => tonic - 2 + index)
    .filter(note => scale.includes((note - tonic + 12) % 12));
  const phraseRhythms = [];
  const events = [];
  let previous = tonic + 7;
  degrees.forEach((_, bar) => {
    const phraseEnd = bar % 4 === 3;
    let pattern = bar < 4 || (bar >= 8 && bar < 12)
      ? choose(RHYTHMS[rhythm])
      : phraseRhythms[bar % 4];
    if (bar < 4) phraseRhythms.push(pattern);
    if (phraseEnd) pattern = bar === 15 ? [1, 1, 2] : choose([[1, 1, 2], [2, 1, 1], [1, 1.5, 1.5]]);
    const chordPitches = chords[bar].map(note => note % 12);
    let beat = 0;
    pattern.forEach((beats, index) => {
      const final = bar === 15 && index === pattern.length - 1;
      const pause = (phraseEnd && index === pattern.length - 1 && bar !== 15 && random() < .34)
        || (index > 0 && !final && random() < rest * .42);
      if (pause) {
        events.push({ beats, bar, beat });
      } else {
        const target = Math.min(tonic + 20, Math.max(tonic, previous + motive[(bar % 4 * 3 + index) % motive.length] * 2));
        const downbeat = beat === 0 || beat === 2;
        let note = tonic + 7;
        let bestCost = Infinity;
        for (const candidate of candidateNotes) {
          const chordTone = chordPitches.includes(candidate % 12);
          const cost = Math.abs(candidate - target) * .62 + Math.abs(candidate - previous) * .25
            + (chordTone ? 0 : downbeat ? 5 : .3) + (candidate < tonic + 1 ? 1.2 : 0)
            + (random() - .5) * 1.45;
          if (cost < bestCost) {
            bestCost = cost;
            note = candidate;
          }
        }
        if (final) note = tonic + 12;
        previous = note;
        const velocity = .91 + (index === 0 ? .1 : 0) + (phraseEnd ? -.04 : 0) + (random() - .5) * .1;
        const gap = !final && beats >= 1 && random() < rest * .45 ? Math.min(.25, beats * .22) : 0;
        events.push({ note, beats, bar, beat, gap, velocity });
      }
      beat += beats;
    });
  });
  const starNotes = [0, 2, 4, 5, 7, 12].map(interval => tonic + 12 + interval);
  return { chords, events, starNotes, harmony };
}

export function createPlayer() {
  const Audio = window.AudioContext || window.webkitAudioContext;
  let context;
  let master;
  let channel;
  let resumePending;

  function init() {
    context = new Audio();
    master = context.createGain();
    master.gain.value = 0;
    const limiter = context.createDynamicsCompressor();
    limiter.threshold.value = -15;
    limiter.ratio.value = 6;
    master.connect(limiter).connect(context.destination);
  }

  async function ready() {
    if (!Audio) throw new Error('Web Audio unavailable');
    if (!context) init();
    if (context.state === 'running') return;
    if (!resumePending) {
      resumePending = context.resume().finally(() => { resumePending = null; });
    }
    await resumePending;
  }

  function mix(volume, echo) {
    if (!context) return;
    const time = context.currentTime;
    master.gain.setTargetAtTime(volume / 100 * .7, time, .025);
    if (!channel) return;
    channel.echo.gain.setTargetAtTime(echo / 100 * .38, time, .06);
    channel.feedback.gain.setTargetAtTime(.17 + echo / 100 * .34, time, .06);
  }

  function open(volume, echo) {
    if (!channel) {
      const output = context.createGain();
      const dry = context.createGain();
      const echo = context.createGain();
      const feedback = context.createGain();
      const delay = context.createDelay(.8);
      delay.delayTime.value = .36;
      dry.connect(output);
      echo.connect(delay).connect(output);
      delay.connect(feedback).connect(delay);
      output.connect(master);
      channel = { output, dry, echo, feedback, delay };
    }
    mix(volume, echo);
  }

  function silence() {
    if (!channel) return;
    const { output, dry, echo, feedback, delay } = channel;
    const time = context.currentTime;
    output.gain.setTargetAtTime(0, time, .019);
    setTimeout(() => {
      for (const node of [output, dry, echo, feedback, delay]) node.disconnect();
    }, 130);
    channel = null;
  }

  function play(midi, time, length, velocity, timbre) {
    const { partials, release, rise, filter } = TIMBRES[timbre];
    const start = Math.max(context.currentTime + .003, time);
    const end = start + length + release;
    const amplitude = .19 * Math.min(velocity, 1);
    const gain = context.createGain();
    const lowpass = context.createBiquadFilter();
    lowpass.type = 'lowpass';
    lowpass.frequency.value = Math.min(context.sampleRate * .45, filter);
    const attack = Math.min(rise, length * .45);
    gain.gain.setValueAtTime(.00006, start);
    gain.gain.exponentialRampToValueAtTime(amplitude, start + attack);
    gain.gain.exponentialRampToValueAtTime(amplitude * .36, start + length * .86);
    gain.gain.exponentialRampToValueAtTime(.00006, end);
    lowpass.connect(gain);
    gain.connect(channel.dry);
    gain.connect(channel.echo);
    const frequency = 440 * 2 ** ((midi - 69) / 12);
    const voices = [];
    for (const [ratio, level] of partials) {
      if (frequency * ratio >= context.sampleRate * .46) continue;
      const oscillator = context.createOscillator();
      const partial = context.createGain();
      oscillator.frequency.value = frequency * ratio;
      partial.gain.value = level;
      oscillator.connect(partial).connect(lowpass);
      oscillator.start(start);
      oscillator.stop(end + .01);
      voices.push([oscillator, partial]);
    }
    voices[0][0].onended = () => {
      for (const [oscillator, partial] of voices) {
        oscillator.disconnect();
        partial.disconnect();
      }
      lowpass.disconnect();
      gain.disconnect();
    };
  }

  return { ready, open, mix, silence, play, now: () => context.currentTime };
}
