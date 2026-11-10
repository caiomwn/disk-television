import {compileSchedule, locate} from './schedule.js';
import {Playout} from './playout.js';
import {PresentationController} from './presentation.js';
import {StationAudio} from './station-audio.js';

const $ = id => document.getElementById(id);
const timeFormat = new Intl.DateTimeFormat('pt-BR',{timeZone:'America/Sao_Paulo',hour:'2-digit',minute:'2-digit',hourCycle:'h23'});
const clockFormat = new Intl.DateTimeFormat('pt-BR',{timeZone:'America/Sao_Paulo',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'});
let config, catalog, slots, epoch, tuned=false, player=null, playerReady=false, apiPromise=null;
let playout, lastSlotKey='', guideOpen=false, muted=false, lastGuideIndex=-1;
const stationAudio=new StationAudio({baseUrl:new URL('./assets/audio/',document.baseURI)});
let connection=null;
let suspendedForView=false;
let clock;
let presentationOpen=false;
const seconds = value => `${Math.floor(value/60)}:${String(Math.floor(value%60)).padStart(2,'0')}`;
const setText = (id,text) => { if ($(id).textContent!==String(text)) $(id).textContent=text; };

function pictureVisible(){
  const frame=$('youtube-player');
  const frameRect=frame?.getBoundingClientRect();
  const rect=frameRect?.width && frameRect?.height ? frameRect : $('stage').getBoundingClientRect();
  const width=Math.max(0,Math.min(innerWidth,rect.right)-Math.max(0,rect.left));
  const height=Math.max(0,Math.min(innerHeight,rect.bottom)-Math.max(0,rect.top));
  return !document.hidden && !guideOpen && !presentationOpen && rect.width>=200 && rect.height>=200 && width*height/(rect.width*rect.height)>.5;
}

function loadYouTube() {
  if (window.YT?.Player) return Promise.resolve();
  if (apiPromise) return apiPromise;
  apiPromise=new Promise((resolve,reject)=>{
    const timer=setTimeout(()=>{apiPromise=null;script.remove();reject(new Error('A API do YouTube não respondeu.'));},12000);
    window.onYouTubeIframeAPIReady=()=>{clearTimeout(timer);resolve();};
    const script=document.createElement('script');
    script.src='https://www.youtube.com/iframe_api';
    script.onerror=()=>{clearTimeout(timer);apiPromise=null;script.remove();reject(new Error('Não foi possível acessar o YouTube.'));};
    document.head.append(script);
  });
  return apiPromise;
}

const adapter={
  load(videoId,offset){
    if (!playerReady || !pictureVisible()) return;
    $('player-shell').hidden=false;
    player.loadVideoById({videoId,startSeconds:Math.max(0,offset)});
  },
  stop(){ if(playerReady) player.stopVideo(); }
};

async function connectPlayer() {
  await loadYouTube();
  if (playerReady) return;
  await new Promise((resolve,reject)=>{
    const timeout=setTimeout(()=>{player?.destroy();player=null;playerReady=false;$('player-shell').innerHTML='<div id="youtube-player"></div>';reject(new Error('O player não respondeu.'));},15000);
    player=new window.YT.Player('youtube-player',{
      width:'100%',height:'100%',
      playerVars:{autoplay:0,controls:1,playsinline:1,rel:0,fs:1,origin:location.origin,hl:'pt',mute:muted?1:0},
      events:{
        onReady(){clearTimeout(timeout);playerReady=true; muted?player.mute():player.unMute(); resolve();},
        onStateChange(event){
          if (!playout || guideOpen || presentationOpen || suspendedForView || document.hidden) return;
          playout.state(event.data,Date.now());
          renderSignal();
        },
        onError(event){ if(playout && clock?.slot.type==='video' && !guideOpen){playout.fail(`YouTube ${event.data}`);renderSignal();} },
        onAutoplayBlocked(){ if(playout){playout.blocked();renderSignal();} }
      }
    });
  });
}

function ensureConnected(){
  if(playerReady)return Promise.resolve();
  if(connection)return connection;
  connection=connectPlayer().then(()=>{
    if(tuned && !guideOpen && !presentationOpen && !document.hidden){playout.retry();tick();}
  }).catch(error=>{
    if(playout){playout.fail(error.message);renderSignal();}
  }).finally(()=>{connection=null;});
  return connection;
}

function unlockAudio(){
  // Resume inside the interaction, before asynchronous file fetch/decode.
  stationAudio.unlock();stationAudio.prepare();
}

function nextVideo(index){
  for(let i=1;i<=slots.length;i++){
    const next=slots[(index+i)%slots.length];
    if(next.type==='video')return next;
  }
  return null;
}

function tick(){
  const now=Date.now();
  setText('clock',clockFormat.format(now));
  if(!slots)return;
  clock=locate(slots,epoch,now);
  const {slot,elapsed,startMs,endMs,index}=clock;
  $('app').style.setProperty('--block-color',slot.block.includes('CYBERIA')?'#a1d9e5':slot.block.includes('MOE')?'#d8a6c6':slot.block.includes('AFTER')?'#afa2d6':'#b6c3de');
  const key=`${startMs}:${slot.id}`;
  $('stage').dataset.slotId=slot.id;
  $('stage').dataset.slotType=slot.type;
  $('stage').dataset.elapsed=String(elapsed);
  $('stage').dataset.startMs=String(startMs);
  $('stage').dataset.endMs=String(endMs);
  setText('now-title',slot.title);
  const item=catalog.find(item=>item.id===slot.contentId);
  setText('now-meta',item?`${slot.block} · ${item.creator} · ${item.year}`:`${slot.block} · Continuidade original`);
  const next=nextVideo(index);
  setText('next-title',next?.title||'DISK TELEVISION');
  let nextStart=clock.cycleStartMs+(next?.start||0)*1000;
  if(nextStart<=startMs)nextStart+=config.cycleSeconds*1000;
  setText('next-time',`Às ${timeFormat.format(nextStart)} · ${next?.block||'CH 99'}`);
  setText('slot-start',timeFormat.format(startMs));setText('slot-end',timeFormat.format(endMs));
  $('progress').style.width=`${100*elapsed/slot.duration}%`;
  if(tuned && !guideOpen && !presentationOpen && !document.hidden){
    if(!pictureVisible()){
      if(!suspendedForView){suspendedForView=true;adapter.stop();playout?.retry();}
      stationAudio.stop();
      setText('station-state','SINAL EM ESPERA');
      return;
    }
    if(suspendedForView){suspendedForView=false;playout?.retry();lastSlotKey='';}
    if(playout && (playerReady || slot.type==='ident')) playout.sync(clock,now);
    if(key!==lastSlotKey){
      lastSlotKey=key;
      if(slot.type==='video' && !playerReady)ensureConnected();
      if(slot.type==='ident'){
        $('continuity').dataset.role=slot.role||'';
        $('continuity').dataset.variant=slot.variant==='continuity'?'night':slot.variant;
        setText('ident-label',slot.role==='block-opening'?'ABERTURA DE BLOCO / CH 99':slot.variant==='next'?'NA SEQUÊNCIA':slot.variant==='night'?'FREQUÊNCIA NOTURNA':slot.variant==='continuity'?'INTERVALO ORBITAL':'IDENTIFICAÇÃO / CH 99');
        setText('ident-title',slot.role==='block-opening'?slot.block:slot.variant==='next'?slot.nextTitle:slot.variant==='night'?'Para quem ainda está acordado.':slot.variant==='continuity'?'O sinal permanece.':'Uma frequência fora do tempo.');
        setText('ident-subtitle',slot.variant==='next'?'FIQUE NA FREQUÊNCIA':slot.variant==='night'?'A NOITE NÃO TERMINA AQUI.':'DISK TELEVISION · TRANSMISSÃO CONTÍNUA');

      }
    }
    renderSignal();
  }
  stationAudio.update(clock,{enabled:tuned&&!muted&&!guideOpen&&!presentationOpen&&!document.hidden&&pictureVisible()});
  const soundState=stationAudio.getState();
  $('app').dataset.audioState=soundState.contextState;
  $('app').dataset.audioStarts=String(soundState.starts);
  $('app').dataset.audioActive=String(Boolean(soundState.activeKey));
  $('app').dataset.audioVariants=soundState.readyVariants.join(',');
  if(guideOpen && lastGuideIndex!==index)renderGuide();
}

function renderSignal(){
  if(!clock || !tuned || guideOpen || presentationOpen || suspendedForView)return;
  const status=playout?.status||'connecting';
  const ident=clock.slot.type==='ident';
  const fallback=!ident && ['unavailable','connecting','idle'].includes(status);
  $('player-shell').hidden=ident || fallback || !playerReady;
  $('continuity').hidden=!ident && !fallback;
  $('reception').hidden=ident || status==='playing';
  setText('station-state',ident?'CONTINUIDADE':status==='playing'?'NO AR':status==='loading'?'RECEBENDO SINAL':'SINTONIZADO');
  if(fallback){
    $('continuity').dataset.variant='unavailable';
    setText('ident-label',status==='unavailable'?'CONTINUIDADE / CH 99':'CONECTANDO / CH 99');
    setText('ident-title',status==='unavailable'?'O sinal continua.':'Estabelecendo contato.');
    setText('ident-subtitle',status==='unavailable'?'ESTA ATRAÇÃO NÃO RESPONDEU. A PRÓXIMA ENTRA NO HORÁRIO.':'O RELÓGIO DA EMISSORA NÃO PARA.');
  }
  setText('ident-block',clock.slot.block);
  setText('ident-countdown',`PRÓXIMA TRANSMISSÃO EM ${seconds(clock.remaining)}`);
  $('continuity').style.setProperty('--ident-progress',clock.elapsed/clock.slot.duration);
  const descriptions={loading:'Recebendo o sinal do YouTube…',blocked:'O navegador bloqueou a reprodução automática. Use Ressintonizar ou o botão do player.',paused:'O vídeo está pausado. Ressintonize para voltar ao horário da emissora.',unavailable:`Atração indisponível (${playout?.reason||'conexão'}). A grade segue automaticamente.`,connecting:'Conectando ao YouTube…',idle:'Conectando ao YouTube…'};
  setText('reception-text',descriptions[status]||'');
  $('retry').disabled=status==='connecting';
}

async function tune(){
  unlockAudio();
  if(playerReady && pictureVisible()){muted?player.mute():player.unMute();}
  tuned=true;$('gate').hidden=true;
  presentation.setOnAir(true);
  window.scrollTo(0,$('stage').offsetTop);
  playout??=new Playout(adapter);
  playout.retry();lastSlotKey='';
  tick();
  $('guide-open').focus({preventScroll:true});
  await ensureConnected();
}

function renderGuide(){
  if(!clock)return;
  const list=$('guide-list');list.replaceChildren();
  const fragment=document.createDocumentFragment();
  for(const [i,slot] of slots.entries()){
    const row=document.createElement('article');
    row.className=`guide-row${i===clock.index?' current':i<clock.index?' past':''}`;
    if(i===clock.index)row.setAttribute('aria-current','true');
    const at=document.createElement('time');at.dateTime=new Date(clock.cycleStartMs+slot.start*1000).toISOString();at.textContent=timeFormat.format(clock.cycleStartMs+slot.start*1000);
    const info=document.createElement('div'), title=document.createElement('h3'), detail=document.createElement('p');
    title.textContent=slot.variant==='next'?`A seguir: ${slot.nextTitle}`:slot.title;
    detail.textContent=slot.type==='video'?`${catalog.find(item=>item.id===slot.contentId)?.creator||''} · ${seconds(slot.duration)}`:`Vinheta original · ${seconds(slot.duration)}`;
    info.append(title,detail);
    const block=document.createElement('span');block.className='guide-block';block.textContent=slot.block;
    const kind=document.createElement('span');kind.className='guide-kind';kind.textContent=i===clock.index?'NO AR':slot.type==='video'?'ATRAÇÃO':'VINHETA';
    row.append(at,info,block,kind);fragment.append(row);
  }
  list.append(fragment);lastGuideIndex=clock.index;
  const current=list.querySelector('.current');
  if(current)list.scrollTop=current.offsetTop-list.offsetTop-30;
}
function showGuide(){
  if(!slots)return;
  guideOpen=true;
  // Replace, rather than overlay, the official player. No hidden background playback.
  adapter.stop();stationAudio.stop();$('player-shell').hidden=true;
  $('main').inert=true;$('main').style.visibility='hidden';
  $('guide').hidden=false;$('guide-open').setAttribute('aria-expanded','true');
  renderGuide();$('guide-close').focus();
}
function closeGuide(){
  guideOpen=false;$('guide').hidden=true;$('main').inert=false;$('main').style.visibility='';
  $('guide-open').setAttribute('aria-expanded','false');
  if(tuned){playout?.retry();lastSlotKey='';tick();}
  $('guide-open').focus({preventScroll:true});
}

$('tune').addEventListener('click',tune);$('retry').addEventListener('click',tune);
$('guide-open').addEventListener('click',showGuide);$('guide-close').addEventListener('click',closeGuide);
$('sound').addEventListener('click',()=>{
  muted=!muted;unlockAudio();
  if(muted)stationAudio.stop();
  tick();
  if(playerReady)muted?player.mute():player.unMute();
  $('sound').setAttribute('aria-pressed',String(muted));
  $('sound').setAttribute('aria-label',muted?'Ativar áudio':'Silenciar áudio');
  setText('sound',muted?'Som desligado':'Som ligado');
});
$('fullscreen').addEventListener('click',async()=>{
  try { if(document.fullscreenElement)await document.exitFullscreen();else await $('app').requestFullscreen(); }
  catch{setText('reception-text','Tela cheia indisponível neste navegador. Use o modo de tela cheia da TV.');$('reception').hidden=false;}
});
document.addEventListener('fullscreenchange',()=>setText('fullscreen',document.fullscreenElement?'Sair da tela cheia':'Tela cheia'));
document.addEventListener('keydown',event=>{
  if(presentationOpen)return;
  if(event.target?.tagName==='IFRAME')return;
  const key=event.key&&event.key!=='Unidentified'?event.key:({37:'ArrowLeft',38:'ArrowUp',39:'ArrowRight',40:'ArrowDown',27:'Escape',10009:'BrowserBack'})[event.keyCode]||'';
  if(key.toLowerCase()==='g'){event.preventDefault();guideOpen?closeGuide():showGuide();}
  if(['Escape','BrowserBack','GoBack'].includes(key)){if(guideOpen){event.preventDefault();closeGuide();}}
  if(guideOpen){
    if(['ArrowDown','ArrowUp','PageDown','PageUp'].includes(key)){
      event.preventDefault();$('guide-list').scrollTop+=key==='ArrowDown'?100:key==='ArrowUp'?-100:key==='PageDown'?450:-450;
    }
    if(key==='Tab'){event.preventDefault();document.activeElement===$('guide-close')?$('guide-list').focus():$('guide-close').focus();}
  } else if(key.startsWith('Arrow')){
    const buttons=[...document.querySelectorAll('button,a[href]')].filter(b=>!b.disabled && b.getClientRects().length && !b.closest('[inert]') && getComputedStyle(b).visibility!=='hidden');
    const index=buttons.indexOf(document.activeElement);
    if(buttons.length){event.preventDefault();buttons[(index+(key==='ArrowLeft'||key==='ArrowUp'?-1:1)+buttons.length)%buttons.length].focus();}
  }
});
document.addEventListener('visibilitychange',()=>{
  if(document.hidden){adapter.stop();stationAudio.stop();}
  else if(tuned && !guideOpen && !presentationOpen){playout?.retry();tick();}
});
window.addEventListener('pageshow',()=>{if(tuned){playout?.retry();tick();}});

async function boot(){
  try{
    const responses=await Promise.all(['./data/catalog.json','./data/schedule.json'].map(url=>fetch(url,{cache:'no-cache'})));
    if(responses.some(response=>!response.ok))throw new Error('Não foi possível ler o catálogo e a grade.');
    const [raw,settings]=await Promise.all(responses.map(response=>response.json()));
    catalog=Array.isArray(raw)?raw:raw.items;config=settings;
    slots=compileSchedule(config,catalog);epoch=Date.parse(config.epoch);
    $('tune').disabled=false;
    setText('boot-message','Uma interação inicia a transmissão. Conteúdos via YouTube.');
    tick();$('tune').focus();
  }catch(error){setText('boot-message',`Falha de sintonia: ${error.message} Abra por HTTP(S), não como arquivo local.`);}
}
const presentation=new PresentationController($('app'),{
  onOpen(){
    presentationOpen=true;
    if(guideOpen)closeGuide();
    adapter.stop();stationAudio.stop();$('player-shell').hidden=true;
    $('main').inert=true;$('main').style.visibility='hidden';
  },
  onClose(){
    presentationOpen=false;$('main').inert=false;$('main').style.visibility='';
    if(tuned){playout?.retry();lastSlotKey='';tick();}
  },
  onModeChange(){if(tuned && !presentationOpen)tick();}
});
setInterval(tick,250);tick();boot();
