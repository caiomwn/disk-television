export class StationAudio {
  constructor({ contextFactory, fetcher, baseUrl } = {}) {
    this.contextFactory = contextFactory ?? (() => {
      const Context = globalThis.AudioContext ?? globalThis.webkitAudioContext;
      return Context ? new Context() : null;
    });
    this.fetcher = fetcher ?? globalThis.fetch?.bind(globalThis);
    this.baseUrl = baseUrl ?? new URL('./assets/audio/', globalThis.document?.baseURI ?? 'http://localhost/');
    this.context = null;
    this.buffers = new Map();
    this.errorCount = 0;
    this.starts = 0;
    this.activeKey = null;
  }

  prepare() {
    return this.preparation ??= this.load();
  }

  async load() {
    try {
      this.context ??= this.contextFactory();
      if (!this.context || !this.fetcher) return;
      await Promise.all(['station', 'next', 'night'].map(async variant => {
        for (const extension of ['mp3', 'wav']) {
          try {
            const response = await this.fetcher(new URL(`ident-${variant}.${extension}`, this.baseUrl));
            if (!response.ok) throw new Error('Audio fetch failed');
            const buffer = await this.context.decodeAudioData(await response.arrayBuffer());
            if (!buffer || !(buffer.duration > 0)) throw new Error('Invalid audio buffer');
            this.buffers.set(variant, buffer);
            return;
          } catch { this.errorCount++; }
        }
      }));
    } catch {
      this.errorCount++;
    }
  }

  async unlock() {
    try {
      // Create/resume synchronously before the first await to preserve the gesture.
      this.context ??= this.contextFactory();
      await this.context?.resume();
    } catch { this.errorCount++; }
  }

  update(clock, { enabled = true } = {}) {
    const { slot, elapsed, startMs } = clock;
    if (!enabled || slot.type !== 'ident') { this.stop(); return; }
    const key = JSON.stringify([startMs, slot.id]);
    if (this.playedKey === key) return;
    // A slot transition always silences the old ident, even if the new one is not ready.
    if (this.source) this.stop();
    if (this.context?.state !== 'running') return;
    const variant = slot.variant === 'continuity' ? 'night' : slot.variant;
    const buffer = this.buffers.get(variant);
    if (!buffer) return;
    const end = Math.min(buffer.duration, slot.duration, variant === 'next' ? 4 : 18);
    if (!Number.isFinite(elapsed) || elapsed < 0 || !(end > elapsed)) return;
    let source;
    try {
      source = this.context.createBufferSource();
      source.buffer = buffer;
      source.connect(this.context.destination);
      source.onended = () => {
        try { source.disconnect(); } catch { this.errorCount++; }
        if (this.source === source) {
          this.source = null;
          this.activeKey = null;
        }
        // Keep playedKey: natural completion is not permission to replay a filler.
      };
      source.start(0, elapsed, end - elapsed);
      this.source = source;
      this.playedKey = key;
      this.activeKey = key;
      this.starts++;
    } catch {
      this.errorCount++;
      if (source) {
        source.onended = null;
        try { source.stop(); } catch { /* A source that never started may reject stop. */ }
        try { source.disconnect(); } catch { /* Best-effort cleanup. */ }
      }
    }
  }

  stop() {
    const source = this.source;
    this.source = null;
    this.activeKey = null;
    this.playedKey = null;
    if (!source) return;
    try { source.stop(); } catch { this.errorCount++; }
    try { source.disconnect(); } catch { this.errorCount++; }
  }

  getState() {
    return { readyVariants: [...this.buffers.keys()], activeKey: this.activeKey,
      contextState: this.context?.state ?? 'unavailable', starts: this.starts, errorCount: this.errorCount };
  }
}
