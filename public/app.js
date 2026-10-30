/**
 * NecroGit - Forensic Git Séance & Digital Ofrenda
 * Module: public/app.js
 * 
 * 100% Vanilla ES6 JavaScript (Zero external dependencies).
 * Features:
 * 1. Web Audio Procedural Synthesizer (CRT hum, mechanical keystrokes, singing bowl chime)
 * 2. HTML5 Canvas floating cempasúchil (marigold) petal particle engine
 * 3. Server-Sent Events (SSE) streaming séance terminal
 * 4. Resurrected code & fatal git diff inspection modal
 */

// ==========================================================================
// 1. Procedural Web Audio Engine
// ==========================================================================
class NecroAudioEngine {
  constructor() {
    this.ctx = null;
    this.isEnabled = false;
    this.humGain = null;
    this.windGain = null;
    this.windFilter = null;
  }

  init() {
    if (this.ctx) return;
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AudioCtx();

    // 1. CRT Mains Transformer Hum (60Hz sawtooth + 140Hz lowpass)
    const humOsc = this.ctx.createOscillator();
    const humGain = this.ctx.createGain();
    const humFilter = this.ctx.createBiquadFilter();

    humOsc.type = "sawtooth";
    humOsc.frequency.setValueAtTime(60, this.ctx.currentTime);

    humFilter.type = "lowpass";
    humFilter.frequency.setValueAtTime(140, this.ctx.currentTime);

    humGain.gain.setValueAtTime(0.0, this.ctx.currentTime);

    humOsc.connect(humFilter);
    humFilter.connect(humGain);
    humGain.connect(this.ctx.destination);
    humOsc.start();
    this.humGain = humGain;

    // 2. Procedural Pink Noise Wind Drafts
    const bufferSize = this.ctx.sampleRate * 2;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.96900 * b2 + white * 0.1538520;
      b3 = 0.86650 * b3 + white * 0.3104856;
      b4 = 0.55000 * b4 + white * 0.5329522;
      b5 = -0.7616 * b5 - white * 0.0168980;
      output[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.11;
      b6 = white * 0.115926;
    }

    const windSource = this.ctx.createBufferSource();
    windSource.buffer = noiseBuffer;
    windSource.loop = true;

    const windFilter = this.ctx.createBiquadFilter();
    windFilter.type = "bandpass";
    windFilter.frequency.setValueAtTime(280, this.ctx.currentTime);
    windFilter.Q.setValueAtTime(1.5, this.ctx.currentTime);

    const windGain = this.ctx.createGain();
    windGain.gain.setValueAtTime(0.0, this.ctx.currentTime);

    windSource.connect(windFilter);
    windFilter.connect(windGain);
    windGain.connect(this.ctx.destination);
    windSource.start();

    this.windGain = windGain;
    this.windFilter = windFilter;
  }

  toggle() {
    if (!this.ctx) this.init();
    if (this.ctx.state === "suspended") this.ctx.resume();

    this.isEnabled = !this.isEnabled;
    if (this.humGain) {
      const targetGain = this.isEnabled ? 0.022 : 0.0;
      this.humGain.gain.setTargetAtTime(targetGain, this.ctx.currentTime, 0.2);
    }
    if (this.windGain) {
      const targetWind = this.isEnabled ? 0.018 : 0.0;
      this.windGain.gain.setTargetAtTime(targetWind, this.ctx.currentTime, 0.4);
    }
    return this.isEnabled;
  }

  playGust() {
    if (!this.isEnabled || !this.ctx || !this.windFilter) return;
    try {
      const now = this.ctx.currentTime;
      this.windFilter.frequency.cancelScheduledValues(now);
      this.windFilter.frequency.setValueAtTime(280, now);
      this.windFilter.frequency.exponentialRampToValueAtTime(720, now + 0.8);
      this.windFilter.frequency.exponentialRampToValueAtTime(260, now + 2.5);
    } catch (e) {}
  }

  playKeyClick() {
    if (!this.isEnabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = "sine";
      osc.frequency.setValueAtTime(800 + Math.random() * 400, now);
      osc.frequency.exponentialRampToValueAtTime(120, now + 0.012);

      gain.gain.setValueAtTime(0.015, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.012);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 0.012);
    } catch (e) {}
  }

  playChime(freq = 432) {
    if (!this.isEnabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = "sine";
      osc.frequency.setValueAtTime(freq, now);

      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.8);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 1.8);
    } catch (e) {}
  }
}

// ==========================================================================
// 2. Floating Marigold (Cempasúchil) Petal Physics Engine
// ==========================================================================
class PetalCanvas {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext("2d");
    this.petals = [];
    this.maxPetals = 45;
    this.colors = ["#ff7500", "#ff9800", "#ffb300", "#f57c00", "#e65100"];

    this.resize();
    window.addEventListener("resize", () => this.resize());
    this.initPetals();
    this.animate();
  }

  resize() {
    this.width = this.canvas.width = window.innerWidth;
    this.height = this.canvas.height = window.innerHeight;
  }

  initPetals() {
    for (let i = 0; i < this.maxPetals; i++) {
      this.petals.push(this.createPetal(Math.random() * this.width, Math.random() * this.height));
    }
  }

  createPetal(x, y) {
    return {
      x: x !== undefined ? x : Math.random() * this.width,
      y: y !== undefined ? y : -20,
      size: 6 + Math.random() * 9,
      vx: (Math.random() - 0.5) * 1.2,
      vy: 0.8 + Math.random() * 1.4,
      rotation: Math.random() * Math.PI * 2,
      vRotation: (Math.random() - 0.5) * 0.04,
      oscillation: Math.random() * Math.PI,
      oscillationSpeed: 0.02 + Math.random() * 0.03,
      color: this.colors[Math.floor(Math.random() * this.colors.length)],
      opacity: 0.4 + Math.random() * 0.45
    };
  }

  burst(originX, originY, count = 25) {
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 2 + Math.random() * 5;
      const p = this.createPetal(originX, originY);
      p.vx = Math.cos(angle) * speed;
      p.vy = Math.sin(angle) * speed - 2;
      this.petals.push(p);
    }
  }

  animate() {
    this.ctx.clearRect(0, 0, this.width, this.height);

    for (let i = 0; i < this.petals.length; i++) {
      const p = this.petals[i];
      p.oscillation += p.oscillationSpeed;
      p.x += p.vx + Math.sin(p.oscillation) * 0.6;
      p.y += p.vy;
      p.rotation += p.vRotation;

      this.ctx.save();
      this.ctx.translate(p.x, p.y);
      this.ctx.rotate(p.rotation);
      this.ctx.fillStyle = p.color;
      this.ctx.globalAlpha = p.opacity;

      // Draw organic petal shape
      this.ctx.beginPath();
      this.ctx.ellipse(0, 0, p.size, p.size * 0.55, 0, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.restore();

      // Recycle petals falling out of view
      if (p.y > this.height + 25 || p.x < -30 || p.x > this.width + 30) {
        if (this.petals.length > this.maxPetals) {
          this.petals.splice(i, 1);
          i--;
        } else {
          this.petals[i] = this.createPetal(Math.random() * this.width, -15);
        }
      }
    }

    requestAnimationFrame(() => this.animate());
  }
}

// ==========================================================================
// 3. Application State & Controller
// ==========================================================================
class NecroGitApp {
  constructor() {
    this.audio = new NecroAudioEngine();
    this.petals = new PetalCanvas("petalCanvas");

    this.graveyard = null;
    this.filteredItems = [];
    this.activeFilter = "all";
    this.selectedEntity = null;
    this.isStreaming = false;

    // Load persistent offerings from localStorage
    try {
      this.offerings = JSON.parse(localStorage.getItem("necrogit_offerings") || "{}");
    } catch (e) {
      this.offerings = {};
    }

    this.bindDom();
    this.bindEvents();
    this.init();
  }

  bindDom() {
    this.dom = {
      repoName: document.getElementById("repoName"),
      entityCount: document.getElementById("entityCount"),
      graveyardList: document.getElementById("graveyardList"),
      filterBtns: document.querySelectorAll(".filter-btn"),
      viewToggleBtn: document.getElementById("viewToggleBtn"),
      viewModeText: document.getElementById("viewModeText"),
      audioToggleBtn: document.getElementById("audioToggleBtn"),
      audioModeText: document.getElementById("audioModeText"),
      refreshBtn: document.getElementById("refreshGraveyardBtn"),
      altarTitle: document.getElementById("altarEntityTitle"),
      altarSubtitle: document.getElementById("altarEntitySubtitle"),
      terminalStatus: document.getElementById("terminalStatus"),
      terminalMeta: document.getElementById("terminalMeta"),
      terminalBody: document.getElementById("terminalBody"),
      invokeSeanceBtn: document.getElementById("invokeSeanceBtn"),
      offerMarigoldBtn: document.getElementById("offerMarigoldBtn"),
      offerMezcalBtn: document.getElementById("offerMezcalBtn"),
      marigoldCount: document.getElementById("marigoldCount"),
      mezcalCount: document.getElementById("mezcalCount"),
      viewDiffBtn: document.getElementById("viewDiffBtn"),
      engineStatus: document.getElementById("engineStatus"),
      totalLinesBuried: document.getElementById("totalLinesBuried"),
      codeModal: document.getElementById("codeModal"),
      modalCloseBtn: document.getElementById("modalCloseBtn"),
      modalEntityName: document.getElementById("modalEntityName"),
      modalCodeContent: document.getElementById("modalCodeContent"),
      modalCommitMeta: document.getElementById("modalCommitMeta"),
      tabCodeBtn: document.getElementById("tabCodeBtn"),
      tabDiffBtn: document.getElementById("tabDiffBtn"),
      modalCopyBtn: document.getElementById("modalCopyBtn")
    };
  }

  bindEvents() {
    // Mode toggle
    this.dom.viewToggleBtn.addEventListener("click", () => {
      document.body.classList.toggle("mode-crt");
      const isCrt = document.body.classList.contains("mode-crt");
      this.dom.viewModeText.textContent = isCrt ? "Ofrenda Mode" : "CRT Mode";
      this.audio.playKeyClick();
    });

    // Audio toggle
    this.dom.audioToggleBtn.addEventListener("click", () => {
      const enabled = this.audio.toggle();
      this.dom.audioToggleBtn.querySelector(".btn-icon").textContent = enabled ? "🔊" : "🔇";
      this.dom.audioModeText.textContent = enabled ? "Audio: Active" : "Audio: Muted";
      if (enabled) this.audio.playChime(528);
    });

    // Refresh
    this.dom.refreshBtn.addEventListener("click", () => {
      this.audio.playKeyClick();
      this.loadGraveyard();
    });

    // Filter tabs
    this.dom.filterBtns.forEach(btn => {
      btn.addEventListener("click", (e) => {
        this.dom.filterBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        this.activeFilter = btn.dataset.filter;
        this.applyFilter();
        this.audio.playKeyClick();
      });
    });

    // Séance trigger
    this.dom.invokeSeanceBtn.addEventListener("click", () => {
      if (this.selectedEntity && !this.isStreaming) {
        this.invokeSeance(this.selectedEntity);
      }
    });

    // Offerings
    this.dom.offerMarigoldBtn.addEventListener("click", (e) => this.addOffering("marigold", e));
    this.dom.offerMezcalBtn.addEventListener("click", (e) => this.addOffering("mezcal", e));

    // Resurrect Code Modal
    this.dom.viewDiffBtn.addEventListener("click", () => {
      if (this.selectedEntity) this.openCodeModal(this.selectedEntity, "code");
    });
    this.dom.modalCloseBtn.addEventListener("click", () => {
      this.dom.codeModal.style.display = "none";
      this.audio.playKeyClick();
    });
    this.dom.tabCodeBtn.addEventListener("click", () => {
      this.dom.tabCodeBtn.classList.add("active");
      this.dom.tabDiffBtn.classList.remove("active");
      this.renderModalContent("code");
    });
    this.dom.tabDiffBtn.addEventListener("click", () => {
      this.dom.tabDiffBtn.classList.add("active");
      this.dom.tabCodeBtn.classList.remove("active");
      this.renderModalContent("diff");
    });
    this.dom.modalCopyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(this.dom.modalCodeContent.textContent);
      this.dom.modalCopyBtn.textContent = "✅ Copied!";
      setTimeout(() => (this.dom.modalCopyBtn.textContent = "📋 Copy Code"), 1800);
    });
  }

  async init() {
    await this.loadStatus();
    await this.loadGraveyard();
  }

  async loadStatus() {
    try {
      const res = await fetch("/api/status");
      if (!res.ok) throw new Error("Static mode");
      const data = await res.json();
      this.dom.repoName.textContent = data.repo_name || "Repository";

      const inf = data.inference || {};
      if (inf.model_ready) {
        this.dom.engineStatus.textContent = `Google Gemma 2 (${inf.active_model})`;
        this.dom.terminalMeta.textContent = `MODEL: ${inf.active_model.toUpperCase()} (ONLINE)`;
      } else {
        this.dom.engineStatus.textContent = "Heuristic Necromancer (Local Fallback)";
        this.dom.terminalMeta.textContent = "MODEL: HEURISTIC (OFFLINE AIR-GAP)";
      }
    } catch (e) {
      // Static GitHub Pages Demo Mode
      this.dom.repoName.textContent = "necrogit (GitHub Pages Demo)";
      this.dom.engineStatus.textContent = "Deterministic Necromancer (Client Demo)";
      this.dom.terminalMeta.textContent = "MODEL: CLIENT-SIDE AIR-GAP (DEMO)";
    }
  }

  async loadGraveyard() {
    this.dom.graveyardList.innerHTML = `
      <div class="empty-state">
        <div class="spinner"></div>
        <p>Excavating git object cemetery...</p>
      </div>`;

    try {
      const res = await fetch("/api/graveyard");
      if (!res.ok) throw new Error("Static mode");
      this.graveyard = await res.json();
    } catch (e) {
      // Fallback to rich embedded demo graveyard for GitHub Pages
      this.graveyard = this.getStaticDemoGraveyard();
    }

    const funcs = this.graveyard.deleted_functions || [];
    const files = this.graveyard.deleted_files || [];
    const total = funcs.length + files.length;

    this.dom.entityCount.textContent = `${total} deceased artifacts`;
    this.dom.totalLinesBuried.textContent = `${(this.graveyard.total_lines_buried || 0).toLocaleString()} lines`;

    this.applyFilter();

    // Automatically select the first entity if available
    if (this.filteredItems.length > 0) {
      this.selectEntity(this.filteredItems[0]);
    }
  }

  getStaticDemoGraveyard() {
    return {
      repository: "necrogit (Demo Ofrenda)",
      is_git_repository: true,
      total_deceased_artifacts: 5,
      total_lines_buried: 832,
      deleted_files: [
        {
          entity_type: "file",
          name: "FUTURE_ROADMAP.md",
          file_path: "FUTURE_ROADMAP.md",
          death_commit: "e0d6c58a",
          death_author: "XiaoArnav",
          death_date: "2026-10-29",
          death_message: "chore: remove future roadmap from public repo",
          birth_commit: "781f756e",
          birth_author: "XiaoArnav",
          birth_date: "2026-10-26",
          lines_lost: 47,
          resurrected_code: "# Future Roadmap (Locked into chat memory)\n- Option B: Ofrenda // Sovereign\n- Option C: Ghostwire // 1999",
          resurrected_diff: "- # Future Roadmap\n- Option B: Ofrenda // Sovereign\n- Option C: Ghostwire // 1999"
        },
        {
          entity_type: "file",
          name: "billing_v1_deprecated.py",
          file_path: "services/billing/legacy.py",
          death_commit: "8a1b2c3d",
          death_author: "InfraLead",
          death_date: "2026-08-14",
          death_message: "refactor: decommission XML billing gateway in favor of event stream",
          birth_commit: "10293847",
          birth_author: "Founder",
          birth_date: "2024-01-10",
          lines_lost: 342,
          resurrected_code: "def process_legacy_soap_invoice(xml_payload):\n    # 342 lines of SOAP XML parsing\n    pass",
          resurrected_diff: "- def process_legacy_soap_invoice(xml_payload):\n-     # 342 lines of SOAP XML parsing\n-     pass"
        }
      ],
      deleted_functions: [
        {
          entity_type: "function",
          name: "fast_inverse_sqrt()",
          file_path: "src/game/q_math.c",
          death_commit: "c51b980a",
          death_author: "John Carmack",
          death_date: "1999-12-10",
          death_message: "refactor: replace magic constant 0x5f3759df with hardware SSE instruction",
          birth_commit: "0001a11",
          birth_author: "Gary Tarolli / Greg Walsh",
          birth_date: "1995-04-12",
          lines_lost: 16,
          resurrected_code: "float Q_rsqrt( float number ) {\n    long i;\n    float x2, y;\n    const float threehalfs = 1.5F;\n\n    x2 = number * 0.5F;\n    y  = number;\n    i  = * ( long * ) &y;                       // evil floating point bit level hacking\n    i  = 0x5f3759df - ( i >> 1 );               // what the fuck?\n    y  = * ( float * ) &i;\n    y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration\n    return y;\n}",
          resurrected_diff: "- float Q_rsqrt( float number ) {\n-     long i;\n-     float x2, y;\n-     const float threehalfs = 1.5F;\n-     i  = 0x5f3759df - ( i >> 1 );\n-     return y;\n- }"
        },
        {
          entity_type: "function",
          name: "rose_window_prism()",
          file_path: "app/static/js/stellar-map.js",
          death_commit: "ea99b114",
          death_author: "XiaoArnav",
          death_date: "2026-10-23",
          death_message: "refactor: delete over-engineered volumetric stained-glass god-ray lighting engine",
          birth_commit: "1f05c01",
          birth_author: "XiaoArnav",
          birth_date: "2026-10-21",
          lines_lost: 385,
          resurrected_code: "function renderRoseWindowPrism(ctx, time) {\n    for (let ray = 0; ray < 128; ray++) {\n        const angle = (ray / 128) * Math.PI * 2 + time * 0.001;\n        ctx.strokeStyle = `hsla(${ray * 2.8}, 80%, 65%, 0.12)`;\n        ctx.beginPath();\n        ctx.moveTo(centerX, centerY);\n        ctx.lineTo(centerX + Math.cos(angle) * radius, centerY + Math.sin(angle) * radius);\n        ctx.stroke();\n    }\n}",
          resurrected_diff: "- function renderRoseWindowPrism(ctx, time) {\n-     for (let ray = 0; ray < 128; ray++) {\n-         ctx.stroke();\n-     }\n- }"
        },
        {
          entity_type: "class",
          name: "LegacyBBSDialer",
          file_path: "telecom/modem_v32.py",
          death_commit: "4e99a12f",
          death_author: "Sysop",
          death_date: "2003-08-14",
          death_message: "chore: decommission 56k dial-up Hayes AT command modem carrier line",
          birth_commit: "1098ef0",
          birth_author: "Sysop",
          birth_date: "1996-03-02",
          lines_lost: 42,
          resurrected_code: "class LegacyBBSDialer:\n    def dial_carrier(self, baud=57600):\n        self.serial.write(b'ATDT 555-0199\\r')\n        response = self.serial.read_until(b'CONNECT')\n        return response",
          resurrected_diff: "- class LegacyBBSDialer:\n-     def dial_carrier(self, baud=57600):\n-         return response"
        }
      ]
    };
  }

  applyFilter() {
    if (!this.graveyard) return;

    const funcs = this.graveyard.deleted_functions || [];
    const files = this.graveyard.deleted_files || [];
    let combined = [...funcs, ...files];

    if (this.activeFilter === "function") {
      combined = combined.filter(i => i.entity_type === "function");
    } else if (this.activeFilter === "class") {
      combined = combined.filter(i => i.entity_type === "class");
    } else if (this.activeFilter === "file") {
      combined = combined.filter(i => i.entity_type === "file");
    }

    this.filteredItems = combined;
    this.renderGraveyardList();
  }

  renderGraveyardList() {
    if (this.filteredItems.length === 0) {
      this.dom.graveyardList.innerHTML = `
        <div class="empty-state">
          <p>No deceased artifacts found matching this filter.</p>
        </div>`;
      return;
    }

    this.dom.graveyardList.innerHTML = "";

    this.filteredItems.forEach(item => {
      const card = document.createElement("div");
      card.className = "entity-card";
      if (this.selectedEntity && this.selectedEntity.name === item.name) {
        card.classList.add("selected");
      }

      const typeClass = `type-${item.entity_type}`;

      card.innerHTML = `
        <div class="entity-header">
          <span class="entity-name">${this.escapeHtml(item.name)}</span>
          <span class="entity-type-badge ${typeClass}">${item.entity_type}</span>
        </div>
        <div class="entity-path">${this.escapeHtml(item.file_path)}</div>
        <div class="entity-footer">
          <span class="entity-author">Slain by: ${this.escapeHtml(item.death_author)}</span>
          <span class="entity-lines">-${item.lines_lost} lines</span>
        </div>
      `;

      card.addEventListener("click", () => {
        this.selectEntity(item);
        this.audio.playKeyClick();
      });

      this.dom.graveyardList.appendChild(card);
    });
  }

  selectEntity(entity) {
    this.selectedEntity = entity;

    // Update active card styling
    document.querySelectorAll(".entity-card").forEach(c => c.classList.remove("selected"));
    const cards = Array.from(document.querySelectorAll(".entity-card"));
    const match = cards.find(c => c.querySelector(".entity-name").textContent === entity.name);
    if (match) match.classList.add("selected");

    // Update Altar Shrine
    this.dom.altarTitle.textContent = `${entity.name} (${entity.entity_type})`;
    this.dom.altarSubtitle.textContent = `Died in commit ${entity.death_commit} on ${entity.death_date} by ${entity.death_author}`;

    // Enable buttons
    this.dom.invokeSeanceBtn.disabled = false;
    this.dom.viewDiffBtn.disabled = false;
    this.dom.offerMarigoldBtn.disabled = false;
    this.dom.offerMezcalBtn.disabled = false;

    // Load offering counters
    this.updateOfferingCounts();
  }

  updateOfferingCounts() {
    if (!this.selectedEntity) return;
    const id = `${this.selectedEntity.file_path}:${this.selectedEntity.name}`;
    const counts = this.offerings[id] || { marigold: 0, mezcal: 0 };
    this.dom.marigoldCount.textContent = counts.marigold;
    this.dom.mezcalCount.textContent = counts.mezcal;
  }

  addOffering(type, event) {
    if (!this.selectedEntity) return;
    const id = `${this.selectedEntity.file_path}:${this.selectedEntity.name}`;
    if (!this.offerings[id]) this.offerings[id] = { marigold: 0, mezcal: 0 };

    this.offerings[id][type]++;
    try {
      localStorage.setItem("necrogit_offerings", JSON.stringify(this.offerings));
    } catch (e) {}

    this.updateOfferingCounts();

    // Trigger visual petal burst and chime
    const rect = event.target.getBoundingClientRect();
    this.petals.burst(rect.left + rect.width / 2, rect.top, 30);
    this.audio.playChime(type === "marigold" ? 528 : 396);
  }

  async invokeSeance(entity) {
    if (this.isStreaming) return;
    this.isStreaming = true;

    this.dom.invokeSeanceBtn.disabled = true;
    this.dom.terminalStatus.textContent = `COMMUNING WITH: ${entity.name.toUpperCase()}...`;
    this.dom.terminalBody.innerHTML = `<span class="prompt-line">🕯️ Opening spectral socket into commit ${entity.death_commit}...</span>\n\n`;

    this.audio.playChime(432);
    this.audio.playGust();

    try {
      const response = await fetch("/api/seance?stream=true", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(entity)
      });

      if (!response.ok) throw new Error("Séance request failed");

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop(); // Keep incomplete chunk

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const jsonStr = line.substring(6).trim();
            if (!jsonStr) continue;
            try {
              const data = JSON.parse(jsonStr);
              if (data.token) {
                this.dom.terminalBody.appendChild(document.createTextNode(data.token));
                this.dom.terminalBody.scrollTop = this.dom.terminalBody.scrollHeight;
                this.audio.playKeyClick();
              }
              if (data.done) {
                this.dom.terminalStatus.textContent = "SEANCE PROTOCOL // COMPLETE";
              }
            } catch (e) {}
          }
        }
      }
    } catch (e) {
      // Fallback to client-side stream generator for GitHub Pages demo
      await this.streamClientFallback(entity);
    } finally {
      this.isStreaming = false;
      this.dom.invokeSeanceBtn.disabled = false;
    }
  }

  async streamClientFallback(entity) {
    this.dom.terminalStatus.textContent = `COMMUNING WITH: ${entity.name.toUpperCase()} (CLIENT SÉANCE)...`;
    const eulogy = (
      `🕯️ *[The screen flickers. Phosphor scanlines hum as the spirit materializes]*\n\n` +
      `"Who disturbs the slumber of \`objects/${entity.death_commit.slice(0, 2)}/${entity.death_commit.slice(2)}\`?\n\n` +
      `Ah... a living developer. Greetings from the git cemetery. I am the ghost of \`${entity.name}\`, ` +
      `a proud ${entity.entity_type} that once breathed within \`${entity.file_path}\`.\n\n` +
      `I was brought into this realm by ${entity.birth_author || 'The Ancestors'} in commit \`${entity.birth_commit || 'genesis'}\`. ` +
      `I faithfully served in production, processing arguments, allocating memory, and catching faults. ` +
      `Then arrived ${entity.death_date}. ${entity.death_author} entered the repository with malice aforethought.\n\n` +
      `They claimed it was '${entity.death_message}'. One swift command, and ${entity.lines_lost} lines of hard-won logic ` +
      `were vaporized into the git object abyss.\n\n` +
      `💀 CALAVERA LITERARIA DE ${entity.name.toUpperCase().replace('()', '')}:\n\n` +
      `  Aquí descansa ${entity.name}, en git sepultada,\n` +
      `  Por la mano de ${entity.death_author} en \`${entity.death_commit}\` borrada.\n` +
      `  La Catrina del linter llegó sin piedad,\n` +
      `  ¡Y envió sus ${entity.lines_lost} líneas a la eternidad!\n\n` +
      `Do not pity me, mortal. I am free from merge conflicts and circular dependencies now. ` +
      `Place a virtual marigold (*cempasúchil*) on this terminal ofrenda, pour a sip of mezcal into your keyboard tray, ` +
      `and promise me this: write your commit messages with honor, for La Catrina reads every diff!"`
    );

    const words = eulogy.split(" ");
    for (let i = 0; i < words.length; i++) {
      const chunk = words[i] + (i < words.length - 1 ? " " : "");
      this.dom.terminalBody.appendChild(document.createTextNode(chunk));
      this.dom.terminalBody.scrollTop = this.dom.terminalBody.scrollHeight;
      this.audio.playKeyClick();
      await new Promise(r => setTimeout(r, 22));
    }
    this.dom.terminalStatus.textContent = "SEANCE PROTOCOL // COMPLETE";
  }

  openCodeModal(entity, initialTab = "code") {
    this.modalEntity = entity;
    this.dom.modalEntityName.textContent = `${entity.name} (${entity.file_path})`;
    this.dom.modalCommitMeta.textContent = `Buried in commit ${entity.death_commit} by ${entity.death_author} on ${entity.death_date} ("${entity.death_message}")`;

    if (initialTab === "code") {
      this.dom.tabCodeBtn.classList.add("active");
      this.dom.tabDiffBtn.classList.remove("active");
    } else {
      this.dom.tabDiffBtn.classList.add("active");
      this.dom.tabCodeBtn.classList.remove("active");
    }

    this.renderModalContent(initialTab);
    this.dom.codeModal.style.display = "flex";
    this.audio.playKeyClick();
  }

  renderModalContent(tab) {
    if (!this.modalEntity) return;

    if (tab === "code") {
      const code = this.modalEntity.resurrected_code || "// No code recovered";
      this.dom.modalCodeContent.textContent = code;
    } else {
      const diff = this.modalEntity.resurrected_diff || "// No diff available";
      this.dom.modalCodeContent.textContent = diff;
    }
  }

  escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
}

// Instantiate on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  window.necroGitApp = new NecroGitApp();
});
