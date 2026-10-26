# ⚡ Week 4: The Essential Runbook & Cheatsheet (ESSENTIAL.md)

Quick-reference operational runbook, command cheatsheet, port map, environment config, Ollama setup, and troubleshooting guide for **Week 4**.

---

## 1. 🚀 Quickstart Commands

### 1.1 Local Server Launch
Runs on standard Python 3.9+ with **zero external pip dependencies**:

```bash
# Clone the repository
git clone https://github.com/XiaoArnav/week-4.git
cd week-4

# Option A: Fast startup script
chmod +x run.sh && ./run.sh

# Option B: Direct Python invocation
python3 app/server.py
```
> **Local Portal:** [`http://localhost:7777`](http://localhost:7777)  
> **Default Port:** `7777` (configurable via `--port <PORT>` or `PORT` env)

### 1.2 CLI Headless Mode
```bash
# Direct task execution via standard input
echo "Analyze task" | python3 app/cli.py

# Format as structured JSON
python3 app/cli.py --query "Summarize" --json
```

---

## 2. 🔌 Ports & Network Topology

| Port / Address | Service | Protocol | Function |
| :--- | :--- | :--- | :--- |
| `localhost:7777` | Week-4 Python Gateway | HTTP/1.1 | Multi-threaded static server & streaming API daemon |
| `localhost:11434` | Local Ollama Engine | HTTP / JSON | Hosts Google Gemma 2 (`gemma2:2b` / `gemma2:9b`) |
| `0.0.0.0:7777` | LAN Portal (Optional) | HTTP/1.1 | Accessible on local Wi-Fi when testing mobile |

---

## 3. 🧠 Local Ollama & Gemma 2 Setup

Week 4 is designed to run 100% offline using open-weight models:

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

> **Fallback Mode:** If Ollama is not running, the application automatically engages the deterministic heuristic engine. No crashes, no blocked execution.

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
week-4/
├── .gitignore                      # Ignore Python caches, temp files, and secrets
├── LICENSE                         # MIT Open-Source License
├── README.md                       # Project overview, hero Xiaohei illustration, quickstart
├── PRD.md                          # Product Requirements Document
├── ARCHITECTURE.md                 # System architecture, topology, and data flows
├── ESSENTIAL.md                    # Operational runbook and cheatsheet
├── hacktoberfest-week4-schedule.ics# Notion / Google Calendar sprint schedule
├── assets/
│   └── 01-week4-roadmap-xiaohei.jpg# Ian Xiaohei conceptual sprint illustration
├── app/                            # Application code (server, engine, routes)
│   ├── server.py                   # Zero-dependency Python HTTP daemon
│   └── cli.py                      # Composable POSIX CLI interface
└── tests/                          # Automated unit test suite
```
