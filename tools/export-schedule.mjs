// Optional documentation export. Application runtime reads the JSON directly.
import fs from 'node:fs';
import {compileSchedule} from '../src/schedule.js';
const base=new URL('../',import.meta.url);
const config=JSON.parse(fs.readFileSync(new URL('data/schedule.json',base)));
const catalog=JSON.parse(fs.readFileSync(new URL('data/catalog.json',base)));
const slots=compileSchedule(config,catalog);
fs.mkdirSync(new URL('docs/evidence/dt002/',base),{recursive:true});
fs.writeFileSync(new URL('docs/evidence/dt002/compiled-schedule.json',base),JSON.stringify(slots,null,2)+'\n');
const hhmmss=s=>[Math.floor(s/3600),Math.floor(s/60)%60,s%60].map(n=>String(n).padStart(2,'0')).join(':');
const csv=value=>'"'+String(value??'').replaceAll('"','""')+'"';
const header=['inicio_brasilia','fim_brasilia','tipo','variante','titulo','bloco','youtube_id'];
const rows=slots.map(s=>[hhmmss(s.start),hhmmss(s.start+s.duration),s.type,s.variant,s.variant==='next'?`A seguir: ${s.nextTitle}`:s.title,s.block,s.videoId]);
fs.writeFileSync(new URL('docs/GRADE.csv',base),'\uFEFF'+[header,...rows].map(r=>r.map(csv).join(',')).join('\n')+'\n');
fs.writeFileSync(new URL('docs/GRADE.md',base),'# DISK TELEVISION — grade de 24 horas\n\nHorários de Brasília. Gerado a partir dos JSON editáveis; rode `node tools/export-schedule.mjs` para atualizar esta cópia. As vinhetas fazem parte dos horários. O CSV contém os mesmos slots.\n\n| Início | Fim | Atração / continuidade | Bloco |\n|---|---|---|---|\n'+rows.map(r=>`| ${r[0]} | ${r[1]} | ${r[4]} | ${r[5]} |`).join('\n')+'\n');
const totals={catalogItems:catalog.length,uniqueContentSeconds:catalog.reduce((n,c)=>n+c.durationSeconds,0),cycleSeconds:config.cycleSeconds,blocks:config.blocks.length,slots:slots.length,videoSlots:slots.filter(s=>s.type==='video').length,identSlots:slots.filter(s=>s.type==='ident').length,continuityFillSeconds:slots.filter(s=>s.variant==='continuity').reduce((n,s)=>n+s.duration,0),variantCounts:Object.fromEntries(['station','next','night','continuity'].map(v=>[v,slots.filter(s=>s.variant===v).length]))};
fs.writeFileSync(new URL('docs/evidence/schedule-summary.json',base),JSON.stringify(totals,null,2)+'\n');
console.log(JSON.stringify(totals,null,2));
