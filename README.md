# 🪦 NecroGit: The Air-Gapped Code Séance & Digital Ofrenda

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Hacktoberfest: 2026](https://img.shields.io/badge/Hacktoberfest-2026-orange.svg)](https://hacktoberfest.com)
[![DEV Challenge: Ghost in the Machine](https://img.shields.io/badge/DEV%20Challenge-Ghost%20in%20the%20Machine-black.svg)](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)
[![Tag: #hf26challenge](https://img.shields.io/badge/Tag-%23hf26challenge-FF7518.svg)](https://dev.to/t/hf26challenge)
[![Model: Google Gemma 2](https://img.shields.io/badge/Model-Google%20Gemma%202-4285F4.svg)](https://ai.google.dev/gemma)
[![Runtime: Local & Offline](https://img.shields.io/badge/Runtime-100%25%20Air--Gapped-brightgreen.svg)](#)
[![Live Demo: GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-FF7500.svg)](https://xiaoarnav.github.io/necrogit/)
[![Live Mirror: Vercel](https://img.shields.io/badge/Live%20Mirror-Vercel-000000.svg?logo=vercel&logoColor=white)](https://necrogit.vercel.app)

> **"Code dies. But its ghost lingers forever in `.git`."**  
> Built for the **Hacktoberfest Open-Source AI Challenge: Week 4 ("Ghost in the Machine")** celebrating Halloween and Día de los Muertos (October 26 – October 31, 2026).  
> **Live 1-Click Interactive Altar:** [https://xiaoarnav.github.io/necrogit/](https://xiaoarnav.github.io/necrogit/) *(Backup Mirror: [https://necrogit.vercel.app](https://necrogit.vercel.app))*  
> An air-gapped forensic terminal séance and digital remembrance ofrenda for deleted functions, abandoned classes, and buried software architectures powered entirely by **Google Gemma 2** running on local silicon.

---

## 🎨 The Entire Project in One Picture (Xiaohei Edition)

![NecroGit: The Air-Gapped Code Séance & Digital Ofrenda](assets/02-necrogit-seance-ofrenda-xiaohei.jpg)

*Xiaohei solemnly exhuming a departed `def legacy_worker()` scroll from the `.git/objects` graveyard with mechanical tongs and transferring it onto the candlelit marigold ofrenda altar powered by local Google Gemma 2, completely air-gapped from cloud AI.*

---

## 🕯️ The Concept: What is NecroGit?

When Halloween arrives on October 31 and Día de los Muertos follows on November 1–2, the line between living software and buried code grows thin.

Every git repository is a cemetery. Functions that survived brutal production outages are refactored away. Classes written late at night are deleted with a single callous commit: `refactor: remove legacy worker`. 

**NecroGit** gives departed code a voice and an altar:
1. **The Forensic Git Excavator:** Deeply inspects your repository's commit history (`git log -p -M`), recovering not just whole deleted files, but **deleted functions, deprecated classes, and abandoned commits**.
2. **The Terminal Séance (`--seance`):** Summons the spirit of a deleted function. Powered by local **Google Gemma 2**, the code roleplays in your shell, explaining what purpose it served, what bug broke it, and what lesson it left behind.
3. **The Digital Code Ofrenda:** An interactive browser sanctuary rendered in amber CRT phosphor and fluttering marigold petals (*cempasúchil*). Place dead code artifacts onto altar tiers, view side-by-side resurrected diffs, and read commemorative *calaveras literarias*.
4. **100% Air-Gapped & Sovereign:** Zero cloud APIs. Zero external tracking. Your proprietary code and git histories never leave your laptop.

---

## 🧠 Why Open Innovation Matters Here

The challenge asks: *Why does open innovation matter for what you built?*

| Closed Cloud LLMs (OpenAI / Anthropic) | NecroGit (Local Open-Weight Google Gemma 2) |
| :--- | :--- |
| ❌ Uploading private git histories leaks proprietary code, keys, and NDAs | ✅ **100% Data Sovereignty:** Code never leaves local memory |
| ❌ Fails completely when internet connectivity drops | ✅ **True Air-Gap:** Runs in pitch darkness or airplane mode |
| ❌ Pay-per-token API fees ($0.03–$0.08/call) punish deep repository scans | ✅ **Zero Marginal Cost:** 100% free to run on CPU or Apple Silicon |
| ❌ Corporate content policies sanitize and standardize output | ✅ **Sovereign Persona:** Unfiltered historical technical roleplay |

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph RepoGraveyard ["1. The Git Graveyard (.git)"]
        GitLog["📜 git log -p --diff-filter=D -M"]
        GitObjects["📦 Dangling Commits & Killed Functions"]
    end

    subgraph ForensicEngine ["2. Air-Gapped Python Daemon (StdLib)"]
        Excavator["⚡ git_archaeology.py (Function AST & Diff Parser)"]
        Router["🔀 Spectral Inference Router (app/engine.py)"]
    end

    subgraph Intelligence ["3. Open-Weight Model Core"]
        Gemma["🧠 Google Gemma 2 (Local Ollama gemma2:2b / 9b)"]
        Fallback["⚙️ Deterministic Heuristic Necromancer (Zero Downtime)"]
    end

    subgraph DualSurface ["4. The Dual Surface Experience"]
        CLI["📟 Haunted TTY Terminal (POSIX Pipe / Interactive Shell)"]
        Altar["🕯️ Digital Code Ofrenda (Amber CRT & Marigold Canvas)"]
    end

    RepoGraveyard --> ForensicEngine
    ForensicEngine --> Intelligence
    Intelligence --> DualSurface
```

---

## 🚀 Quickstart

Run with pure Python 3.9+ with **zero external pip dependencies**:

```bash
# 1. Clone the repository
git clone https://github.com/XiaoArnav/necrogit.git
cd necrogit

# 2. Launch the local daemon & web ofrenda
python3 app/server.py
# (Or use the quick launcher: chmod +x run.sh && ./run.sh)

# 3. Run the zero-dependency test suite
python3 -m unittest discover -s tests -p "test_*.py" -v
```

Then navigate to [`http://localhost:7777`](http://localhost:7777) in your browser.

### Connect Local Google Gemma 2 (Offline & Air-Gapped)
In a separate terminal window, warm up Google's open-weight model:
```bash
ollama run gemma2:2b
```

### Haunted Terminal CLI Mode
```bash
# Run a forensic scan on the current repository
python3 app/cli.py --scan

# Hold an interactive séance with a specific departed function
python3 app/cli.py --seance "legacy_auth_v1"

# Pipe shell logs or historical diffs directly into the machine
git log -n 5 -p | python3 app/cli.py --haunt
```

---

## 🏁 The Grand Finale Roadmap

![Week 4 Grand Finale Sprint Roadmap](assets/01-week4-roadmap-xiaohei.jpg)

*Xiaohei hauling the countdown clock toward the October 31 deadline, continuing the shipped progression of Week 1 ([WildTrail](https://github.com/XiaoArnav/wildtrail)), Week 2 ([GhostLedger](https://github.com/XiaoArnav/ghostledger)), and Week 3 ([Compline](https://github.com/XiaoArnav/complineapp)).*

---

## 📚 Technical Documentation Index

| Document | Purpose & Description |
| :--- | :--- |
| **[`PRD.md`](PRD.md)** | Product Requirements Document: problem space, personas, and Día de los Muertos specs |
| **[`ARCHITECTURE.md`](ARCHITECTURE.md)** | Technical design, inference router, sequence diagrams, and air-gapped security boundary |
| **[`ESSENTIAL.md`](ESSENTIAL.md)** | Operational runbook, port assignments, Ollama setup, and troubleshooting cheatsheet |
| **[`eval/BENCHMARK_RESULTS.md`](eval/BENCHMARK_RESULTS.md)** | Empirical benchmark: 4.0x AST granularity gain, 100% commit fidelity, 0B egress |
| **[`hacktoberfest-week4-schedule.ics`](hacktoberfest-week4-schedule.ics)** | Direct Notion Calendar / Google Calendar sync for Week 4 milestones |

---

## 🏆 Target Prize Tracks

* 🥇 **Overall Winner ($250 USD):** High-craft open-source AI project with comprehensive technical execution and writeup.
* ⭐ **Featured Category: Best Use of Gemma ($200 USD):** Air-gapped on-device inference using Google's Gemma 2 open-weight models.
* 🤝 **Partner Categories:** Sentry Agent Tracing, Temporal durable workflows, DigitalOcean.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — see the LICENSE file for details. Built with 💚 for Hacktoberfest 2026.
