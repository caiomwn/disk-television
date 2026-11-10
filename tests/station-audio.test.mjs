import test from 'node:test';
import assert from 'node:assert/strict';
import { StationAudio } from '../src/station-audio.js';

class AudioContextMock {
  state = 'suspended';
  destination = {};
  sources = [];
  async decodeAudioData(bytes) {
    if (!bytes.byteLength) throw new Error('decode failed');
    return { duration: 7 };
  }
  async resume() { this.state = 'running'; }
  createBufferSource() {
    const source = {
      connect() {}, disconnect() {},
      starts: [], stops: 0,
      start(...args) { this.starts.push(args); },
      stop() { this.stops++; this.onended?.(); },
    };
    this.sources.push(source);
    return source;
  }
}
// Real Node fetch with an in-memory data URL: only Web Audio is mocked.
const localFetch = () => fetch('data:application/octet-stream;base64,AQ==');
const clock = (elapsed = 0, extra = {}) => ({
  slot: { id: 'ident-1', type: 'ident', variant: 'station', duration: 12 },
  elapsed, startMs: 1000, ...extra,
});
function fixture(options = {}) {
  const context = new AudioContextMock();
  const audio = new StationAudio({ contextFactory: () => context, fetcher: localFetch, ...options });
  return { audio, context };
}

test('mute and GUI stop resume only at the current offset', async () => {
  const { audio, context } = fixture();
  await audio.prepare(); await audio.unlock();
  audio.update(clock(1));
  audio.update(clock(2), { enabled: false });
  assert.equal(context.sources[0].stops, 1);
  audio.update(clock(3));
  assert.deepEqual(context.sources[1].starts, [[0, 3, 4]]);
  audio.stop(); audio.stop();
  audio.update(clock(4));
  assert.deepEqual(context.sources[2].starts, [[0, 4, 3]]);
});

test('video cuts the source immediately and stop is idempotent', async () => {
  const { audio, context } = fixture();
  await audio.prepare(); await audio.unlock();
  audio.update(clock(1));
  audio.update(clock(0, { slot: { id: 'video', type: 'video', duration: 30 } }));
  assert.equal(context.sources.length, 1);
  assert.equal(context.sources[0].stops, 1);
  assert.equal(audio.getState().activeKey, null);
  audio.stop(); audio.stop();
  assert.equal(context.sources[0].stops, 1);
});

test('ticks and natural completion never restart the same absolute ident', async () => {
  const { audio, context } = fixture();
  await audio.prepare(); await audio.unlock();
  audio.update(clock(1));
  audio.update(clock(2));
  assert.equal(context.sources.length, 1);
  context.sources[0].onended?.();
  audio.update(clock(3));
  assert.equal(context.sources.length, 1);
  audio.update(clock(1, { startMs: 86401000 }));
  assert.equal(context.sources.length, 2);
});

test('entry seeks to elapsed time and clips playback to the remaining slot', async () => {
  const { audio, context } = fixture();
  await audio.prepare();
  await audio.unlock();
  audio.update(clock(3, { slot: { id: 'short', type: 'ident', variant: 'station', duration: 5 } }));
  assert.deepEqual(context.sources[0].starts, [[0, 3, 2]]);
  assert.equal(audio.getState().starts, 1);
});

test('unavailable context never throws or blocks an ident update', async () => {
  const audio = new StationAudio({ contextFactory: () => null });
  await audio.prepare(); await audio.unlock();
  assert.doesNotThrow(() => audio.update(clock(1)));
  assert.equal(audio.getState().starts, 0);
});

test('suspended context waits without consuming the absolute key', async () => {
  const { audio, context } = fixture();
  await audio.prepare();
  audio.update(clock(1));
  assert.equal(context.sources.length, 0);
  await audio.unlock();
  audio.update(clock(3));
  assert.deepEqual(context.sources[0].starts, [[0, 3, 4]]);
});

for (const failure of ['network', 'http', 'decode']) {
  test(`MP3 ${failure} failure falls back to WAV independently per variant`, async () => {
    const urls = [];
    const { audio } = fixture({ fetcher: async url => {
      urls.push(String(url));
      if (String(url).endsWith('.mp3')) {
        if (failure === 'network') throw new Error('offline');
        return { ok: failure !== 'http', arrayBuffer: async () => new ArrayBuffer(0) };
      }
      return localFetch();
    } });
    await audio.prepare();
    assert.deepEqual(audio.getState().readyVariants.sort(), ['next', 'night', 'station']);
    assert.equal(urls.filter(url => url.endsWith('.wav')).length, 3);
  });
}

test('both failed formats leave other variants usable and never throw', async () => {
  const { audio, context } = fixture({ fetcher: async url => {
    if (String(url).includes('ident-station.')) throw new Error('missing');
    return localFetch();
  } });
  await audio.prepare(); await audio.unlock();
  assert.deepEqual(audio.getState().readyVariants.sort(), ['next', 'night']);
  assert.doesNotThrow(() => audio.update(clock(1)));
  assert.equal(context.sources.length, 0);
});

test('new absolute ident stops the previous source before starting another', async () => {
  const { audio, context } = fixture();
  await audio.prepare(); await audio.unlock();
  audio.update(clock(1));
  const originalCreate = context.createBufferSource.bind(context);
  context.createBufferSource = () => {
    assert.equal(context.sources[0].stops, 1);
    return originalCreate();
  };
  audio.update(clock(2, { startMs: 2000 }));
  assert.equal(context.sources.length, 2);
  assert.equal(audio.getState().activeKey, JSON.stringify([2000, 'ident-1']));
});

test('continuity uses night once and does not loop through a long filler', async () => {
  const { audio, context } = fixture();
  await audio.prepare(); await audio.unlock();
  const slot = { id: 'filler', type: 'ident', variant: 'continuity', duration: 600 };
  audio.update(clock(2, { slot }));
  assert.equal(context.sources.length, 1);
  assert.equal(context.sources[0].buffer, audio.buffers.get('night'));
  context.sources[0].onended?.();
  assert.equal(audio.getState().activeKey, null);
  audio.update(clock(60, { slot }));
  assert.equal(context.sources.length, 1);
});

for (const [variant, duration] of [['next', 4], ['station', 18], ['night', 18]]) {
  test(`${variant} never exceeds its maximum playback window`, async () => {
    const { audio, context } = fixture();
    await audio.prepare(); await audio.unlock();
    audio.buffers.set(variant, { duration: 60 });
    const slot = { id: 'long', type: 'ident', variant, duration: 600 };
    audio.update(clock(1, { slot }));
    assert.deepEqual(context.sources[0].starts, [[0, 1, duration - 1]]);
  });
}

test('entry after audio or slot end remains silent without creating a source', async () => {
  const { audio, context } = fixture();
  await audio.prepare(); await audio.unlock();
  audio.update(clock(9));
  assert.equal(context.sources.length, 0);
  audio.update(clock(5, { slot: { id: 'ended', type: 'ident', variant: 'station', duration: 4 } }));
  assert.equal(context.sources.length, 0);
});

test('late decoded buffers seek from the latest tick, not the initial offset', async () => {
  let release;
  const gate = new Promise(resolve => { release = resolve; });
  const { audio, context } = fixture({ fetcher: async () => { await gate; return localFetch(); } });
  const preparation = audio.prepare();
  await audio.unlock();
  audio.update(clock(1));
  audio.update(clock(2));
  assert.equal(context.sources.length, 0);
  release(); await preparation;
  audio.update(clock(4));
  assert.deepEqual(context.sources[0].starts, [[0, 4, 3]]);
});

for (const operation of ['createBufferSource', 'connect', 'start']) {
  test(`Web Audio ${operation} failure stays nonfatal and permits retry`, async () => {
    const { audio, context } = fixture();
    await audio.prepare(); await audio.unlock();
    const create = context.createBufferSource.bind(context);
    context.createBufferSource = () => {
      if (operation === 'createBufferSource') throw new Error('device failure');
      const source = create();
      source[operation] = () => { throw new Error('device failure'); };
      return source;
    };
    assert.doesNotThrow(() => audio.update(clock(1)));
    assert.equal(audio.getState().starts, 0);
    assert.equal(audio.getState().activeKey, null);
    context.createBufferSource = create;
    audio.update(clock(3));
    assert.deepEqual(context.sources.at(-1).starts, [[0, 3, 4]]);
  });
}

test('unlock creates its context during the gesture even without prior prepare', async () => {
  const { audio, context } = fixture();
  await audio.unlock();
  assert.equal(context.state, 'running');
  await audio.prepare();
  audio.update(clock(2));
  assert.equal(context.sources.length, 1);
});

test('context constructor and resume failures never escape', async () => {
  const { audio, context } = fixture();
  context.resume = async () => { throw new Error('blocked'); };
  await audio.prepare(); await assert.doesNotReject(() => audio.unlock());
  assert.doesNotThrow(() => audio.update(clock(1)));
  const unavailable = new StationAudio({ contextFactory: () => { throw new Error('unsupported'); } });
  await assert.doesNotReject(() => unavailable.prepare());
  await assert.doesNotReject(() => unavailable.unlock());
  assert.doesNotThrow(() => unavailable.update(clock(1)));
});

test('late ended events from a stopped source cannot clear the new source', async () => {
  const { audio, context } = fixture();
  await audio.prepare(); await audio.unlock();
  audio.update(clock(1));
  const oldSource = context.sources[0];
  audio.update(clock(2, { startMs: 2000 }));
  oldSource.onended?.();
  assert.equal(audio.getState().activeKey, JSON.stringify([2000, 'ident-1']));
});

test('prepare decodes the three local variants without playing or resuming', async () => {
  const urls = [];
  const { audio, context } = fixture({ fetcher: url => { urls.push(String(url)); return localFetch(); } });
  await audio.prepare();
  assert.deepEqual(audio.getState().readyVariants.sort(), ['next', 'night', 'station']);
  assert.equal(context.state, 'suspended');
  assert.equal(context.sources.length, 0);
  assert.ok(urls.every(url => url.endsWith('.mp3') && url.includes('/assets/audio/ident-')));
  assert.equal(urls.length, 3);
});
