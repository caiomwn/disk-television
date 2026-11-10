import test from 'node:test';
import assert from 'node:assert/strict';
import * as engine from '../src/schedule.js';

const catalog = [
  { id: 'a', youtubeId: 'AAAAAAAAAAA', title: 'Alpha', durationSeconds: 40 },
  { id: 'b', youtubeId: 'BBBBBBBBBBB', title: 'Beta', durationSeconds: 20 },
];
const config = {
  epoch: '2026-01-01T03:00:00Z', cycleSeconds: 100,
  blocks: [{ start: 0, label: 'Órbita', rotation: ['a', 'b'] }],
  idents: { station: 3, next: 2, night: 4 },
};

test('compiles complete videos with preceding idents and exact continuity fill', () => {
  const slots = engine.compileSchedule(config, catalog);
  assert.deepEqual(slots.map(s => [s.start,s.duration,s.type,s.variant]), [
    [0,4,'ident','night'], [4,2,'ident','next'], [6,40,'video',undefined],
    [46,4,'ident','night'], [50,2,'ident','next'], [52,20,'video',undefined],
    [72,28,'ident','continuity'],
  ]);
  assert.equal(slots[1].nextTitle, 'Alpha');
  assert.equal(slots[2].videoId, 'AAAAAAAAAAA');
  assert.equal(slots[2].contentId, 'a');
  assert.equal(slots[2].title, 'Alpha');
  assert.equal(slots[2].block, 'Órbita');
  assert.equal(slots.at(-1).title, 'Intervalo orbital');
  assert.equal(new Set(slots.map(s => s.id)).size, slots.length);
});

test('accepts wrapped catalogs and produces identical reloads without mutating inputs', () => {
  const before = JSON.stringify({config, catalog});
  const first = engine.compileSchedule(config, {items: catalog});
  assert.deepEqual(first, engine.compileSchedule(structuredClone(config), structuredClone(catalog)));
  assert.equal(JSON.stringify({config, catalog}), before);
});

test('locates wall-clock boundaries and wraps before epoch and midnight', () => {
  const slots=engine.compileSchedule(config,catalog), epoch=Date.parse(config.epoch);
  assert.equal(typeof engine.locate,'function');
  const join=engine.locate(slots,epoch,epoch+28000);
  assert.equal(join.slot.title,'Alpha');
  assert.equal(join.elapsed,22);
  assert.equal(join.remaining,18);
  assert.equal(join.startMs,epoch+6000);
  assert.equal(join.endMs,epoch+46000);
  assert.equal(join.next.variant,'night');
  assert.equal(engine.locate(slots,epoch,epoch+46000).elapsed,0);
  assert.equal(engine.locate(slots,epoch,epoch+100000).index,0);
  assert.equal(engine.locate(slots,epoch,epoch-1000).elapsed,27);
  assert.equal(engine.locate(slots,epoch,epoch-1000).cycleStartMs,epoch-100000);
});

test('rejects invalid cycles, epochs, blocks, idents and missing or unplayable rotations', () => {
  for (const value of [null, {...config,epoch:'no-date'}, {...config,cycleSeconds:0},
    {...config,blocks:[]}, {...config,blocks:[{...config.blocks[0],start:1}]},
    {...config,blocks:[config.blocks[0],config.blocks[0]]},
    {...config,blocks:[{...config.blocks[0],rotation:[]}]},
    {...config,blocks:[{...config.blocks[0],rotation:['missing']}]},
    {...config,idents:{...config.idents,next:0}},
    {...config,cycleSeconds:10}]) {
    assert.throws(()=>engine.compileSchedule(value,catalog),/grade|config|bloco|época|ciclo|vinheta|rotação|cabe|ident/i);
  }
});

test('guide continues across cycle boundaries and marks only the current slot', () => {
  assert.equal(typeof engine.guide,'function');
  const slots=engine.compileSchedule(config,catalog), epoch=Date.parse(config.epoch);
  const rows=engine.guide(slots,epoch,epoch+99000,4);
  assert.equal(rows.length,4);
  assert.equal(rows[0].isCurrent,true);
  assert.equal(rows[0].slot.variant,'continuity');
  assert.equal(rows[1].startMs,epoch+100000);
  assert.equal(rows[1].isCurrent,false);
  assert.equal(rows[2].startMs,rows[1].endMs);
  assert.throws(()=>engine.locate(slots,NaN,epoch),/relógio/i);
});

test('rejects malformed YouTube tokens and fractional durations without repairing them',()=>{
  for(const youtubeId of ['bad','https://www.youtube.com/watch?v=AAAAAAAAAAA',' AAAAAAAAAAA','AAAAAAAAAAA ',null]){
    assert.throws(()=>engine.compileSchedule(config,[{...catalog[0],youtubeId},catalog[1]]),/YouTube|catálogo/i);
  }
  assert.throws(()=>engine.compileSchedule(config,[{...catalog[0],durationSeconds:1.5},catalog[1]]),/duração/i);
});

test('rejects malformed catalog IDs and nonpositive or nonfinite durations', () => {
  for (const invalid of [null, {}, [], [{...catalog[0], id: ''}], [{...catalog[0], id: 3}],
    [catalog[0],catalog[0]], ...[0,-1,NaN,Infinity,'40'].map(durationSeconds => [{...catalog[0],durationSeconds}])]) {
    assert.throws(() => engine.compileSchedule(config, invalid), /catálogo|catalog|id|dura/i);
  }
});
