# 🎯 Week 4: Product Requirements Document (PRD)

**Project:** Ghost in the Machine (Phantasm)  
**Theme:** "Ghost in the Machine" — Halloween & Día de los Muertos  
**Challenge:** Hacktoberfest Open-Source AI Challenge (Week 4 Grand Finale)  
**Version:** 1.0.0  
**Target Platform:** Modern Web (Desktop & Mobile, PWA Offline Ready) & POSIX CLI  
**Author:** Arnav Patel ([@XiaoArnav](https://github.com/XiaoArnav))  
**Required Tag:** `#hf26challenge`  
**License:** MIT  

---

## 1. Executive Summary & Product Vision

### 1.1 The Challenge Prompt
Hacktoberfest 2026 Week 4 is the **Grand Finale**:
> *"Build something spooky, or something that honors the past in the spirit of Día de los Muertos, with open-weight models or open-source AI."*  
> (October 26 – October 31, 2026; $2,850 in prizes across 21 winners).

### 1.2 Product Vision: Ghost in the Machine
As modern technology rushes forward, it leaves behind an eerie trail of abandoned software, deprecated codebases, and forgotten digital memories. Meanwhile, proprietary cloud AI platforms exploit human grief and nostalgia by commercializing digital avatars behind subscription paywalls and surveilled databases.

**Ghost in the Machine (Phantasm)** restores dignity, contemplation, and playful gothic horror to computing:
- **Haunted Terminal (Séance CLI):** Possesses the developer's shell, murmuring eerie gothic reflections upon commands, compilation failures, and historical git diffs.
- **Digital Ofrenda (Memory Altar):** A sovereign, candlelit altar celebrating departed open-source technologies, lost projects, and personal memories with marigold-illuminated typography.
- **Resurrection Engine:** Channels deceased architectures (LISP machines, Commodore 64 BASIC, Turbo Pascal, punch cards) into functioning code and poetic folklore.
- **Air-Gapped Sovereignty:** 100% offline, zero-telemetry, zero-cost execution with **Google Gemma 2** running on consumer silicon.

```mermaid
flowchart LR
    W1["🌱 Week 1: Touch Grass<br/>(WildTrail - CLIP Vision)"] --> W2["💼 Week 2: Side Hustle<br/>(GhostLedger - Tax Intelligence)"]
    W2 --> W3["🦥 Week 3: Slow & Steady<br/>(Compline - Sleep Sanctuary)"]
    W3 --> W4["👻 Week 4: Ghost in the Machine<br/>(Phantasm - Digital Ofrenda & Séance)"]
```

---

## 2. Target Audience & User Personas

### 2.1 Persona A: The Nostalgic Systems Hacker ("Dante", 32)
* **Profile:** Senior systems engineer and open-source archivist.
* **Pain Point:** Saddened by the rapid obsolescence of foundational software and tired of sterile, corporate AI chat interfaces.
* **Desire:** A haunted, poetic terminal companion that remembers computing history and breathes spectral life into deprecated tools.

### 2.2 Persona B: The Sovereign Memory Keeper ("Ximena", 26)
* **Profile:** Digital archivist and cultural preservationist.
* **Pain Point:** Refuses to upload family memories, deceased relatives' writings, or cultural histories to corporate cloud AI vendors that retain and monetize private data.
* **Desire:** An air-gapped digital ofrenda that runs strictly on local device storage, generating reverent commemorations and folklore with Google Gemma 2.

---

## 3. Functional Requirements & Feature Sets

### 3.1 The Haunted Terminal (POSIX Séance)
* **CLI Interface (`app/cli.py`):** Accepts standard unix pipes (`cat error.log | python3 app/cli.py --haunt`) and command line flags.
* **Spectral Commentary:** Analyzes code smells, failed build logs, and commit histories, returning eerie, evocative aphorisms formatted with ANSI spectral glows.
* **Dead Language Séancist:** Prompts Gemma 2 with structured archetypes of deceased programming paradigms (APL, ALGOL, Forth, COBOL).

### 3.2 The Digital Ofrenda (Web Altar)
* **Candlelit Marigold Aesthetic:** High-contrast dark gothic canvas with glowing amber candlelight and marigold petals floating across the viewport.
* **Altar Offerings:** Users place digital offerings (a snippet of legacy code, a photo, a memory paragraph) onto the altar.
* **Commemorative Elegy Generator:** Google Gemma 2 weaves an unhurried, respectful memorial narrative that celebrates the offering's impact.

### 3.3 Zero-Dependency Standard Library Core
* Python 3.9+ backend uses strictly standard libraries (`http.server`, `urllib.request`, `json`, `dataclasses`).
* No `pip install`, no node build steps, zero third-party telemetry.

---

## 4. Non-Functional Requirements (NFRs)

| Attribute | Specification | Validation Target |
| :--- | :--- | :--- |
| **Data Privacy** | 100% Air-Gapped | Zero network egress to third-party domains |
| **Inference Time** | Local Gemma 2 Streaming | First token rendered `< 500ms` on Apple Silicon |
| **Fallback Latency** | Offline Heuristic Engine | Instant response (`< 15ms`) if Ollama is absent |
| **Portability** | Multi-OS Support | macOS, Linux, Windows (WSL2 / PowerShell) |

---

## 5. Target Prize Categories

* 🏆 **Overall Winner ($250 USD + DEV++ Membership)**
* ⭐ **Featured Category: Best Use of Gemma ($200 USD):** Local on-device inference using Google's Gemma 2 open-weight model family.
* 🤝 **Partner Categories:** Sentry Agent Tracing, Temporal, DigitalOcean.
