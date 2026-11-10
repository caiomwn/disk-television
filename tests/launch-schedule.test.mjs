import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {compileSchedule, locate} from '../src/schedule.js';
const catalog=[{id:'a',youtubeId:'AAAAAAAAAAA',title:'Alpha',durationSeconds:40},{id:'b',youtubeId:'BBBBBBBBBBB',title:'Beta',durationSeconds:20}];
const config={epoch:'2026-01-01T03:00:00Z',cycleSeconds:100,idents:{station:3,next:2,night:4},blocks:[{start:0,label:'Orbit',rotation:['a','b']}],continuityMode:'block-opening-short-links',blockOpeningSeconds:18,programmeLinkSeconds:4};
const production=JSON.parse(fs.readFileSync(new URL('../data/schedule.json',import.meta.url)));
const productionCatalog=JSON.parse(fs.readFileSync(new URL('../data/catalog.json',import.meta.url)));
test('launch never repeats the identical work back-to-back',()=>{
 const videos=compileSchedule(production,productionCatalog).filter(s=>s.type==='video');
 for(let i=1;i<videos.length;i++)assert.notEqual(videos[i].contentId,videos[i-1].contentId,'unnecessary adjacent repeat');
});
test('launch dataset opts in and never broadcasts three consecutive episodes of one series',()=>{
 assert.equal(production.continuityMode,'block-opening-short-links');
 assert.equal(production.blockOpeningSeconds,18); assert.equal(production.programmeLinkSeconds,4);
 const byId=new Map(productionCatalog.map(i=>[i.id,i])); let previous=null,run=0;
 for(const slot of compileSchedule(production,productionCatalog).filter(s=>s.type==='video')){
  const item=byId.get(slot.contentId); const series=item.kind==='episode'?item.series:null;
  run=series&&series===previous?run+1:1; previous=series;
  assert.ok(run<=2,`${slot.block}: ${item.title} is consecutive episode ${run}`);
 }
});
test('opt-in validates positive integer continuity durations and exact-fit opening overhead',()=>{
 for(const key of ['blockOpeningSeconds','programmeLinkSeconds'])for(const value of [undefined,0,-1,1.5,NaN])assert.throws(()=>compileSchedule({...config,[key]:value},catalog),/continuidade|vinheta/i);
 const tiny=[{...catalog[0],durationSeconds:2}];
 const exact={...config,cycleSeconds:20,idents:{station:100,next:100,night:100},blocks:[{start:0,label:'Exact',rotation:['a']}]};
 assert.equal(compileSchedule(exact,tiny).at(-1).start,18);
 assert.throws(()=>compileSchedule({...exact,cycleSeconds:19},tiny),/cabe/i);
});
test('opt-in opens each block once and links directly to complete programmes',()=>{
 const slots=compileSchedule(config,catalog);
 assert.deepEqual(slots.map(s=>[s.start,s.duration,s.type,s.variant,s.role]),[[0,18,'ident','night','block-opening'],[18,40,'video',undefined,undefined],[58,4,'ident','next','programme-link'],[62,20,'video',undefined,undefined],[82,18,'ident','continuity',undefined]]);
 assert.equal(slots[0].title,'Orbit'); assert.equal(slots[0].nextTitle,'Alpha'); assert.equal(slots[2].nextTitle,'Beta');
 const epoch=Date.parse(config.epoch); assert.equal(locate(slots,epoch,epoch+28000).elapsed,10); assert.equal(locate(slots,epoch,epoch+100000).index,0);
});
