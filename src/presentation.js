// One presentation controller; it never selects content or owns programme time.
export class PresentationController {
  constructor(root,{onOpen=()=>{},onClose=()=>{},onModeChange=()=>{},idleMs=4500,storage}={}){
    this.root=root;this.onOpen=onOpen;this.onClose=onClose;this.onModeChange=onModeChange;this.idleMs=idleMs;
    this.onAir=false;this.opened=false;this.collapsing=false;this.timer=null;
    try{this.storage=storage??window.sessionStorage;this.mode=this.storage.getItem('disk-television-presentation')||'B';}catch{this.storage=null;this.mode='B';}
    if(!['A','B','C'].includes(this.mode))this.mode='B';
    this.dialog=document.getElementById('presentation-dialog');
    this.buttons=[...root.querySelectorAll('[data-presentation]')];
    this.buttons.forEach(button=>button.addEventListener('click',()=>this.setMode(button.dataset.presentation)));
    document.getElementById('presentation-open').addEventListener('click',()=>this.showPicker());
    document.getElementById('presentation-close').addEventListener('click',()=>this.closePicker());
    document.getElementById('reveal-controls').addEventListener('click',()=>this.activity());
    root.addEventListener('pointermove',()=>this.activity());
    root.addEventListener('focusin',()=>{if(!this.collapsing)this.activity();});
    document.addEventListener('keydown',event=>{
      this.activity();
      if(!this.opened)return;
      const key=event.key&&event.key!=='Unidentified'?event.key:({37:'ArrowLeft',38:'ArrowUp',39:'ArrowRight',40:'ArrowDown',27:'Escape',10009:'BrowserBack'})[event.keyCode]||'';
      if(['Escape','BrowserBack','GoBack'].includes(key)){event.preventDefault();event.stopImmediatePropagation();this.closePicker();return;}
      const controls=[...this.dialog.querySelectorAll('button')];
      if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Tab'].includes(key)){
        event.preventDefault();event.stopImmediatePropagation();
        const backwards=['ArrowLeft','ArrowUp'].includes(key)||(key==='Tab'&&event.shiftKey);
        const index=controls.indexOf(document.activeElement);
        controls[(index+(backwards?-1:1)+controls.length)%controls.length].focus({preventScroll:true});
      }
    },true);
    this.setMode(this.mode,false);
  }
  setMode(mode,persist=true){
    if(!['A','B','C'].includes(mode))return;
    this.mode=mode;this.root.dataset.presentation=mode;
    this.buttons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.presentation===mode)));
    document.getElementById('presentation-current').textContent=`PLAYER ${mode} / ${mode==='A'?'CLEAN':mode==='B'?'BROADCAST FRAME':'EXPERIMENTAL'}`;
    if(persist){try{this.storage?.setItem('disk-television-presentation',mode);}catch{}}
    this.activity();this.onModeChange(mode);
  }
  setOnAir(value){this.onAir=value;this.root.classList.toggle('is-tuned',value);this.activity();}
  setChrome(hidden){
    this.root.classList.toggle('chrome-hidden',hidden);this.root.dataset.chrome=hidden?'hidden':'visible';
    for(const element of [this.root.querySelector('.station-bar'),this.root.querySelector('.programme-bar')])element.inert=hidden;
    if(hidden){this.collapsing=true;document.getElementById('reveal-controls').focus({preventScroll:true});this.collapsing=false;}
  }
  activity(){
    clearTimeout(this.timer);this.setChrome(false);
    if(this.mode==='A'&&this.onAir&&!this.opened){
      this.timer=setTimeout(()=>{
        if(!document.getElementById('guide').hidden||this.opened)return;
        this.setChrome(true);
      },this.idleMs);
    }
  }
  showPicker(){
    this.opened=true;this.activity();this.onOpen();this.dialog.hidden=false;
    this.dialog.querySelector(`[data-presentation="${this.mode}"]`).focus({preventScroll:true});
    document.getElementById('presentation-open').setAttribute('aria-expanded','true');
  }
  closePicker(){
    this.opened=false;this.dialog.hidden=true;this.onClose();this.activity();
    document.getElementById('presentation-open').setAttribute('aria-expanded','false');
    document.getElementById('presentation-open').focus({preventScroll:true});
  }
}
