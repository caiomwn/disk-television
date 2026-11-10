import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {compileSchedule} from '../src/schedule.js';
const read = path => JSON.parse(fs.readFileSync(new URL('../'+path,import.meta.url)));
const catalog=read('data/catalog.json');
const config=read('data/schedule.json');
const slots=compileSchedule(config,catalog);
const byId=new Map(catalog.map(item=>[item.id,item]));

test('primary 24h editorial schedule is majority Japanese animation with confirmed playback',()=>{
  const japaneseSeconds=slots.filter(s=>s.type==='video'&&byId.get(s.contentId).isJapaneseAnime===true).reduce((n,s)=>n+s.duration,0);
  assert.ok(japaneseSeconds/config.cycleSeconds>.5,'Japanese animation must occupy more than half of the entire broadcast day, including idents');
  for(const slot of slots.filter(s=>s.type==='video')){
    const item=byId.get(slot.contentId);
    assert.equal(item.broadcastEnabled,true,`${item.id} is not enabled for broadcast`);
    assert.equal(item.verification.status,'VERIFIED',`${item.id} has no real embed verification`);
    assert.equal(item.verification.actualPlayback,true);
    assert.equal(item.completeWork,true);
  }
});

test('episodes progress in order and each reset to episode 1 is an explicit reprise',()=>{
  const last=new Map();
  for(const slot of slots.filter(s=>s.type==='video')){
    const item=byId.get(slot.contentId);
    if(item.kind!=='episode'||!Number.isInteger(item.episodeNumber))continue;
    const previous=last.get(item.series);
    const block=config.blocks.find(b=>b.label===slot.block);
    if(previous===undefined)assert.equal(item.episodeNumber,1,`${item.series} begins in the middle`);
    else if(item.episodeNumber!==previous+1){
      assert.equal(item.episodeNumber,1,`${item.series} skipped or reversed an episode`);
      assert.ok(block.explicitReprises?.includes(item.series),`${item.series} reset without a declared reprise`);
    }
    last.set(item.series,item.episodeNumber);
  }
});

test('daily repetition limits and short continuity fillers are respected',()=>{
  const counts=new Map();
  for(const slot of slots){
    if(slot.type==='video')counts.set(slot.contentId,(counts.get(slot.contentId)||0)+1);
    if(slot.variant==='continuity')assert.ok(slot.duration<=180,'Overlong empty continuity instead of a programme');
  }
  for(const [id,count] of counts)assert.ok(count<=byId.get(id).editorialMaxDailyPlays,`${id} exceeds its daily cap`);
});

test('every catalogue entry has matching real playback evidence; new sources are identified',()=>{
  const evidence=read('docs/evidence/dt002/playback-results.json');
  const original=read('tests/fixtures/dt001/catalog.json');
  const oldIds=new Set(original.map(i=>i.youtubeId));
  assert.equal(new Set(catalog.map(i=>i.youtubeId)).size,catalog.length,'Duplicate YouTube ID');
  assert.equal(new Set(catalog.map(i=>i.id)).size,catalog.length,'Duplicate slug');
  for(const item of catalog){
    const proof=evidence.find(e=>e.youtubeId===item.youtubeId);
    assert.ok(proof?.actualPlayback,`${item.id} missing actual observation`);
    assert.equal(proof.expectedDurationSeconds,item.durationSeconds);
    assert.equal(item.verification.status,'VERIFIED');
    if(!oldIds.has(item.youtubeId)){
      assert.match(item.legitimacy.channelId,/^UC[A-Za-z0-9_-]{22}$/);
      assert.ok(item.legitimacy.evidenceUrl.startsWith('https://'));
      if(item.isJapaneseAnime)assert.equal(item.countryOfOrigin,'JP');
    }
  }
});
