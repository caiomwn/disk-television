// The wall clock owns the programme; the player is only an output device.
export class Playout {
  constructor(player) { this.player = player; this.key = null; this.status = 'idle'; }
  retry() { this.key = null; }
  blocked() { if (this.status !== 'ident') this.status = 'blocked'; }
  state(code, nowMs) {
    if (['ident', 'unavailable', 'idle'].includes(this.status)) return;
    if (code === 0) this.fail('ended');
    else if (code === 1) this.status = 'playing';
    else if (code === 2) this.status = 'paused';
    else if (code === 3) {
      if (this.status !== 'loading') this.pendingSince = nowMs;
      this.status = 'loading';
    }
  }
  fail(reason) {
    this.reason = String(reason);
    this.status = 'unavailable';
    this.player.stop();
  }
  sync(clock, nowMs) {
    const key = `${clock.startMs ?? ''}:${clock.slot.id}`;
    if (key !== this.key) {
      this.key = key;
      this.pendingSince = nowMs;
      this.status = clock.slot.type === 'video' ? 'loading' : 'ident';
      if (clock.slot.type === 'video') this.player.load(clock.slot.videoId, clock.elapsed);
      else this.player.stop();
    }
    if (this.status === 'loading' && nowMs - this.pendingSince >= 21000) this.fail('timeout');
    return this.status;
  }
}
