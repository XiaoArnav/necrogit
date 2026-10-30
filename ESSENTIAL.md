# ⚡ NecroGit: The Essential Runbook & Cheatsheet (ESSENTIAL.md)

Quick-reference operational runbook, command cheatsheet, port map, environment config, Ollama setup, and troubleshooting guide for **NecroGit**.

---

## 1. 🚀 Quickstart Commands

### 1.1 Local Server Launch
Runs on standard Python 3.9+ with **zero external pip dependencies**:

```bash
# Clone the repository
git clone https://github.com/XiaoArnav/necrogit.git
cd necrogit

# Option A: Fast startup script
chmod +x run.sh && ./run.sh

# Option B: Direct Python invocation
python3 app/server.py
```
> **Local Ofrenda Portal:** [`http://localhost:7777`](http://localhost:7777)  
> **Default Port:** `7777` (configurable via `--port <PORT>` or `PORT` env)

### 1.2 CLI Headless Mode
```bash
# Scan repository for deleted code
python3 app/cli.py --scan

# Perform an interactive terminal séance
python3 app/cli.py --seance "legacy_auth_v1"

# Pipe a commit diff into the haunting engine
git diff HEAD~1 | python3 app/cli.py --haunt
```

---

## 2. 🔌 Ports & Network Topology

| Port / Address | Service | Protocol | Function |
| :--- | :--- | :--- | :--- |
| `localhost:7777` | NecroGit Gateway | HTTP/1.1 | Multi-threaded static server & streaming API daemon |
| `localhost:11434` | Local Ollama Engine | HTTP / JSON | Hosts Google Gemma 2 (`gemma2:2b` / `gemma2:9b`) |
| `0.0.0.0:7777` | LAN Portal (Optional) | HTTP/1.1 | Accessible on local Wi-Fi when testing mobile |

---

## 3. 🧠 Local Ollama & Gemma 2 Setup

NecroGit runs 100% offline using open-weight models:

```bash
# Verify Ollama is installed and running
ollama --version

# Pull the high-efficiency 2B open-weight Gemma 2 model
ollama pull gemma2:2b

# Optional: Pull the larger 9B reasoning variant (Apple Silicon / GPU)
ollama pull gemma2:9b

# Verify active models in memory
ollama list
```

> **Fallback Mode:** If Ollama is not running, NecroGit automatically engages its deterministic heuristic necromancer. No crashes, no blocked execution.

---

## 4. 🧪 Verification & Test Suite

Run the zero-dependency test runner:

```bash
# Run unit & behavioral tests
python3 -m unittest discover -s tests -p "test_*.py" -v

# Quick syntax & lint check
python3 -m py_compile app/server.py
```

---

## 5. 🛠️ Troubleshooting Runbook

### Issue A: Port `7777` already in use
```bash
# Find and terminate the dangling process
lsof -ti:7777 | xargs kill -9

# Or run the server on an alternative port
python3 app/server.py --port 8888
```

### Issue B: Ollama model connection refused (`ECONNREFUSED 127.0.0.1:11434`)
* **Cause:** Ollama daemon is stopped.
* **Fix:** Start Ollama with `ollama serve` in a background terminal.
* **Resilience:** The application will seamlessly fallback to heuristic parsing until the daemon comes back online.

### Issue C: Browser serving stale cached files
* **Hard Refresh:** `Cmd + Shift + R` (macOS) or `Ctrl + F5` (Windows/Linux).
* **Verify Headers:** Run `curl -sI http://localhost:7777/` and ensure `Cache-Control: no-cache, no-store, must-revalidate` is present.

---

## 6. 📁 Repository Tree

```text
necrogit/
├── .gitignore                      # Ignore Python caches, temp files, and secrets
├── LICENSE                         # MIT Open-Source License
├── README.md                       # Project overview, hero Xiaohei illustration, quickstart
├── PRD.md                          # Product Requirements Document
├── ARCHITECTURE.md                 # System architecture, topology, and data flows
├── ESSENTIAL.md                    # Operational runbook and cheatsheet
├── eval/                           # Empirical benchmark evaluation suite
│   ├── benchmark.py                # Automated 25-deletion benchmark runner
│   └── BENCHMARK_RESULTS.md        # Scientific evaluation report (recall & accuracy)
├── assets/
│   └── 02-necrogit-seance-ofrenda-xiaohei.jpg # Ian Xiaohei concept illustration
├── app/                            # Application code (server, engine, archaeology)
│   ├── server.py                   # Zero-dependency Python HTTP daemon
│   ├── engine.py                   # Local Gemma 2 inference & fallback necromancer
│   ├── git_archaeology.py          # Deleted function, class & diff excavator
│   └── cli.py                      # Composable POSIX CLI interface
├── public/                         # Web frontend (Amber CRT & Marigold Altar)
│   ├── index.html                  # HTML5 dual surface
│   ├── app.js                      # Client controller & Web Audio procedural synth
│   └── style.css                   # CRT scanlines & cempasúchil particle styling
└── tests/                          # Automated unit test suite
```
