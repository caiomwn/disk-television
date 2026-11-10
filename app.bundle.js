/* Compatibility shims for the Chrome 69 production target; not a TV certification. */
(function(g){
  if(typeof g.globalThis==='undefined')g.globalThis=g;
  if(!Array.prototype.at)Object.defineProperty(Array.prototype,'at',{configurable:true,writable:true,value:function(index){var n=Math.trunc(Number(index)||0);if(n<0)n=this.length+n;return n<0||n>=this.length?undefined:this[n];}});
  if(g.Element&&!Element.prototype.replaceChildren)Element.prototype.replaceChildren=function(){while(this.firstChild)this.removeChild(this.firstChild);for(var i=0;i<arguments.length;i++){var child=arguments[i];this.appendChild(child&&child.nodeType?child:document.createTextNode(String(child)));}};
  if(!Promise.allSettled)Promise.allSettled=function(values){return Promise.all(Array.from(values).map(function(value){return Promise.resolve(value).then(function(result){return {status:'fulfilled',value:result};},function(reason){return {status:'rejected',reason:reason};});}));};
})(typeof window!=='undefined'?window:this);

(() => {
  // src/schedule.js
  function compileSchedule(config2, catalog2) {
    var _a, _b, _c;
    const entries = Array.isArray(catalog2) ? catalog2 : catalog2 == null ? void 0 : catalog2.items;
    if (!Array.isArray(entries) || !entries.length) throw new Error("Catálogo vazio ou inválido");
    const seen = /* @__PURE__ */ new Set();
    for (const item of entries) {
      if (!item || typeof item.id !== "string" || !item.id || seen.has(item.id)) throw new Error("ID de catálogo inválido ou duplicado");
      if (!Number.isInteger(item.durationSeconds) || item.durationSeconds <= 0) throw new Error("Duração inválida no catálogo");
      if (typeof item.youtubeId !== "string" || !/^[A-Za-z0-9_-]{11}$/.test(item.youtubeId)) throw new Error(`ID YouTube inválido no catálogo: ${item.id}`);
      seen.add(item.id);
    }
    const items = new Map(entries.map((item) => [item.id, item]));
    if (!config2 || !Number.isFinite(Date.parse(config2.epoch))) throw new Error("Época inválida na configuração");
    if (!Number.isInteger(config2.cycleSeconds) || config2.cycleSeconds <= 0) throw new Error("Ciclo inválido");
    if (!Array.isArray(config2.blocks) || !config2.blocks.length || config2.blocks[0].start !== 0) throw new Error("Grade deve iniciar no bloco zero");
    for (const key of ["station", "next", "night"]) {
      if (!Number.isInteger((_a = config2.idents) == null ? void 0 : _a[key]) || config2.idents[key] <= 0) throw new Error("Duração de vinheta inválida");
    }
    const shortLinks = config2.continuityMode === "block-opening-short-links";
    if (shortLinks) for (const key of ["blockOpeningSeconds", "programmeLinkSeconds"]) {
      if (!Number.isInteger(config2[key]) || config2[key] <= 0) throw new Error("Duração de continuidade inválida");
    }
    for (const [i, block] of config2.blocks.entries()) {
      const end = (_c = (_b = config2.blocks[i + 1]) == null ? void 0 : _b.start) != null ? _c : config2.cycleSeconds;
      if (!Number.isInteger(block.start) || block.start < 0 || end <= block.start || end > config2.cycleSeconds) throw new Error("Blocos fora de ordem ou do ciclo");
      if (!Array.isArray(block.rotation) || !block.rotation.length) throw new Error("Rotação vazia no bloco");
      for (const id of block.rotation) {
        const item = items.get(id);
        if (!item) throw new Error(`Rotação referencia conteúdo inexistente: ${id}`);
        const variant = block.start < 21600 ? "night" : "station";
        const overhead = shortLinks ? Math.max(config2.blockOpeningSeconds, config2.programmeLinkSeconds) : config2.idents[variant] + config2.idents.next;
        if (item.durationSeconds + overhead > end - block.start) throw new Error(`Vídeo não cabe no bloco: ${id}`);
      }
    }
    const slots2 = [];
    config2.blocks.forEach((block, blockIndex) => {
      var _a2, _b2;
      const end = (_b2 = (_a2 = config2.blocks[blockIndex + 1]) == null ? void 0 : _a2.start) != null ? _b2 : config2.cycleSeconds;
      let cursor = block.start;
      const add = (duration, type, details) => {
        slots2.push({
          id: `slot-${blockIndex}-${slots2.length}`,
          start: cursor,
          duration,
          type,
          block: block.label,
          ...details
        });
        cursor += duration;
      };
      let rotationIndex = 0;
      while (cursor < end) {
        const item = items.get(block.rotation[rotationIndex % block.rotation.length]);
        const variant = cursor < 21600 ? "night" : "station";
        const first = rotationIndex === 0;
        const identDuration = shortLinks ? first ? config2.blockOpeningSeconds : config2.programmeLinkSeconds : config2.idents[variant];
        const overhead = identDuration + (shortLinks ? 0 : config2.idents.next);
        if (cursor + overhead + item.durationSeconds > end) {
          add(end - cursor, "ident", { variant: "continuity", title: "Intervalo orbital" });
          break;
        }
        if (shortLinks) {
          add(identDuration, "ident", {
            variant: first ? variant : "next",
            role: first ? "block-opening" : "programme-link",
            title: first ? block.label : "A seguir",
            nextTitle: item.title
          });
        } else {
          add(identDuration, "ident", { variant, title: "DISK TELEVISION" });
          add(config2.idents.next, "ident", { variant: "next", title: "A seguir", nextTitle: item.title });
        }
        add(item.durationSeconds, "video", { title: item.title, videoId: item.youtubeId, contentId: item.id });
        rotationIndex++;
      }
    });
    return slots2;
  }
  function locate(slots2, epochMs, nowMs) {
    if (!(slots2 == null ? void 0 : slots2.length) || !Number.isFinite(epochMs) || !Number.isFinite(nowMs)) throw new Error("Grade ou relógio inválido");
    const cycle = slots2.at(-1).start + slots2.at(-1).duration;
    const cycleStartMs = epochMs + Math.floor((nowMs - epochMs) / (cycle * 1e3)) * cycle * 1e3;
    const position = (nowMs - cycleStartMs) / 1e3;
    const index = slots2.findIndex((s) => position >= s.start && position < s.start + s.duration);
    if (index < 0) throw new Error("Lacuna na grade");
    const slot = slots2[index];
    const startMs = cycleStartMs + slot.start * 1e3;
    return {
      slot,
      index,
      elapsed: (nowMs - startMs) / 1e3,
      remaining: slot.duration - (nowMs - startMs) / 1e3,
      startMs,
      endMs: startMs + slot.duration * 1e3,
      cycleStartMs,
      next: slots2[(index + 1) % slots2.length]
    };
  }

  // src/playout.js
  var Playout = class {
    constructor(player2) {
      this.player = player2;
      this.key = null;
      this.status = "idle";
    }
    retry() {
      this.key = null;
    }
    blocked() {
      if (this.status !== "ident") this.status = "blocked";
    }
    state(code, nowMs) {
      if (["ident", "unavailable", "idle"].includes(this.status)) return;
      if (code === 0) this.fail("ended");
      else if (code === 1) this.status = "playing";
      else if (code === 2) this.status = "paused";
      else if (code === 3) {
        if (this.status !== "loading") this.pendingSince = nowMs;
        this.status = "loading";
      }
    }
    fail(reason) {
      this.reason = String(reason);
      this.status = "unavailable";
      this.player.stop();
    }
    sync(clock2, nowMs) {
      var _a;
      const key = `${(_a = clock2.startMs) != null ? _a : ""}:${clock2.slot.id}`;
      if (key !== this.key) {
        this.key = key;
        this.pendingSince = nowMs;
        this.status = clock2.slot.type === "video" ? "loading" : "ident";
        if (clock2.slot.type === "video") this.player.load(clock2.slot.videoId, clock2.elapsed);
        else this.player.stop();
      }
      if (this.status === "loading" && nowMs - this.pendingSince >= 21e3) this.fail("timeout");
      return this.status;
    }
  };

  // src/presentation.js
  var PresentationController = class {
    constructor(root, { onOpen = () => {
    }, onClose = () => {
    }, onModeChange = () => {
    }, idleMs = 4500, storage } = {}) {
      this.root = root;
      this.onOpen = onOpen;
      this.onClose = onClose;
      this.onModeChange = onModeChange;
      this.idleMs = idleMs;
      this.onAir = false;
      this.opened = false;
      this.collapsing = false;
      this.timer = null;
      try {
        this.storage = storage != null ? storage : window.sessionStorage;
        this.mode = this.storage.getItem("disk-television-presentation") || "B";
      } catch {
        this.storage = null;
        this.mode = "B";
      }
      if (!["A", "B", "C"].includes(this.mode)) this.mode = "B";
      this.dialog = document.getElementById("presentation-dialog");
      this.buttons = [...root.querySelectorAll("[data-presentation]")];
      this.buttons.forEach((button) => button.addEventListener("click", () => this.setMode(button.dataset.presentation)));
      document.getElementById("presentation-open").addEventListener("click", () => this.showPicker());
      document.getElementById("presentation-close").addEventListener("click", () => this.closePicker());
      document.getElementById("reveal-controls").addEventListener("click", () => this.activity());
      root.addEventListener("pointermove", () => this.activity());
      root.addEventListener("focusin", () => {
        if (!this.collapsing) this.activity();
      });
      document.addEventListener("keydown", (event) => {
        this.activity();
        if (!this.opened) return;
        const key = event.key && event.key !== "Unidentified" ? event.key : { 37: "ArrowLeft", 38: "ArrowUp", 39: "ArrowRight", 40: "ArrowDown", 27: "Escape", 10009: "BrowserBack" }[event.keyCode] || "";
        if (["Escape", "BrowserBack", "GoBack"].includes(key)) {
          event.preventDefault();
          event.stopImmediatePropagation();
          this.closePicker();
          return;
        }
        const controls = [...this.dialog.querySelectorAll("button")];
        if (["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Tab"].includes(key)) {
          event.preventDefault();
          event.stopImmediatePropagation();
          const backwards = ["ArrowLeft", "ArrowUp"].includes(key) || key === "Tab" && event.shiftKey;
          const index = controls.indexOf(document.activeElement);
          controls[(index + (backwards ? -1 : 1) + controls.length) % controls.length].focus({ preventScroll: true });
        }
      }, true);
      this.setMode(this.mode, false);
    }
    setMode(mode, persist = true) {
      var _a;
      if (!["A", "B", "C"].includes(mode)) return;
      this.mode = mode;
      this.root.dataset.presentation = mode;
      this.buttons.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.presentation === mode)));
      document.getElementById("presentation-current").textContent = `PLAYER ${mode} / ${mode === "A" ? "CLEAN" : mode === "B" ? "BROADCAST FRAME" : "EXPERIMENTAL"}`;
      if (persist) {
        try {
          (_a = this.storage) == null ? void 0 : _a.setItem("disk-television-presentation", mode);
        } catch {
        }
      }
      this.activity();
      this.onModeChange(mode);
    }
    setOnAir(value) {
      this.onAir = value;
      this.root.classList.toggle("is-tuned", value);
      this.activity();
    }
    setChrome(hidden) {
      this.root.classList.toggle("chrome-hidden", hidden);
      this.root.dataset.chrome = hidden ? "hidden" : "visible";
      for (const element of [this.root.querySelector(".station-bar"), this.root.querySelector(".programme-bar")]) element.inert = hidden;
      if (hidden) {
        this.collapsing = true;
        document.getElementById("reveal-controls").focus({ preventScroll: true });
        this.collapsing = false;
      }
    }
    activity() {
      clearTimeout(this.timer);
      this.setChrome(false);
      if (this.mode === "A" && this.onAir && !this.opened) {
        this.timer = setTimeout(() => {
          if (!document.getElementById("guide").hidden || this.opened) return;
          this.setChrome(true);
        }, this.idleMs);
      }
    }
    showPicker() {
      this.opened = true;
      this.activity();
      this.onOpen();
      this.dialog.hidden = false;
      this.dialog.querySelector(`[data-presentation="${this.mode}"]`).focus({ preventScroll: true });
      document.getElementById("presentation-open").setAttribute("aria-expanded", "true");
    }
    closePicker() {
      this.opened = false;
      this.dialog.hidden = true;
      this.onClose();
      this.activity();
      document.getElementById("presentation-open").setAttribute("aria-expanded", "false");
      document.getElementById("presentation-open").focus({ preventScroll: true });
    }
  };

  // src/station-audio.js
  var StationAudio = class {
    constructor({ contextFactory, fetcher, baseUrl } = {}) {
      var _a, _b, _c;
      this.contextFactory = contextFactory != null ? contextFactory : (() => {
        var _a2;
        const Context = (_a2 = globalThis.AudioContext) != null ? _a2 : globalThis.webkitAudioContext;
        return Context ? new Context() : null;
      });
      this.fetcher = fetcher != null ? fetcher : (_a = globalThis.fetch) == null ? void 0 : _a.bind(globalThis);
      this.baseUrl = baseUrl != null ? baseUrl : new URL("./assets/audio/", (_c = (_b = globalThis.document) == null ? void 0 : _b.baseURI) != null ? _c : "http://localhost/");
      this.context = null;
      this.buffers = /* @__PURE__ */ new Map();
      this.errorCount = 0;
      this.starts = 0;
      this.activeKey = null;
    }
    prepare() {
      var _a;
      return (_a = this.preparation) != null ? _a : this.preparation = this.load();
    }
    async load() {
      var _a;
      try {
        (_a = this.context) != null ? _a : this.context = this.contextFactory();
        if (!this.context || !this.fetcher) return;
        await Promise.all(["station", "next", "night"].map(async (variant) => {
          for (const extension of ["mp3", "wav"]) {
            try {
              const response = await this.fetcher(new URL(`ident-${variant}.${extension}`, this.baseUrl));
              if (!response.ok) throw new Error("Audio fetch failed");
              const buffer = await this.context.decodeAudioData(await response.arrayBuffer());
              if (!buffer || !(buffer.duration > 0)) throw new Error("Invalid audio buffer");
              this.buffers.set(variant, buffer);
              return;
            } catch {
              this.errorCount++;
            }
          }
        }));
      } catch {
        this.errorCount++;
      }
    }
    async unlock() {
      var _a, _b;
      try {
        (_a = this.context) != null ? _a : this.context = this.contextFactory();
        await ((_b = this.context) == null ? void 0 : _b.resume());
      } catch {
        this.errorCount++;
      }
    }
    update(clock2, { enabled = true } = {}) {
      var _a;
      const { slot, elapsed, startMs } = clock2;
      if (!enabled || slot.type !== "ident") {
        this.stop();
        return;
      }
      const key = JSON.stringify([startMs, slot.id]);
      if (this.playedKey === key) return;
      if (this.source) this.stop();
      if (((_a = this.context) == null ? void 0 : _a.state) !== "running") return;
      const variant = slot.variant === "continuity" ? "night" : slot.variant;
      const buffer = this.buffers.get(variant);
      if (!buffer) return;
      const end = Math.min(buffer.duration, slot.duration, variant === "next" ? 4 : 18);
      if (!Number.isFinite(elapsed) || elapsed < 0 || !(end > elapsed)) return;
      let source;
      try {
        source = this.context.createBufferSource();
        source.buffer = buffer;
        source.connect(this.context.destination);
        source.onended = () => {
          try {
            source.disconnect();
          } catch {
            this.errorCount++;
          }
          if (this.source === source) {
            this.source = null;
            this.activeKey = null;
          }
        };
        source.start(0, elapsed, end - elapsed);
        this.source = source;
        this.playedKey = key;
        this.activeKey = key;
        this.starts++;
      } catch {
        this.errorCount++;
        if (source) {
          source.onended = null;
          try {
            source.stop();
          } catch {
          }
          try {
            source.disconnect();
          } catch {
          }
        }
      }
    }
    stop() {
      const source = this.source;
      this.source = null;
      this.activeKey = null;
      this.playedKey = null;
      if (!source) return;
      try {
        source.stop();
      } catch {
        this.errorCount++;
      }
      try {
        source.disconnect();
      } catch {
        this.errorCount++;
      }
    }
    getState() {
      var _a, _b;
      return {
        readyVariants: [...this.buffers.keys()],
        activeKey: this.activeKey,
        contextState: (_b = (_a = this.context) == null ? void 0 : _a.state) != null ? _b : "unavailable",
        starts: this.starts,
        errorCount: this.errorCount
      };
    }
  };

  // src/app.js
  var $ = (id) => document.getElementById(id);
  var timeFormat = new Intl.DateTimeFormat("pt-BR", { timeZone: "America/Sao_Paulo", hour: "2-digit", minute: "2-digit", hourCycle: "h23" });
  var clockFormat = new Intl.DateTimeFormat("pt-BR", { timeZone: "America/Sao_Paulo", hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23" });
  var config;
  var catalog;
  var slots;
  var epoch;
  var tuned = false;
  var player = null;
  var playerReady = false;
  var apiPromise = null;
  var playout;
  var lastSlotKey = "";
  var guideOpen = false;
  var muted = false;
  var lastGuideIndex = -1;
  var stationAudio = new StationAudio({ baseUrl: new URL("./assets/audio/", document.baseURI) });
  var connection = null;
  var suspendedForView = false;
  var clock;
  var presentationOpen = false;
  var seconds = (value) => `${Math.floor(value / 60)}:${String(Math.floor(value % 60)).padStart(2, "0")}`;
  var setText = (id, text) => {
    if ($(id).textContent !== String(text)) $(id).textContent = text;
  };
  function pictureVisible() {
    const frame = $("youtube-player");
    const frameRect = frame == null ? void 0 : frame.getBoundingClientRect();
    const rect = (frameRect == null ? void 0 : frameRect.width) && (frameRect == null ? void 0 : frameRect.height) ? frameRect : $("stage").getBoundingClientRect();
    const width = Math.max(0, Math.min(innerWidth, rect.right) - Math.max(0, rect.left));
    const height = Math.max(0, Math.min(innerHeight, rect.bottom) - Math.max(0, rect.top));
    return !document.hidden && !guideOpen && !presentationOpen && rect.width >= 200 && rect.height >= 200 && width * height / (rect.width * rect.height) > 0.5;
  }
  function loadYouTube() {
    var _a;
    if ((_a = window.YT) == null ? void 0 : _a.Player) return Promise.resolve();
    if (apiPromise) return apiPromise;
    apiPromise = new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        apiPromise = null;
        script.remove();
        reject(new Error("A API do YouTube não respondeu."));
      }, 12e3);
      window.onYouTubeIframeAPIReady = () => {
        clearTimeout(timer);
        resolve();
      };
      const script = document.createElement("script");
      script.src = "https://www.youtube.com/iframe_api";
      script.onerror = () => {
        clearTimeout(timer);
        apiPromise = null;
        script.remove();
        reject(new Error("Não foi possível acessar o YouTube."));
      };
      document.head.append(script);
    });
    return apiPromise;
  }
  var adapter = {
    load(videoId, offset) {
      if (!playerReady || !pictureVisible()) return;
      $("player-shell").hidden = false;
      player.loadVideoById({ videoId, startSeconds: Math.max(0, offset) });
    },
    stop() {
      if (playerReady) player.stopVideo();
    }
  };
  async function connectPlayer() {
    await loadYouTube();
    if (playerReady) return;
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        player == null ? void 0 : player.destroy();
        player = null;
        playerReady = false;
        $("player-shell").innerHTML = '<div id="youtube-player"></div>';
        reject(new Error("O player não respondeu."));
      }, 15e3);
      player = new window.YT.Player("youtube-player", {
        width: "100%",
        height: "100%",
        playerVars: { autoplay: 0, controls: 1, playsinline: 1, rel: 0, fs: 1, origin: location.origin, hl: "pt", mute: muted ? 1 : 0 },
        events: {
          onReady() {
            clearTimeout(timeout);
            playerReady = true;
            muted ? player.mute() : player.unMute();
            resolve();
          },
          onStateChange(event) {
            if (!playout || guideOpen || presentationOpen || suspendedForView || document.hidden) return;
            playout.state(event.data, Date.now());
            renderSignal();
          },
          onError(event) {
            if (playout && (clock == null ? void 0 : clock.slot.type) === "video" && !guideOpen) {
              playout.fail(`YouTube ${event.data}`);
              renderSignal();
            }
          },
          onAutoplayBlocked() {
            if (playout) {
              playout.blocked();
              renderSignal();
            }
          }
        }
      });
    });
  }
  function ensureConnected() {
    if (playerReady) return Promise.resolve();
    if (connection) return connection;
    connection = connectPlayer().then(() => {
      if (tuned && !guideOpen && !presentationOpen && !document.hidden) {
        playout.retry();
        tick();
      }
    }).catch((error) => {
      if (playout) {
        playout.fail(error.message);
        renderSignal();
      }
    }).finally(() => {
      connection = null;
    });
    return connection;
  }
  function unlockAudio() {
    stationAudio.unlock();
    stationAudio.prepare();
  }
  function nextVideo(index) {
    for (let i = 1; i <= slots.length; i++) {
      const next = slots[(index + i) % slots.length];
      if (next.type === "video") return next;
    }
    return null;
  }
  function tick() {
    const now = Date.now();
    setText("clock", clockFormat.format(now));
    if (!slots) return;
    clock = locate(slots, epoch, now);
    const { slot, elapsed, startMs, endMs, index } = clock;
    $("app").style.setProperty("--block-color", slot.block.includes("CYBERIA") ? "#a1d9e5" : slot.block.includes("MOE") ? "#d8a6c6" : slot.block.includes("AFTER") ? "#afa2d6" : "#b6c3de");
    const key = `${startMs}:${slot.id}`;
    $("stage").dataset.slotId = slot.id;
    $("stage").dataset.slotType = slot.type;
    $("stage").dataset.elapsed = String(elapsed);
    $("stage").dataset.startMs = String(startMs);
    $("stage").dataset.endMs = String(endMs);
    setText("now-title", slot.title);
    const item = catalog.find((item2) => item2.id === slot.contentId);
    setText("now-meta", item ? `${slot.block} · ${item.creator} · ${item.year}` : `${slot.block} · Continuidade original`);
    const next = nextVideo(index);
    setText("next-title", (next == null ? void 0 : next.title) || "DISK TELEVISION");
    let nextStart = clock.cycleStartMs + ((next == null ? void 0 : next.start) || 0) * 1e3;
    if (nextStart <= startMs) nextStart += config.cycleSeconds * 1e3;
    setText("next-time", `Às ${timeFormat.format(nextStart)} · ${(next == null ? void 0 : next.block) || "CH 99"}`);
    setText("slot-start", timeFormat.format(startMs));
    setText("slot-end", timeFormat.format(endMs));
    $("progress").style.width = `${100 * elapsed / slot.duration}%`;
    if (tuned && !guideOpen && !presentationOpen && !document.hidden) {
      if (!pictureVisible()) {
        if (!suspendedForView) {
          suspendedForView = true;
          adapter.stop();
          playout == null ? void 0 : playout.retry();
        }
        stationAudio.stop();
        setText("station-state", "SINAL EM ESPERA");
        return;
      }
      if (suspendedForView) {
        suspendedForView = false;
        playout == null ? void 0 : playout.retry();
        lastSlotKey = "";
      }
      if (playout && (playerReady || slot.type === "ident")) playout.sync(clock, now);
      if (key !== lastSlotKey) {
        lastSlotKey = key;
        if (slot.type === "video" && !playerReady) ensureConnected();
        if (slot.type === "ident") {
          $("continuity").dataset.role = slot.role || "";
          $("continuity").dataset.variant = slot.variant === "continuity" ? "night" : slot.variant;
          setText("ident-label", slot.role === "block-opening" ? "ABERTURA DE BLOCO / CH 99" : slot.variant === "next" ? "NA SEQUÊNCIA" : slot.variant === "night" ? "FREQUÊNCIA NOTURNA" : slot.variant === "continuity" ? "INTERVALO ORBITAL" : "IDENTIFICAÇÃO / CH 99");
          setText("ident-title", slot.role === "block-opening" ? slot.block : slot.variant === "next" ? slot.nextTitle : slot.variant === "night" ? "Para quem ainda está acordado." : slot.variant === "continuity" ? "O sinal permanece." : "Uma frequência fora do tempo.");
          setText("ident-subtitle", slot.variant === "next" ? "FIQUE NA FREQUÊNCIA" : slot.variant === "night" ? "A NOITE NÃO TERMINA AQUI." : "DISK TELEVISION · TRANSMISSÃO CONTÍNUA");
        }
      }
      renderSignal();
    }
    stationAudio.update(clock, { enabled: tuned && !muted && !guideOpen && !presentationOpen && !document.hidden && pictureVisible() });
    const soundState = stationAudio.getState();
    $("app").dataset.audioState = soundState.contextState;
    $("app").dataset.audioStarts = String(soundState.starts);
    $("app").dataset.audioActive = String(Boolean(soundState.activeKey));
    $("app").dataset.audioVariants = soundState.readyVariants.join(",");
    if (guideOpen && lastGuideIndex !== index) renderGuide();
  }
  function renderSignal() {
    if (!clock || !tuned || guideOpen || presentationOpen || suspendedForView) return;
    const status = (playout == null ? void 0 : playout.status) || "connecting";
    const ident = clock.slot.type === "ident";
    const fallback = !ident && ["unavailable", "connecting", "idle"].includes(status);
    $("player-shell").hidden = ident || fallback || !playerReady;
    $("continuity").hidden = !ident && !fallback;
    $("reception").hidden = ident || status === "playing";
    setText("station-state", ident ? "CONTINUIDADE" : status === "playing" ? "NO AR" : status === "loading" ? "RECEBENDO SINAL" : "SINTONIZADO");
    if (fallback) {
      $("continuity").dataset.variant = "unavailable";
      setText("ident-label", status === "unavailable" ? "CONTINUIDADE / CH 99" : "CONECTANDO / CH 99");
      setText("ident-title", status === "unavailable" ? "O sinal continua." : "Estabelecendo contato.");
      setText("ident-subtitle", status === "unavailable" ? "ESTA ATRAÇÃO NÃO RESPONDEU. A PRÓXIMA ENTRA NO HORÁRIO." : "O RELÓGIO DA EMISSORA NÃO PARA.");
    }
    setText("ident-block", clock.slot.block);
    setText("ident-countdown", `PRÓXIMA TRANSMISSÃO EM ${seconds(clock.remaining)}`);
    $("continuity").style.setProperty("--ident-progress", clock.elapsed / clock.slot.duration);
    const descriptions = { loading: "Recebendo o sinal do YouTube…", blocked: "O navegador bloqueou a reprodução automática. Use Ressintonizar ou o botão do player.", paused: "O vídeo está pausado. Ressintonize para voltar ao horário da emissora.", unavailable: `Atração indisponível (${(playout == null ? void 0 : playout.reason) || "conexão"}). A grade segue automaticamente.`, connecting: "Conectando ao YouTube…", idle: "Conectando ao YouTube…" };
    setText("reception-text", descriptions[status] || "");
    $("retry").disabled = status === "connecting";
  }
  async function tune() {
    unlockAudio();
    if (playerReady && pictureVisible()) {
      muted ? player.mute() : player.unMute();
    }
    tuned = true;
    $("gate").hidden = true;
    presentation.setOnAir(true);
    window.scrollTo(0, $("stage").offsetTop);
    playout != null ? playout : playout = new Playout(adapter);
    playout.retry();
    lastSlotKey = "";
    tick();
    $("guide-open").focus({ preventScroll: true });
    await ensureConnected();
  }
  function renderGuide() {
    var _a;
    if (!clock) return;
    const list = $("guide-list");
    list.replaceChildren();
    const fragment = document.createDocumentFragment();
    for (const [i, slot] of slots.entries()) {
      const row = document.createElement("article");
      row.className = `guide-row${i === clock.index ? " current" : i < clock.index ? " past" : ""}`;
      if (i === clock.index) row.setAttribute("aria-current", "true");
      const at = document.createElement("time");
      at.dateTime = new Date(clock.cycleStartMs + slot.start * 1e3).toISOString();
      at.textContent = timeFormat.format(clock.cycleStartMs + slot.start * 1e3);
      const info = document.createElement("div"), title = document.createElement("h3"), detail = document.createElement("p");
      title.textContent = slot.variant === "next" ? `A seguir: ${slot.nextTitle}` : slot.title;
      detail.textContent = slot.type === "video" ? `${((_a = catalog.find((item) => item.id === slot.contentId)) == null ? void 0 : _a.creator) || ""} · ${seconds(slot.duration)}` : `Vinheta original · ${seconds(slot.duration)}`;
      info.append(title, detail);
      const block = document.createElement("span");
      block.className = "guide-block";
      block.textContent = slot.block;
      const kind = document.createElement("span");
      kind.className = "guide-kind";
      kind.textContent = i === clock.index ? "NO AR" : slot.type === "video" ? "ATRAÇÃO" : "VINHETA";
      row.append(at, info, block, kind);
      fragment.append(row);
    }
    list.append(fragment);
    lastGuideIndex = clock.index;
    const current = list.querySelector(".current");
    if (current) list.scrollTop = current.offsetTop - list.offsetTop - 30;
  }
  function showGuide() {
    if (!slots) return;
    guideOpen = true;
    adapter.stop();
    stationAudio.stop();
    $("player-shell").hidden = true;
    $("main").inert = true;
    $("main").style.visibility = "hidden";
    $("guide").hidden = false;
    $("guide-open").setAttribute("aria-expanded", "true");
    renderGuide();
    $("guide-close").focus();
  }
  function closeGuide() {
    guideOpen = false;
    $("guide").hidden = true;
    $("main").inert = false;
    $("main").style.visibility = "";
    $("guide-open").setAttribute("aria-expanded", "false");
    if (tuned) {
      playout == null ? void 0 : playout.retry();
      lastSlotKey = "";
      tick();
    }
    $("guide-open").focus({ preventScroll: true });
  }
  $("tune").addEventListener("click", tune);
  $("retry").addEventListener("click", tune);
  $("guide-open").addEventListener("click", showGuide);
  $("guide-close").addEventListener("click", closeGuide);
  $("sound").addEventListener("click", () => {
    muted = !muted;
    unlockAudio();
    if (muted) stationAudio.stop();
    tick();
    if (playerReady) muted ? player.mute() : player.unMute();
    $("sound").setAttribute("aria-pressed", String(muted));
    $("sound").setAttribute("aria-label", muted ? "Ativar áudio" : "Silenciar áudio");
    setText("sound", muted ? "Som desligado" : "Som ligado");
  });
  $("fullscreen").addEventListener("click", async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await $("app").requestFullscreen();
    } catch {
      setText("reception-text", "Tela cheia indisponível neste navegador. Use o modo de tela cheia da TV.");
      $("reception").hidden = false;
    }
  });
  document.addEventListener("fullscreenchange", () => setText("fullscreen", document.fullscreenElement ? "Sair da tela cheia" : "Tela cheia"));
  document.addEventListener("keydown", (event) => {
    var _a;
    if (presentationOpen) return;
    if (((_a = event.target) == null ? void 0 : _a.tagName) === "IFRAME") return;
    const key = event.key && event.key !== "Unidentified" ? event.key : { 37: "ArrowLeft", 38: "ArrowUp", 39: "ArrowRight", 40: "ArrowDown", 27: "Escape", 10009: "BrowserBack" }[event.keyCode] || "";
    if (key.toLowerCase() === "g") {
      event.preventDefault();
      guideOpen ? closeGuide() : showGuide();
    }
    if (["Escape", "BrowserBack", "GoBack"].includes(key)) {
      if (guideOpen) {
        event.preventDefault();
        closeGuide();
      }
    }
    if (guideOpen) {
      if (["ArrowDown", "ArrowUp", "PageDown", "PageUp"].includes(key)) {
        event.preventDefault();
        $("guide-list").scrollTop += key === "ArrowDown" ? 100 : key === "ArrowUp" ? -100 : key === "PageDown" ? 450 : -450;
      }
      if (key === "Tab") {
        event.preventDefault();
        document.activeElement === $("guide-close") ? $("guide-list").focus() : $("guide-close").focus();
      }
    } else if (key.startsWith("Arrow")) {
      const buttons = [...document.querySelectorAll("button,a[href]")].filter((b) => !b.disabled && b.getClientRects().length && !b.closest("[inert]") && getComputedStyle(b).visibility !== "hidden");
      const index = buttons.indexOf(document.activeElement);
      if (buttons.length) {
        event.preventDefault();
        buttons[(index + (key === "ArrowLeft" || key === "ArrowUp" ? -1 : 1) + buttons.length) % buttons.length].focus();
      }
    }
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      adapter.stop();
      stationAudio.stop();
    } else if (tuned && !guideOpen && !presentationOpen) {
      playout == null ? void 0 : playout.retry();
      tick();
    }
  });
  window.addEventListener("pageshow", () => {
    if (tuned) {
      playout == null ? void 0 : playout.retry();
      tick();
    }
  });
  async function boot() {
    try {
      const responses = await Promise.all(["./data/catalog.json", "./data/schedule.json"].map((url) => fetch(url, { cache: "no-cache" })));
      if (responses.some((response) => !response.ok)) throw new Error("Não foi possível ler o catálogo e a grade.");
      const [raw, settings] = await Promise.all(responses.map((response) => response.json()));
      catalog = Array.isArray(raw) ? raw : raw.items;
      config = settings;
      slots = compileSchedule(config, catalog);
      epoch = Date.parse(config.epoch);
      $("tune").disabled = false;
      setText("boot-message", "Uma interação inicia a transmissão. Conteúdos via YouTube.");
      tick();
      $("tune").focus();
    } catch (error) {
      setText("boot-message", `Falha de sintonia: ${error.message} Abra por HTTP(S), não como arquivo local.`);
    }
  }
  var presentation = new PresentationController($("app"), {
    onOpen() {
      presentationOpen = true;
      if (guideOpen) closeGuide();
      adapter.stop();
      stationAudio.stop();
      $("player-shell").hidden = true;
      $("main").inert = true;
      $("main").style.visibility = "hidden";
    },
    onClose() {
      presentationOpen = false;
      $("main").inert = false;
      $("main").style.visibility = "";
      if (tuned) {
        playout == null ? void 0 : playout.retry();
        lastSlotKey = "";
        tick();
      }
    },
    onModeChange() {
      if (tuned && !presentationOpen) tick();
    }
  });
  setInterval(tick, 250);
  tick();
  boot();
})();
