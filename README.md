<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Retro Pixel Koi Profile Studio</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Google Fonts: 'Press Start 2P' and 'VT323' for authentic 8-bit & 16-bit retro vibes -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&family=Silkscreen&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            gb: {
              0: '#0f380f',
              1: '#306230',
              2: '#8bac0f',
              3: '#9bbc0f'
            },
            pixel: {
              dark: '#070a0f',
              panel: '#0d131d',
              border: '#1e293b',
              water: '#0a192f',
              koiRed: '#ff3366',
              koiWhite: '#f8fafc',
              koiGold: '#ffb703',
              green: '#10b981',
              neonBlue: '#38bdf8'
            }
          },
          fontFamily: {
            pixel: ['"Press Start 2P"', 'monospace'],
            vt: ['"VT323"', 'monospace'],
            silk: ['"Silkscreen"', 'monospace'],
            mono: ['"JetBrains Mono"', 'monospace']
          }
        }
      }
    }
  </script>
  <style>
    /* Sharp pixel rendering mode */
    canvas, img, .pixelated {
      image-rendering: pixelated;
      image-rendering: -moz-crisp-edges;
      image-rendering: crisp-edges;
    }

    /* Pixelated retro borders */
    .pixel-box {
      border: 3px solid #38bdf8;
      box-shadow: 0 0 0 2px #0f172a, inset 0 0 0 2px #0f172a;
    }
    .pixel-box-green {
      border: 3px solid #10b981;
      box-shadow: 0 0 0 2px #064e3b, inset 0 0 0 2px #064e3b;
    }

    /* Custom scrollbars */
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: #070a0f;
    }
    ::-webkit-scrollbar-thumb {
      background: #1e293b;
      border: 1px solid #38bdf8;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #38bdf8;
    }

    .retro-scanline {
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
      background-size: 100% 4px;
      pointer-events: none;
    }
  </style>
</head>
<body class="bg-[#070a0f] text-slate-200 h-screen flex flex-col overflow-hidden font-mono select-none">

  <!-- Retro Arcade Top Navigation -->
  <header class="h-14 bg-[#0c121d] border-b-2 border-[#1e293b] flex items-center justify-between px-4 z-20 shrink-0">
    <div class="flex items-center gap-3">
      <!-- 8-Bit Pixel Koi Logo -->
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 bg-sky-950 border-2 border-sky-400 flex items-center justify-center pixelated shadow-sm">
          <span class="text-base">🎏</span>
        </div>
        <div class="flex flex-col">
          <span class="font-pixel text-[11px] text-sky-400 tracking-wider">RETRO-KOI // GITHUB STUDIO</span>
          <span class="font-vt text-xs text-slate-400">8-BIT & 16-BIT PROFILE GENERATOR</span>
        </div>
      </div>

      <div class="h-6 w-px bg-slate-800 mx-2 hidden sm:block"></div>

      <!-- Preset Switchers -->
      <div class="flex items-center gap-1.5 bg-[#070a0f] p-1 border-2 border-[#1e293b] rounded">
        <button id="presetGb" onclick="switchPreset('gameboy')" class="px-2.5 py-1 text-[10px] font-pixel transition-all flex items-center gap-1.5 bg-[#10b981] text-black font-bold">
          <span class="w-2 h-2 bg-emerald-950"></span>
          <span>GB 8-BIT</span>
        </button>
        <button id="presetArcade" onclick="switchPreset('arcade')" class="px-2.5 py-1 text-[10px] font-pixel transition-all flex items-center gap-1.5 text-slate-400 hover:text-white">
          <span class="w-2 h-2 bg-rose-500"></span>
          <span>16-BIT ARCADE</span>
        </button>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex items-center gap-2">
      <button onclick="feedKoi()" class="px-2.5 py-1.5 text-[10px] font-pixel bg-amber-500 hover:bg-amber-400 text-black border-2 border-amber-300 shadow active:translate-y-0.5 transition flex items-center gap-1.5">
        <span>🍙</span>
        <span class="hidden sm:inline">DROP FOOD</span>
      </button>

      <button onclick="copyRawMarkdown()" id="copyBtn" class="px-3 py-1.5 text-[10px] font-pixel bg-sky-500 hover:bg-sky-400 text-black border-2 border-sky-300 shadow active:translate-y-0.5 transition flex items-center gap-1.5">
        <i data-lucide="copy" class="w-3.5 h-3.5"></i>
        <span id="copyBtnText">COPY .MD</span>
      </button>

      <button onclick="resetCurrentTemplate()" title="Reset" class="p-1.5 bg-[#0c121d] hover:bg-slate-800 border-2 border-slate-700 text-slate-300">
        <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
      </button>
    </div>
  </header>

  <!-- Split Screen Workspace -->
  <main class="flex-1 flex flex-col md:flex-row overflow-hidden relative">

    <!-- LEFT PANEL: Monospace Markdown Editor -->
    <section class="w-full md:w-1/2 flex flex-col border-b md:border-b-0 md:border-r-2 border-[#1e293b] bg-[#070b12] h-1/2 md:h-full overflow-hidden">
      <!-- Editor Header -->
      <div class="h-8 px-3 bg-[#0d1420] border-b border-[#1e293b] flex items-center justify-between shrink-0 text-xs">
        <div class="flex items-center gap-2 font-pixel text-[9px] text-sky-400">
          <span>&gt; README.md</span>
          <span class="text-slate-500">[EDITABLE]</span>
        </div>
        <div class="flex items-center gap-2 text-slate-400 font-vt text-sm">
          <span id="statChars">0 CHARS</span>
          <span>|</span>
          <span id="statLines">0 LINES</span>
        </div>
      </div>

      <!-- Editor Body with Pixel Gutter -->
      <div class="flex-1 flex overflow-hidden font-mono text-[13px] leading-6 bg-[#05080e]">
        <div id="lineGutter" class="w-10 py-3 bg-[#090e17] text-slate-600 select-none text-right pr-2 font-mono border-r border-[#1e293b] shrink-0 overflow-hidden text-xs">
          1
        </div>
        <div class="relative flex-1 h-full">
          <textarea
            id="markdownInput"
            spellcheck="false"
            class="w-full h-full p-3 bg-transparent text-emerald-300 font-mono text-[13px] leading-6 resize-none focus:outline-none border-none selection:bg-emerald-800 selection:text-white overflow-auto"
            placeholder="<!-- Paste your 8-bit Markdown here -->"
          ></textarea>
        </div>
      </div>

      <!-- Bottom Helper -->
      <div class="h-6 bg-[#090e17] border-t border-[#1e293b] px-3 flex items-center justify-between text-[11px] font-vt text-slate-400">
        <span class="text-emerald-400 flex items-center gap-1">● SYNC ENGINE READY</span>
        <span>MARKDOWN GFM • 8-BIT FORMAT</span>
      </div>
    </section>

    <!-- RIGHT PANEL: Authentic GitHub Dark Mode Preview with Pixel Pond -->
    <section class="w-full md:w-1/2 flex flex-col bg-[#0d1117] h-1/2 md:h-full overflow-hidden">
      <!-- Preview Header -->
      <div class="h-8 px-3 bg-[#161b22] border-b border-[#30363d] flex items-center justify-between shrink-0 text-xs font-mono">
        <div class="flex items-center gap-2 text-slate-300">
          <i data-lucide="terminal" class="w-3.5 h-3.5 text-emerald-400"></i>
          <span class="text-xs">github.com/retro-dev (DARK MODE)</span>
        </div>
        <span class="font-pixel text-[9px] text-amber-400 animate-pulse">● LIVE PREVIEW</span>
      </div>

      <!-- Scrollable Preview -->
      <div class="flex-1 overflow-y-auto p-4 sm:p-6 bg-[#090d13]">
        <div class="max-w-2xl mx-auto border border-[#30363d] bg-[#0d1117] rounded shadow-2xl overflow-hidden">
          
          <!-- GitHub Repo Tab -->
          <div class="px-3 py-2 bg-[#161b22] border-b border-[#30363d] flex items-center justify-between text-xs text-slate-400 font-mono">
            <div class="flex items-center gap-2">
              <i data-lucide="book-marked" class="w-3.5 h-3.5 text-slate-400"></i>
              <span class="text-slate-300 font-semibold">pixel-koi-dev</span>
              <span>/</span>
              <span class="text-slate-200">README.md</span>
            </div>
            <span class="text-[10px] font-pixel text-sky-400">LVL 42 ARCHITECT</span>
          </div>

          <!-- Pixel Pond Canvas Container -->
          <div class="p-3 bg-[#060b12] border-b border-[#30363d] flex flex-col items-center justify-center relative">
            <div class="w-full flex items-center justify-between px-2 mb-2 font-pixel text-[9px]">
              <span class="text-emerald-400 flex items-center gap-1">
                <span>[POND-STATE]</span> ACTIVE
              </span>
              <span class="text-slate-400 hidden sm:inline">CLICK POND TO DROP FOOD 🍙</span>
            </div>

            <!-- The Pixel Canvas (Integer resolution scaled via CSS) -->
            <div class="relative w-full max-w-md border-4 border-[#1e293b] rounded overflow-hidden shadow-lg shadow-black">
              <canvas id="pixelCanvas" width="240" height="120" class="w-full h-44 bg-[#0a1628] cursor-crosshair pixelated"></canvas>
              <div class="retro-scanline absolute inset-0"></div>
            </div>

            <div class="mt-2 text-center font-vt text-sm text-slate-400">
              ⚡ Pixel Koi Kinematics • Dynamic Steering & Ripple Grid
            </div>
          </div>

          <!-- Dynamic Markdown Render Container -->
          <div id="markdownOutput" class="p-5 sm:p-7 text-slate-200 text-sm leading-relaxed">
            <!-- Dynamically populated -->
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- Notification Toast -->
  <div id="toast" class="fixed bottom-5 right-5 transform translate-y-12 opacity-0 pointer-events-none transition-all duration-300 z-50 flex items-center gap-2 bg-[#10b981] text-black border-2 border-emerald-300 font-pixel text-[10px] px-3.5 py-2 shadow-2xl">
    <span>★</span>
    <span id="toastMsg">COPIED TO CLIPBOARD!</span>
  </div>

  <script>
    // 8-Bit & 16-Bit Pixel Markdown Presets
    const PIXEL_PRESETS = {
      gameboy: `<div align="center">

<!-- Retro Pixel Banner -->
<img src="https://capsule-render.vercel.app/api?type=rect&color=0f380f&height=130&section=header&text=A%20WILD%20DEV%20APPEARED!&fontSize=22&fontAlignY=55&fontColor=9bbc0f" width="100%" />

<br/>

<p align="center">
  <img src="https://img.shields.io/badge/HP-100%2F100-306230?style=for-the-badge&logoColor=9bbc0f" />
  <img src="https://img.shields.io/badge/MANA-MAX%20COFFEE-0f380f?style=for-the-badge&logoColor=8bac0f" />
  <img src="https://img.shields.io/badge/CLASS-FULL--STACK%20WARRIOR-8bac0f?style=for-the-badge&logoColor=0f380f" />
</p>

<h3>🎏 <i>"Feed the koi, clear the backlog, level up."</i></h3>

</div>

---

### 🎮 CHARACTER STATS & STATUS

\`\`\`text
+-------------------------------------------------------------+
| [LVL 42 SOFTWARE ARCHITECT]   STATUS: SWIMMING UPSTREAM     |
| [HP] [||||||||||||||||||||||||||||||||||||||||] 100% COFFEE  |
| [MP] [||||||||||||||||||||||||||||||||||]      85% ALGORITHMS|
| [FOCUS] AGENT SECURITY • QUEUE TELEMETRY • HIGH CONCURRENCY |
+-------------------------------------------------------------+
\`\`\`

---

### 🎒 INVENTORY / TECH ARSENAL

| Weapon Slot | Equipment | Mastery |
| :--- | :--- | :--- |
| **Primary Blade** | \`TypeScript\` \`Python\` \`Go\` \`Java\` | ★★★★★ |
| **Shield & Shell** | \`Next.js\` \`React\` \`TailwindCSS\` | ★★★★★ |
| **Potions & Tools**| \`Docker\` \`PostgreSQL\` \`Redis\` \`Linux\` | ★★★★☆ |

---

### 🗺️ ACTIVE QUEST LOG

- ⚔️ **Quest 01: [AgentShield](#)** — Build a firewall & trust layer between LLM agents and sensitive databases.
- 🏥 **Quest 02: [MediQueue](#)** — Deploy real-time OPD hospital queue telemetry with sub-second sync.
- 📜 **Quest 03: [LeetCode Zen Master](#)** — Slay 500+ data structure & graph dragons.

---

### 👾 8-BIT CONTRIBUTION MATRIX

<div align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=torvalds&show_icons=true&theme=matrix&hide_border=true&bg_color=0f380f&text_color=9bbc0f&icon_color=8bac0f&title_color=9bbc0f" height="145" />
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=torvalds&layout=compact&theme=matrix&hide_border=true&bg_color=0f380f&text_color=9bbc0f&title_color=9bbc0f" height="145" />
</div>

<br/>

<div align="center">
  <sub>PRESS [START] TO COLLABORATE • INSERT COIN TO HIRE</sub>
</div>`,

      arcade: `<div align="center">

<!-- 16-Bit Neon Arcade Banner -->
<img src="https://capsule-render.vercel.app/api?type=cylinder&color=09121d&height=140&section=header&text=16-BIT%20NEON%20KOI%20POND&fontSize=24&fontColor=ff3366&animation=twinkling" width="100%" />

<br/>

<p align="center">
  <img src="https://img.shields.io/badge/STATUS-INSERT%20COIN-ff3366?style=for-the-badge&logoColor=white" />
  <img src="https://img.shields.io/badge/GUILD-OPEN%20SOURCE-38bdf8?style=for-the-badge&logoColor=white" />
  <img src="https://img.shields.io/badge/DIFFICULTY-HARDCORE-ffb703?style=for-the-badge&logoColor=black" />
</p>

<h3>⛩️ <i>"A koi leaping through the dragon gate becomes a legend."</i></h3>

</div>

---

### 🕹️ DIALOGUE WINDOW

\`\`\`text
╔═════════════════════════════════════════════════════════════╗
║ NPC SENIOR DEV:                                             ║
║ "It is dangerous to deploy on Fridays! Take this Next.js    ║
║ microservice and guard the production database!"            ║
╚═════════════════════════════════════════════════════════════╝
\`\`\`

---

### ⚔️ BOSS BATTLES (PROJECTS)

| Stage | Boss / Project | Special Moves & Drops |
| :--- | :--- | :--- |
| **Stage 1** | **[AgentShield]** | Autonomous AI agent firewall with policy verification |
| **Stage 2** | **[MediQueue]** | Zero-latency WebSocket triage engine |
| **Stage 3** | **[VoxelPond]** | 60FPS WebGL retro aquatic physics engine |

---

<div align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=torvalds&show_icons=true&theme=tokyonight&hide_border=true&bg_color=00000000" height="150" />
</div>`
    };

    let activePreset = 'gameboy';
    const editor = document.getElementById('markdownInput');
    const gutter = document.getElementById('lineGutter');
    const output = document.getElementById('markdownOutput');
    const statChars = document.getElementById('statChars');
    const statLines = document.getElementById('statLines');

    editor.value = PIXEL_PRESETS.gameboy;

    // Custom Markdown to Pixel HTML Parser
    function parsePixelMarkdown(md) {
      let html = md;
      html = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');

      // Parse code / dialog blocks
      html = html.replace(/```([a-zA-Z0-9_\-]+)?\n([\s\S]*?)```/g, (match, lang, code) => {
        const clean = code.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        return `
          <div class="my-4 border-2 border-[#1e293b] bg-[#05080f] rounded overflow-hidden shadow-lg">
            <div class="bg-[#0f172a] px-3 py-1 border-b border-[#1e293b] flex items-center justify-between font-pixel text-[9px] text-sky-400">
              <span>► RPG DIALOG / TERMINAL</span>
              <span class="text-slate-500">8-BIT BOX</span>
            </div>
            <pre class="p-3 text-xs font-mono text-emerald-400 overflow-x-auto leading-relaxed"><code>${clean}</code></pre>
          </div>
        `;
      });

      // Parse Tables into Retro Item Grid
      html = html.replace(/\|(.+)\|\n\|[-:\s|]+\|\n((?:\|.*\|\n?)*)/g, (match, headerLine, bodyLines) => {
        const headers = headerLine.split('|').filter(h => h.trim() !== '');
        const rows = bodyLines.trim().split('\n').map(row => 
          row.split('|').filter(c => c.trim() !== '')
        );

        return `
          <div class="my-4 overflow-x-auto border-2 border-[#1e293b] bg-[#070c14] rounded">
            <table class="w-full text-left text-xs border-collapse font-mono">
              <thead class="bg-[#0f172a] text-sky-400 font-pixel text-[9px] border-b border-[#1e293b]">
                <tr>
                  ${headers.map(h => `<th class="p-2 tracking-wider">${h.trim()}</th>`).join('')}
                </tr>
              </thead>
              <tbody class="divide-y divide-[#1e293b] text-slate-300">
                ${rows.map(row => `
                  <tr class="hover:bg-sky-950/20 transition">
                    ${row.map(col => `<td class="p-2">${col.trim()}</td>`).join('')}
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `;
      });

      // Headers
      html = html.replace(/^### (.*$)/gim, '<h3 class="font-pixel text-xs text-sky-400 mt-5 mb-2.5 flex items-center gap-1.5"><span class="text-amber-400">►</span> $1</h3>');
      html = html.replace(/^## (.*$)/gim, '<h2 class="font-pixel text-sm text-emerald-400 mt-6 mb-3 pb-1 border-b-2 border-[#1e293b]">$1</h2>');
      html = html.replace(/^# (.*$)/gim, '<h1 class="font-pixel text-base text-white mt-2 mb-3 pb-1 border-b-2 border-[#1e293b]">$1</h1>');

      // Dividers
      html = html.replace(/^---$/gim, '<hr class="my-5 border-t-2 border-[#1e293b]" />');

      // Inline code
      html = html.replace(/`([^`]+)`/g, '<span class="bg-[#0f172a] text-emerald-300 border border-emerald-900/60 px-1.5 py-0.5 rounded text-xs font-mono">$1</span>');

      // Bold & Italic
      html = html.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-bold text-amber-300">$1</strong>');
      html = html.replace(/\*([^*]+)\*/g, '<em class="italic text-slate-400 font-serif">$1</em>');

      // Bullet lists
      html = html.replace(/^\- (.*$)/gim, '<div class="flex items-start gap-2 my-1 text-xs"><span class="text-emerald-400 font-pixel text-[8px] mt-0.5">■</span><div>$1</div></div>');

      return html;
    }

    function syncPreview() {
      const text = editor.value;
      const lines = text.split('\n');

      let gHTML = '';
      for (let i = 1; i <= lines.length; i++) {
        gHTML += `<div>${i}</div>`;
      }
      gutter.innerHTML = gHTML;

      statChars.textContent = `${text.length} CHARS`;
      statLines.textContent = `${lines.length} LINES`;

      output.innerHTML = parsePixelMarkdown(text);
      lucide.createIcons();
    }

    editor.addEventListener('scroll', () => {
      gutter.scrollTop = editor.scrollTop;
    });

    editor.addEventListener('input', syncPreview);

    function switchPreset(key) {
      activePreset = key;
      const btnGb = document.getElementById('presetGb');
      const btnArcade = document.getElementById('presetArcade');

      if (key === 'gameboy') {
        btnGb.className = 'px-2.5 py-1 text-[10px] font-pixel transition-all flex items-center gap-1.5 bg-[#10b981] text-black font-bold';
        btnArcade.className = 'px-2.5 py-1 text-[10px] font-pixel transition-all flex items-center gap-1.5 text-slate-400 hover:text-white';
        editor.value = PIXEL_PRESETS.gameboy;
        canvasBg = '#07160c';
      } else {
        btnArcade.className = 'px-2.5 py-1 text-[10px] font-pixel transition-all flex items-center gap-1.5 bg-rose-500 text-white font-bold';
        btnGb.className = 'px-2.5 py-1 text-[10px] font-pixel transition-all flex items-center gap-1.5 text-slate-400 hover:text-white';
        editor.value = PIXEL_PRESETS.arcade;
        canvasBg = '#0a1424';
      }

      syncPreview();
      showToast(key === 'gameboy' ? 'GAME BOY 8-BIT ACTIVE' : '16-BIT ARCADE ACTIVE');
    }

    function resetCurrentTemplate() {
      editor.value = PIXEL_PRESETS[activePreset];
      syncPreview();
      showToast('RESET TO DEFAULT');
    }

    function copyRawMarkdown() {
      const text = editor.value;
      const dummy = document.createElement("textarea");
      document.body.appendChild(dummy);
      dummy.value = text;
      dummy.select();
      document.execCommand("copy");
      document.body.removeChild(dummy);

      const copyBtnText = document.getElementById('copyBtnText');
      copyBtnText.innerText = 'COPIED!';
      setTimeout(() => {
        copyBtnText.innerText = 'COPY .MD';
      }, 2000);

      showToast('COPIED TO CLIPBOARD!');
    }

    function showToast(msg) {
      const toast = document.getElementById('toast');
      const toastMsg = document.getElementById('toastMsg');
      toastMsg.innerText = msg;
      toast.classList.remove('opacity-0', 'translate-y-12', 'pointer-events-none');
      toast.classList.add('opacity-100', 'translate-y-0');

      setTimeout(() => {
        toast.classList.remove('opacity-100', 'translate-y-0');
        toast.classList.add('opacity-0', 'translate-y-12', 'pointer-events-none');
      }, 2000);
    }

    /* ==========================================================
       AUTHENTIC 8-BIT / 16-BIT PIXEL ART POND ENGINE
       Integer grid calculation with pixel food, lilypads & koi
    ========================================================== */
    const canvas = document.getElementById('pixelCanvas');
    const ctx = canvas.getContext('2d');
    ctx.imageSmoothingEnabled = false;

    let canvasBg = '#07160c';
    const foods = [];
    const pixelRipples = [];
    const lilypads = [
      { x: 30, y: 25, r: 10, notch: 0.4 },
      { x: 195, y: 85, r: 12, notch: 2.2 },
      { x: 120, y: 15, r: 8, notch: 1.1 }
    ];

    // Pixel food drop
    function feedKoi(dropX, dropY) {
      const x = dropX !== undefined ? dropX : Math.floor(Math.random() * 180 + 30);
      const y = dropY !== undefined ? dropY : Math.floor(Math.random() * 80 + 20);
      foods.push({ x: Math.floor(x), y: Math.floor(y), life: 300 });

      // Spawn pixel ripple
      pixelRipples.push({ x, y, step: 0, maxStep: 16 });
      showToast('🍙 FOOD DROPPED!');
    }

    // 8-Bit Pixel Koi Kinematics
    class PixelKoi {
      constructor(colorBody, colorFin, colorPattern, speed) {
        this.x = Math.random() * 180 + 30;
        this.y = Math.random() * 80 + 20;
        this.angle = Math.random() * Math.PI * 2;
        this.targetAngle = this.angle;
        this.speed = speed;
        this.colorBody = colorBody;
        this.colorFin = colorFin;
        this.colorPattern = colorPattern;
        this.tailWiggle = 0;
        
        // 6 spine segments for retro segmented motion
        this.segments = [];
        for (let i = 0; i < 6; i++) {
          this.segments.push({ x: this.x - i * 3, y: this.y });
        }
      }

      update() {
        this.tailWiggle += 0.2;

        // Check if food exists, seek nearest food pellet
        if (foods.length > 0) {
          let closest = foods[0];
          let minDist = 9999;
          foods.forEach(f => {
            const d = Math.hypot(f.x - this.x, f.y - this.y);
            if (d < minDist) {
              minDist = d;
              closest = f;
            }
          });

          this.targetAngle = Math.atan2(closest.y - this.y, closest.x - this.x);

          // Eat food
          if (minDist < 6) {
            const idx = foods.indexOf(closest);
            if (idx > -1) {
              foods.splice(idx, 1);
              pixelRipples.push({ x: this.x, y: this.y, step: 0, maxStep: 12 });
            }
          }
        } else {
          // Wander naturally
          if (Math.random() < 0.04) {
            this.targetAngle += (Math.random() - 0.5) * 1.8;
          }
        }

        // Keep inside bounds
        const m = 18;
        if (this.x < m) this.targetAngle = 0;
        else if (this.x > 240 - m) this.targetAngle = Math.PI;
        if (this.y < m) this.targetAngle = Math.PI / 2;
        else if (this.y > 120 - m) this.targetAngle = -Math.PI / 2;

        // Angle interp
        let da = this.targetAngle - this.angle;
        while (da < -Math.PI) da += Math.PI * 2;
        while (da > Math.PI) da -= Math.PI * 2;
        this.angle += da * 0.08;

        // Move head
        this.x += Math.cos(this.angle) * this.speed;
        this.y += Math.sin(this.angle) * this.speed;

        this.segments[0] = { x: this.x, y: this.y };
        for (let i = 1; i < this.segments.length; i++) {
          const prev = this.segments[i - 1];
          const curr = this.segments[i];
          const dx = curr.x - prev.x;
          const dy = curr.y - prev.y;
          const dist = Math.hypot(dx, dy);
          const targetDist = 3.2;
          if (dist > 0) {
            curr.x = prev.x + (dx / dist) * targetDist;
            curr.y = prev.y + (dy / dist) * targetDist;
          }
        }
      }

      draw(c) {
        // Draw segmented pixel body using integer blocks
        for (let i = this.segments.length - 1; i >= 0; i--) {
          const pt = this.segments[i];
          const px = Math.floor(pt.x);
          const py = Math.floor(pt.y);

          if (i === 0) {
            // Head (4x4 block with eye)
            c.fillStyle = this.colorBody;
            c.fillRect(px - 2, py - 2, 4, 4);

            // Red/Gold Pattern spot
            c.fillStyle = this.colorPattern;
            c.fillRect(px - 1, py - 1, 2, 2);

            // Eye dot
            c.fillStyle = '#000000';
            c.fillRect(px, py - 1, 1, 1);
          } else if (i === 1 || i === 2) {
            // Main torso (5x5 & 4x4)
            c.fillStyle = (i === 2) ? this.colorPattern : this.colorBody;
            c.fillRect(px - 2, py - 2, 4, 4);

            // 8-bit Pectoral Fins
            c.fillStyle = this.colorFin;
            const finWiggle = Math.sin(this.tailWiggle) * 1.5;
            c.fillRect(px - 4, py - 1 + finWiggle, 2, 2);
            c.fillRect(px + 3, py - 1 - finWiggle, 2, 2);
          } else if (i === 3 || i === 4) {
            // Tapering body
            c.fillStyle = (i === 3) ? this.colorPattern : this.colorBody;
            c.fillRect(px - 1, py - 1, 3, 3);
          } else {
            // 8-Bit Tail
            const wiggle = Math.sin(this.tailWiggle * 1.5) * 2;
            c.fillStyle = this.colorFin;
            c.fillRect(px - 1 + wiggle, py - 1, 3, 2);
            c.fillRect(px - 2 + wiggle, py, 4, 2);
          }
        }
      }
    }

    // Two Nishikigoi: Kohaku (White & Crimson) and Yamabuki (Golden Yellow)
    const pixelKoiSchool = [
      new PixelKoi('#f8fafc', '#93c5fd', '#ff3366', 0.9), // Kohaku
      new PixelKoi('#ffb703', '#fbbf24', '#f97316', 0.8), // Yamabuki Gold
      new PixelKoi('#e2e8f0', '#38bdf8', '#0284c7', 0.95) // Asagi Blue
    ];

    // Pixel Pond Rendering Loop
    function renderPond() {
      // Clear with dark pond background
      ctx.fillStyle = canvasBg;
      ctx.fillRect(0, 0, 240, 120);

      // Draw 8-Bit Pixel Water Grid Dots
      ctx.fillStyle = 'rgba(56, 189, 248, 0.08)';
      for (let x = 8; x < 240; x += 12) {
        for (let y = 8; y < 120; y += 12) {
          ctx.fillRect(x, y, 1, 1);
        }
      }

      // Draw Pixel Lily Pads
      lilypads.forEach(l => {
        ctx.fillStyle = '#15803d'; // Forest green
        ctx.beginPath();
        ctx.arc(l.x, l.y, l.r, 0, Math.PI * 2);
        ctx.fill();

        // 8-bit notch
        ctx.fillStyle = canvasBg;
        ctx.fillRect(l.x, l.y - 1, l.r, 2);

        // Center flower bud dot
        ctx.fillStyle = '#f472b6';
        ctx.fillRect(l.x - 1, l.y - 1, 2, 2);
      });

      // Update & Draw Food Pellets
      for (let i = foods.length - 1; i >= 0; i--) {
        const f = foods[i];
        f.life--;
        if (f.life <= 0) {
          foods.splice(i, 1);
          continue;
        }

        // Draw 3x3 pixel onigiri / food pellet
        ctx.fillStyle = '#fef08a';
        ctx.fillRect(f.x - 1, f.y - 1, 3, 3);
        ctx.fillStyle = '#854d0e';
        ctx.fillRect(f.x, f.y, 1, 1);
      }

      // Update & Draw Expanding Pixel Stepped Ripples
      for (let i = pixelRipples.length - 1; i >= 0; i--) {
        const rip = pixelRipples[i];
        rip.step += 0.4;
        if (rip.step >= rip.maxStep) {
          pixelRipples.splice(i, 1);
          continue;
        }

        const r = Math.floor(rip.step);
        ctx.strokeStyle = (activePreset === 'gameboy') ? '#8bac0f' : '#38bdf8';
        ctx.strokeRect(rip.x - r, rip.y - r, r * 2, r * 2);
      }

      // Update & Draw Pixel Koi
      pixelKoiSchool.forEach(koi => {
        koi.update();
        koi.draw(ctx);
      });

      requestAnimationFrame(renderPond);
    }

    // Canvas click to feed
    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const scaleX = 240 / rect.width;
      const scaleY = 120 / rect.height;
      const x = (e.clientX - rect.x) * scaleX;
      const y = (e.clientY - rect.y) * scaleY;
      feedKoi(x, y);
    });

    window.onload = function() {
      syncPreview();
      renderPond();
      lucide.createIcons();
    };
  </script>
</body>
</html>
