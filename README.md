# 👻 Ghost in the Machine — Hacktoberfest 2026 (Week 4 Grand Finale)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Hacktoberfest: 2026](https://img.shields.io/badge/Hacktoberfest-2026-orange.svg)](https://hacktoberfest.com)
[![DEV Challenge: Ghost in the Machine](https://img.shields.io/badge/DEV%20Challenge-Ghost%20in%20the%20Machine-black.svg)](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)
[![Tag: #hf26challenge](https://img.shields.io/badge/Tag-%23hf26challenge-FF7518.svg)](https://dev.to/t/hf26challenge)
[![Model: Google Gemma 2](https://img.shields.io/badge/Model-Google%20Gemma%202-4285F4.svg)](https://ai.google.dev/gemma)
[![Runtime: Local & Offline](https://img.shields.io/badge/Runtime-100%25%20Air--Gapped-brightgreen.svg)](#)

> **"Between the past and the present, the line grows thinner."**  
> Built for the **Hacktoberfest Open-Source AI Challenge: Week 4 ("Ghost in the Machine")** celebrating Halloween and Día de los Muertos (October 26 – October 31, 2026).  
> A sovereign, air-gapped terminal séance and digital remembrance vault powered entirely by **Google Gemma 2** running on local silicon.

---

## 🎨 The Grand Finale Roadmap (Xiaohei Edition)

![Week 4 Grand Finale Sprint Roadmap](assets/01-week4-roadmap-xiaohei.jpg)

*Xiaohei hauling the red countdown clock toward the October 31 midnight deadline, fed by the stamped progression of Week 1 ([WildTrail](https://github.com/XiaoArnav/wildtrail)), Week 2 ([GhostLedger](https://github.com/XiaoArnav/ghostledger)), and Week 3 ([Compline](https://github.com/XiaoArnav/complineapp)) directly into Completionist status.*

---

## 🕯️ The Concept: What is "Ghost in the Machine"?

When Halloween arrives on October 31 and Día de los Muertos follows on November 1–2, the barrier separating digital memory from the living machine dissolves. 

Most modern AI systems are corporate specters: closed cloud APIs that hoard your memories, telemetry, and terminal histories on external server farms to train proprietary models. 

**Ghost in the Machine (Phantasm)** turns that model on its head:
1. **The Haunted Terminal (POSIX Séance):** Channels the departed spirits of deprecated programming languages, deceased hardware architectures, and abandoned open-source tools directly into your CLI with eerie, poetic machine commentary.
2. **The Digital Ofrenda:** An intimate, sovereign altar for memories, lost software codebases, and digital artifacts. You can write remembrances, preserve oral histories, and weave commemorative folklore.
3. **100% Air-Gapped & Offline:** Operates entirely with the lights and the internet turned off. All model weights and memory tokens remain strictly on your local disk.

---

## 🧠 Why Open Innovation Matters Here

The challenge explicitly asks: *Why does open innovation matter for what you built?*

| Closed Cloud LLM Monopolies | Phantasm (Open-Weight Google Gemma 2) |
| :--- | :--- |
| ❌ Intimate memories and family histories uploaded to cloud servers | ✅ **100% Data Sovereignty:** Memories never leave local disk |
| ❌ Fails completely when internet connectivity drops | ✅ **True Offline Séance:** Runs in pitch darkness or airplane mode |
| ❌ Metered token taxes ($0.03–$0.08/call) bleed users | ✅ **Zero Marginal Cost:** 100% free to run on CPU or Apple Silicon |
| ❌ Closed training sets determine censorship and style | ✅ **Sovereign Personality:** Local system prompt tuning and model control |

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph Client ["Spectral Presentation Layer"]
        CLI["📟 Haunted TTY Terminal (POSIX Pipe / Interactive Shell)"]
        Web["🕯️ Digital Ofrenda Altar (Ambient Candlelit Web Cockpit)"]
    end

    subgraph Core ["Air-Gapped Daemon (Zero External Dependencies)"]
        Server["⚡ Python Standard Library HTTP Daemon (app/server.py)"]
        Router["🔀 Spectral Inference Router (app/engine.py)"]
    end

    subgraph ModelEngine ["Open-Weight Intelligence"]
        Gemma["🧠 Google Gemma 2 (Local Ollama Daemon gemma2:2b / 9b)"]
        Heuristics["⚙️ Offline Heuristic Necromancer (Zero-Downtime Fallback)"]
    end

    subgraph Storage ["Sovereign Altar Vault"]
        Vault["📦 Local POSIX Storage / JSON Altar Archives (Zero Cloud Egress)"]
    end

    CLI --> Router
    Web --> Server
    Server --> Router
    Router --> |Ollama Active| Gemma
    Router --> |Ollama Offline / Offline Mode| Heuristics
    Router --> Vault
```

---

## 🚀 Quickstart

Run with pure Python 3.9+ with **zero external pip dependencies**:

```bash
# 1. Clone the repository
git clone https://github.com/XiaoArnav/week-4.git
cd week-4

# 2. Launch the local daemon
python3 app/server.py
```

Then navigate to [`http://localhost:7777`](http://localhost:7777) in your browser.

### Connect Local Google Gemma 2 (Offline & Air-Gapped)
In a separate terminal window, warm up Google's open-weight model:
```bash
ollama run gemma2:2b
```

### Haunted Terminal CLI Mode
```bash
# Direct CLI terminal invocation
python3 app/cli.py --seance "Resurrect the spirit of Turbo Pascal"

# Pipe shell logs or historical diffs directly into the machine
git log -n 5 | python3 app/cli.py --haunt
```

---

## 📚 Technical Documentation Index

| Document | Purpose & Description |
| :--- | :--- |
| **[`PRD.md`](PRD.md)** | Product Requirements Document: problem space, personas, and Día de los Muertos specs |
| **[`ARCHITECTURE.md`](ARCHITECTURE.md)** | Technical design, inference router, sequence diagrams, and air-gapped security boundary |
| **[`ESSENTIAL.md`](ESSENTIAL.md)** | Operational runbook, port assignments, Ollama setup, and troubleshooting cheatsheet |
| **[`hacktoberfest-week4-schedule.ics`](hacktoberfest-week4-schedule.ics)** | Direct Notion Calendar / Google Calendar sync for Week 4 milestones |

---

## 🏆 Target Prize Tracks

* 🥇 **Overall Winner ($250 USD):** High-craft open-source AI project with comprehensive technical execution and writeup.
* ⭐ **Featured Category: Best Use of Gemma ($200 USD):** Air-gapped on-device inference using Google's Gemma 2 open-weight models.
* 🤝 **Partner Categories:** Sentry Agent Tracing, Temporal durable workflows, DigitalOcean.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — see the LICENSE file for details. Built with 💚 for Hacktoberfest 2026.
