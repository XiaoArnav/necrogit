# 🏛️ NecroGit: System Architecture & Technical Design (ARCHITECTURE.md)

**Project:** NecroGit (The Air-Gapped Code Séance & Digital Ofrenda)  
**Author:** Arnav Patel ([@XiaoArnav](https://github.com/XiaoArnav))  
**Repository:** [https://github.com/XiaoArnav/necrogit](https://github.com/XiaoArnav/necrogit)  
**Status:** In Active Architecture / Implementation  
**License:** MIT  

---

## 1. High-Level Architectural Philosophy

NecroGit adheres to three core tenets established throughout our Hacktoberfest series:

1. **Zero External Runtime Dependencies:** The backend relies strictly on the Python 3.9+ Standard Library (`http.server`, `urllib.request`, `json`, `dataclasses`). No heavy virtual environments, no `pip install` friction, and zero supply-chain attack surface.
2. **Local-First & Air-Gapped Resilience:** AI inference runs entirely on the host machine via **Google Gemma 2** (`gemma2:2b` / `gemma2:9b`) through Ollama. When network connectivity is zero or Ollama is unconfigured, the system cascades gracefully into deterministic local heuristics.
3. **Multi-Surface Accessibility:** The core engine is decoupled from presentation layers, serving both an interactive browser ofrenda and a composable POSIX-compliant CLI stream.

```mermaid
flowchart TD
    subgraph Presentation ["Presentation Layer (Multi-Surface)"]
        UI["🖥️ Modern Vanilla Web App (Amber CRT & Marigold Altar)"]
        CLI["📟 POSIX CLI (stdin / stdout / Unix Pipes)"]
    end

    subgraph Gateway ["Zero-Dependency Gateway Daemon"]
        SRV["⚡ Python Standard HTTP Server (app/server.py)"]
        API["📡 REST Endpoints & Streaming SSE Proxy"]
    end

    subgraph Engine ["Sovereign Intelligence Engine"]
        EXCAVATOR["⛏️ Git Archaeology AST Parser (app/git_archaeology.py)"]
        ROUTER["🔀 Spectral Inference Router (app/engine.py)"]
        OLLAMA["🧠 Local Ollama Daemon (gemma2:2b / 9b)"]
        FALLBACK["⚙️ Deterministic Heuristic Fallback Engine"]
    end

    subgraph Storage ["Local Sovereign Storage"]
        BROWSER["📦 Browser Storage (localStorage / IndexedDB)"]
        FILES["📁 Local POSIX Filesystem / JSON Export"]
    end

    UI --> API
    CLI --> ROUTER
    API --> ROUTER
    ROUTER --> EXCAVATOR
    ROUTER --> |Ollama Available| OLLAMA
    ROUTER --> |Ollama Offline / Timeout| FALLBACK
    UI --> BROWSER
    CLI --> FILES
```

---

## 2. Component Topology

### 2.1 The Web Presentation Layer
* **Vanilla Architecture:** Built without bundlers (Webpack/Vite/Rollup) or heavy frontend frameworks (React/Vue). Direct ES modules load instantly via native HTTP imports.
* **Amber Phosphorus CRT & Marigold Altar:** Canvas-rendered floating cempasúchil petals, glowing terminal amber phosphors, and Web Audio procedural synthesizer.
* **Visual Storytelling:** Integrated with **Ian Xiaohei** minimalist hand-drawn vector art and responsive status telemetry.

### 2.2 The Zero-Dependency Gateway (`app/server.py`)
* Implements `http.server.ThreadingHTTPServer` to handle concurrent local requests.
* Handles static asset serving, MIME resolution (`text/html`, `application/javascript`, `image/svg+xml`, `image/jpeg`), and CORS headers for local development.
* Acts as a non-blocking proxy forwarder to Ollama's local port (`11434`), streaming raw chunked tokens back to the web UI.

### 2.3 The Git Archaeology Engine (`app/git_archaeology.py`)
* Extracts deleted whole files (`git log -p --diff-filter=D -M`).
* Parses diff hunks to identify deleted function and class signatures in surviving files (`-def `, `-class `, `-function `).
* Resolves author attribution, commit date, and deletion commit messages.

### 2.4 The Inference Router & Local Gemma Engine (`app/engine.py`)
```mermaid
sequenceDiagram
    autonumber
    actor User as User / Client
    participant Router as Inference Router
    participant Ollama as Local Ollama (Gemma 2)
    participant Fallback as Heuristic Engine

    User->>Router: Send Séance Request for Function
    Router->>Ollama: Check /api/tags (Healthcheck)
    alt Ollama is Online & Gemma 2 Loaded
        Router->>Ollama: POST /api/generate (Stream=True)
        Ollama-->>Router: Yield Spectral Token Stream
        Router-->>User: Stream Word-by-Word Eulogy
    else Ollama Unreachable / Timed Out (> 1.2s)
        Router->>Fallback: Dispatch Heuristic Necromancer
        Fallback-->>Router: Return Deterministic Calavera Verse
        Router-->>User: Deliver Instant Structured Response (Fallback Mode)
    end
```

---

## 3. Data Flow & Security Boundary

```mermaid
flowchart LR
    subgraph LocalMachine ["Air-Gapped Local Host Environment"]
        UserDevice["💻 User Device (Laptop / Desktop)"]
        LocalRepo["🔒 Git Repository & Objects (.git)"]
        GemmaModel["🧠 Gemma 2 Weights (Local Disk)"]
        
        LocalRepo --> GemmaModel
        GemmaModel --> UserDevice
    end

    subgraph ExternalWeb ["External Network (Cloud)"]
        CloudMonopolies["❌ Closed Cloud AI APIs (Blocked)"]
        Tracking["❌ Telemetry & Trackers (Zero)"]
    end

    LocalMachine -.-x|100% Air-Gapped / No Egress| ExternalWeb
```

* **No Egress Policy:** Absolutely no user telemetry, prompts, or output tokens are transmitted outside `localhost`.
* **Audit Defense:** Every generated report, token stream, or transaction can be verified against local source logs.
