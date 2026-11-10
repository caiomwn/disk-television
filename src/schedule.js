/** Compile a repeatable cycle. Times and durations are in seconds. */
export function compileSchedule(config, catalog) {
  const entries = Array.isArray(catalog) ? catalog : catalog?.items;
  if (!Array.isArray(entries) || !entries.length) throw new Error('Catálogo vazio ou inválido');
  const seen = new Set();
  for (const item of entries) {
    if (!item || typeof item.id !== 'string' || !item.id || seen.has(item.id)) throw new Error('ID de catálogo inválido ou duplicado');
    if (!Number.isInteger(item.durationSeconds) || item.durationSeconds <= 0) throw new Error('Duração inválida no catálogo');
    if (typeof item.youtubeId !== 'string' || !/^[A-Za-z0-9_-]{11}$/.test(item.youtubeId)) throw new Error(`ID YouTube inválido no catálogo: ${item.id}`);
    seen.add(item.id);
  }
  const items = new Map(entries.map(item => [item.id, item]));
  if (!config || !Number.isFinite(Date.parse(config.epoch))) throw new Error('Época inválida na configuração');
  if (!Number.isInteger(config.cycleSeconds) || config.cycleSeconds <= 0) throw new Error('Ciclo inválido');
  if (!Array.isArray(config.blocks) || !config.blocks.length || config.blocks[0].start !== 0) throw new Error('Grade deve iniciar no bloco zero');
  for (const key of ['station','next','night']) {
    if (!Number.isInteger(config.idents?.[key]) || config.idents[key] <= 0) throw new Error('Duração de vinheta inválida');
  }
  const shortLinks = config.continuityMode === 'block-opening-short-links';
  if (shortLinks) for (const key of ['blockOpeningSeconds', 'programmeLinkSeconds']) {
    if (!Number.isInteger(config[key]) || config[key] <= 0) throw new Error('Duração de continuidade inválida');
  }
  for (const [i, block] of config.blocks.entries()) {
    const end = config.blocks[i+1]?.start ?? config.cycleSeconds;
    if (!Number.isInteger(block.start) || block.start < 0 || end <= block.start || end > config.cycleSeconds) throw new Error('Blocos fora de ordem ou do ciclo');
    if (!Array.isArray(block.rotation) || !block.rotation.length) throw new Error('Rotação vazia no bloco');
    for (const id of block.rotation) {
      const item=items.get(id);
      if (!item) throw new Error(`Rotação referencia conteúdo inexistente: ${id}`);
      const variant=block.start < 21600 ? 'night' : 'station';
      const overhead = shortLinks ? Math.max(config.blockOpeningSeconds, config.programmeLinkSeconds) : config.idents[variant] + config.idents.next;
      if (item.durationSeconds + overhead > end-block.start) throw new Error(`Vídeo não cabe no bloco: ${id}`);
    }
  }
  const slots = [];
  config.blocks.forEach((block, blockIndex) => {
    const end = config.blocks[blockIndex + 1]?.start ?? config.cycleSeconds;
    let cursor = block.start;
    const add = (duration, type, details) => {
      slots.push({ id: `slot-${blockIndex}-${slots.length}`, start: cursor,
        duration, type, block: block.label, ...details });
      cursor += duration;
    };
    let rotationIndex = 0;
    while (cursor < end) {
      const item = items.get(block.rotation[rotationIndex % block.rotation.length]);
      const variant = cursor < 21600 ? 'night' : 'station';
      const first = rotationIndex === 0;
      const identDuration = shortLinks ? (first ? config.blockOpeningSeconds : config.programmeLinkSeconds) : config.idents[variant];
      const overhead = identDuration + (shortLinks ? 0 : config.idents.next);
      if (cursor + overhead + item.durationSeconds > end) {
        add(end - cursor, 'ident', { variant: 'continuity', title: 'Intervalo orbital' });
        break;
      }
      if (shortLinks) {
        add(identDuration, 'ident', { variant: first ? variant : 'next',
          role: first ? 'block-opening' : 'programme-link',
          title: first ? block.label : 'A seguir', nextTitle: item.title });
      } else {
        add(identDuration, 'ident', { variant, title: 'DISK TELEVISION' });
        add(config.idents.next, 'ident', { variant: 'next', title: 'A seguir', nextTitle: item.title });
      }
      add(item.durationSeconds, 'video', { title: item.title, videoId: item.youtubeId, contentId: item.id });
      rotationIndex++;
    }
  });
  return slots;
}

export function guide(slots, epochMs, nowMs, count = 8) {
  if (!Number.isInteger(count) || count < 0 || count > 10000) throw new Error('Tamanho de guia inválido');
  const rows = [];
  let cursor = nowMs;
  for (let i=0; i<count; i++) {
    const current = locate(slots, epochMs, cursor);
    rows.push({slot:current.slot, startMs:current.startMs, endMs:current.endMs, isCurrent:i===0});
    cursor = current.endMs;
  }
  return rows;
}

export function locate(slots, epochMs, nowMs) {
  if (!slots?.length || !Number.isFinite(epochMs) || !Number.isFinite(nowMs)) throw new Error('Grade ou relógio inválido');
  const cycle = slots.at(-1).start + slots.at(-1).duration;
  const cycleStartMs = epochMs + Math.floor((nowMs - epochMs) / (cycle * 1000)) * cycle * 1000;
  const position = (nowMs - cycleStartMs) / 1000;
  const index = slots.findIndex(s => position >= s.start && position < s.start + s.duration);
  if (index < 0) throw new Error('Lacuna na grade');
  const slot = slots[index];
  const startMs = cycleStartMs + slot.start * 1000;
  return {slot, index, elapsed:(nowMs-startMs)/1000, remaining:slot.duration-(nowMs-startMs)/1000,
    startMs, endMs:startMs+slot.duration*1000, cycleStartMs, next:slots[(index+1)%slots.length]};
}
