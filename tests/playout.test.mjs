import test from 'node:test';
import assert from 'node:assert/strict';
import {Playout} from '../src/playout.js';

test('player events distinguish buffering, pause, autoplay blocking, end and retry', () => {
  let stopped=0;
  const playout = new Playout({load:()=>{},stop:()=>stopped++});
  const clock={slot:{id:'one',type:'video',videoId:'abcdefghijk'},elapsed:0,startMs:0};
  playout.sync(clock,0);
  playout.state(1,100);
  assert.equal(playout.sync(clock,30000),'playing');
  playout.state(3,30001);
  assert.equal(playout.sync(clock,51001),'unavailable');
  playout.retry();
  assert.equal(playout.sync(clock,52000),'loading');
  playout.state(2,53000);
  assert.equal(playout.sync(clock,100000),'paused');
  playout.blocked();
  assert.equal(playout.sync(clock,200000),'blocked');
  playout.state(0,210000);
  assert.equal(playout.status,'unavailable');
  assert.equal(stopped,2);
});

test('a player that never starts times out without freezing the schedule', () => {
  const player = {load:()=>{},stop:()=>{}};
  const playout = new Playout(player);
  const clock = {slot:{id:'one',type:'video',videoId:'abcdefghijk'},elapsed:4,startMs:0};
  playout.sync(clock,1000);
  assert.equal(playout.sync(clock,21999),'loading');
  assert.equal(playout.sync(clock,22000),'unavailable');
});

test('failed video holds continuity until the next wall-clock slot, then recovers', () => {
  const calls = [];
  const player = {load:(...args)=>calls.push(args),stop:()=>calls.push('stop')};
  const playout = new Playout(player);
  const clock = {slot:{id:'a',type:'video',videoId:'abcdefghijk'},startMs:0,elapsed:12};
  playout.sync(clock,0);
  playout.fail(150);
  assert.equal(playout.sync({...clock,elapsed:50},50000),'unavailable');
  assert.equal(calls.length,2);
  playout.sync({slot:{id:'b',type:'video',videoId:'ABCDEFGHIJK'},startMs:60000,elapsed:3},63000);
  assert.equal(playout.status,'loading');
  assert.deepEqual(calls.at(-1),['ABCDEFGHIJK',3]);
});

// Import dynamically so missing implementation is an assertion, not a syntax error.
test('joining a scheduled video loads its current offset, not its beginning', async () => {
  const module = await import('../src/playout.js').catch(() => null);
  assert.ok(module?.Playout, 'Playout must exist');
  const calls = [];
  const player = {load: (...args) => calls.push(args), stop: () => {}};
  const clock = {slot:{id:'one',type:'video',videoId:'12345678901',title:'Film'},elapsed:1320};
  const playout = new module.Playout(player);
  playout.sync(clock, 1000);
  assert.deepEqual(calls, [['12345678901', 1320]]);
  playout.sync({...clock,elapsed:1321},2000);
  assert.equal(calls.length, 1);
});
