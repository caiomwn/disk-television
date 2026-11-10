import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {compileSchedule, locate, guide} from '../src/schedule.js';

const catalog=JSON.parse(fs.readFileSync(new URL('../data/catalog.json',import.meta.url)));
const config=JSON.parse(fs.readFileSync(new URL('../data/schedule.json',import.meta.url)));
const slots=compileSchedule(config,catalog);
const epoch=Date.parse(config.epoch);

test('production cycle covers exactly 24h with unique ids, no gaps and three ident variants',()=>{
  assert.equal(config.cycleSeconds,86400);
  assert.equal(slots[0].start,0);
  let end=0;
  for(const slot of slots){assert.equal(slot.start,end);assert.ok(slot.duration>0);end+=slot.duration;}
  assert.equal(end,86400);
  assert.equal(new Set(slots.map(s=>s.id)).size,slots.length);
  for(const variant of ['station','next','night'])assert.ok(slots.some(s=>s.variant===variant));
  for(const item of catalog){
    assert.match(item.youtubeId,/^[A-Za-z0-9_-]{11}$/);
    assert.ok(Number.isInteger(item.durationSeconds));
    if(item.broadcastEnabled===false){
      assert.ok(item.offAirReason,'Off-air reserve must have an editorial reason');
      assert.ok(!slots.some(s=>s.contentId===item.id),'Off-air reserve leaked into the schedule');
    }else assert.ok(slots.some(s=>s.contentId===item.id));
    assert.equal(item.sourceUrl,`https://www.youtube.com/watch?v=${item.youtubeId}`);
  }
});

test('every second of the day resolves consistently on reopen and next day',()=>{
  for(let second=0;second<86400;second++){
    const now=epoch+second*1000;
    const current=locate(slots,epoch,now);
    assert.equal(current.elapsed,second-current.slot.start);
    assert.ok(current.remaining>0);
    const tomorrow=locate(slots,epoch,now+86400000);
    assert.equal(tomorrow.slot.id,current.slot.id);
    assert.equal(tomorrow.elapsed,current.elapsed);
    assert.deepEqual(current,locate(slots,epoch,now));
  }
});

test('full videos are preserved, upcoming announces its own video and guide crosses midnight',()=>{
  for(let i=0;i<slots.length;i++){
    const slot=slots[i];
    if(slot.type==='video')assert.equal(slot.duration,catalog.find(c=>c.id===slot.contentId).durationSeconds);
    if(slot.variant==='next'){assert.equal(slots[i+1].type,'video');assert.equal(slot.nextTitle,slots[i+1].title);}
  }
  const midnight=epoch+86400000;
  const before=locate(slots,epoch,midnight-1);
  assert.equal(before.endMs,midnight);
  const after=locate(slots,epoch,midnight);
  assert.equal(after.elapsed,0);assert.equal(after.index,0);
  const rows=guide(slots,epoch,midnight-1,4);
  assert.equal(rows[1].startMs,midnight);
});
