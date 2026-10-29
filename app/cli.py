"""
NecroGit - Forensic Git Séance POSIX CLI
Module: app.cli

Terminal command-line interface for air-gapped code cemetery excavation,
haunting diff inspection, and live spectral séances.

Zero external dependencies (Python Standard Library only).
"""

import sys
import os

# Ensure repository root is on sys.path for direct script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import argparse
import json
import re
from typing import Optional, List

from app.git_archaeology import GitArchaeologist, DeathCertificate
from app.engine import SeanceEngine

# ANSI Color Codes
AMBER = "\033[38;5;214m"
GOLD = "\033[38;5;220m"
DIM = "\033[2m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RESET = "\033[0m"


def print_banner():
    banner = f"""{AMBER}{BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║  🕯️   N E C R O G I T  //  T H E   G I T   S É A N C E   E N G I N E   🕯️   ║
║      Digital Remembrance Ofrenda for Deleted Functions & Ghost Commits       ║
║            100% Air-Gapped • Local Gemma 2 Inference • Zero-Dep              ║
╚══════════════════════════════════════════════════════════════════════════════╝{RESET}"""
    print(banner)


def cmd_scan(archaeologist: GitArchaeologist, as_json: bool = False):
    """Excavates and prints the repository's graveyard."""
    graveyard = archaeologist.get_full_graveyard()

    if as_json:
        print(json.dumps(graveyard, indent=2))
        return

    print_banner()
    repo_name = graveyard["repository"]
    total = graveyard["total_deceased_artifacts"]
    lines = graveyard["total_lines_buried"]
    is_git = graveyard["is_git_repository"]

    status_tag = f"{GREEN}Valid Git Repo{RESET}" if is_git else f"{RED}Synthetic Demo Mode{RESET}"
    print(f"\n{BOLD}🪦 CEMETERY SURVEY FOR:{RESET} {CYAN}{repo_name}{RESET} [{status_tag}]")
    print(f"Total Deceased Entities: {BOLD}{total}{RESET}  |  Total Lines Buried: {BOLD}{lines:,}{RESET}\n")

    print(f"{BOLD}{'KIND':<10} {'DECEASED ENTITY':<28} {'PATH':<28} {'LINES':<7} {'SLAIN BY':<16} {'COMMIT':<10}{RESET}")
    print("─" * 105)

    all_entities = graveyard["deleted_functions"] + graveyard["deleted_files"]

    for item in all_entities:
        kind = item["entity_type"].upper()
        name = item["name"][:26]
        path = item["file_path"][:26]
        lines_str = str(item["lines_lost"])
        author = item["death_author"][:14]
        commit = item["death_commit"][:8]

        kind_color = GOLD if kind == "FUNCTION" else (MAGENTA if kind == "CLASS" else CYAN)
        print(f"{kind_color}{kind:<10}{RESET} {BOLD}{name:<28}{RESET} {DIM}{path:<28}{RESET} {lines_str:<7} {author:<16} {DIM}{commit:<10}{RESET}")

    print("─" * 105)
    print(f"\n{DIM}Tip: Summon any spirit above via:{RESET} {AMBER}python3 app/cli.py --seance \"<name>\"{RESET}\n")


def cmd_seance(archaeologist: GitArchaeologist, engine: SeanceEngine, entity_query: str):
    """Summons the spirit of a specific deceased function or file."""
    print_banner()
    print(f"\n{AMBER}🕯️ Lighting the ofrenda candles... summoning spirit matching: {BOLD}'{entity_query}'{RESET}...\n")

    graveyard = archaeologist.get_full_graveyard()
    all_entities = graveyard["deleted_functions"] + graveyard["deleted_files"]

    # Match target entity
    query_clean = entity_query.lower().strip().replace("()", "")
    target = None

    for item in all_entities:
        name_clean = item["name"].lower().replace("()", "")
        if query_clean in name_clean or name_clean in query_clean:
            target = item
            break

    if not target:
        # Search by file path
        for item in all_entities:
            if query_clean in item["file_path"].lower():
                target = item
                break

    if not target:
        print(f"{RED}❌ No spirit found in the graveyard matching '{entity_query}'.{RESET}")
        print(f"Run {AMBER}python3 app/cli.py --scan{RESET} to inspect all available spirits.")
        return

    # Print death certificate
    print(f"{BOLD}╔═══════════════════════ DEATH CERTIFICATE ═══════════════════════╗{RESET}")
    print(f"║ {BOLD}Entity:{RESET}  {GOLD}{target['name']}{RESET} ({target['entity_type']})")
    print(f"║ {BOLD}Path:{RESET}    {DIM}{target['file_path']}{RESET}")
    print(f"║ {BOLD}Slain:{RESET}   {target['death_date']} by {BOLD}{target['death_author']}{RESET} in commit `{target['death_commit']}`")
    print(f"║ {BOLD}Motive:{RESET}  \"{target['death_message']}\"")
    print(f"║ {BOLD}Buried:{RESET}  {target['lines_lost']} lines of code")
    print(f"{BOLD}╚═════════════════════════════════════════════════════════════════╝{RESET}\n")

    # Check inference status
    status = engine.check_ollama()
    mode_text = f"{GREEN}Google Gemma 2 ({status['active_model']}){RESET}" if status["model_ready"] else f"{GOLD}Deterministic Heuristic Necromancer (Air-Gapped Fallback){RESET}"
    print(f"{DIM}[Séance Channel: {mode_text}{DIM}]{RESET}\n")

    # Stream the séance with terminal typing rhythm
    for token in engine.stream_seance(target):
        sys.stdout.write(f"{AMBER}{token}{RESET}")
        sys.stdout.flush()
        # Atmospheric pause on punctuation
        if any(token.endswith(p) for p in [".", "!", "?", "\n"]):
            time.sleep(0.04)
        else:
            time.sleep(0.008)

    print("\n\n" + "─" * 70)
    print(f"{DIM}🕯️ The spirit has spoken. Leave your offering in the terminal.{RESET}\n")


def cmd_haunt(engine: SeanceEngine):
    """
    Reads a git diff from stdin and haunts the developer with warnings
    about code lines being condemned to the underworld.
    """
    print_banner()
    print(f"\n{AMBER}👁️ Inhaling stdin diff stream for lingering spirits...{RESET}\n")

    diff_text = sys.stdin.read()
    if not diff_text.strip():
        print(f"{RED}❌ Stdin was empty. Try piping a git diff:{RESET}")
        print(f"  {CYAN}git diff HEAD~1 | python3 app/cli.py --haunt{RESET}\n")
        return

    # Extract deleted functions from the piped diff
    deleted_lines = [l[1:] for l in diff_text.splitlines() if l.startswith("-") and not l.startswith("---")]
    deleted_count = len(deleted_lines)

    func_matches = []
    for line in deleted_lines:
        for pat in GitArchaeologist.DEF_PATTERNS:
            m = pat.search(line)
            if m:
                func_matches.append(m.group(1))
                break

    print(f"{BOLD}⚡ DIFF ANALYSIS:{RESET} {RED}{deleted_count} lines condemned{RESET} across the diff.")
    if func_matches:
        print(f"{BOLD}💀 Condemned Functions:{RESET} {', '.join(func_matches[:5])}")

    # Generate a cautionary haunt message
    synth_cert = {
        "entity_type": "diff",
        "name": func_matches[0] if func_matches else "anonymous_lines",
        "file_path": "staged_changes",
        "death_commit": "uncommitted_staged",
        "death_author": os.environ.get("USER", "Developer"),
        "death_date": time.strftime("%Y-%m-%d"),
        "death_message": "work in progress",
        "birth_commit": "HEAD",
        "birth_author": "Developer",
        "lines_lost": deleted_count,
        "resurrected_code": "\n".join(deleted_lines[:30])
    }

    print(f"\n{BOLD}👻 THE UNCOMMITTED GHOSTS CRY OUT:{RESET}\n")
    for token in engine.stream_seance(synth_cert):
        sys.stdout.write(f"{AMBER}{token}{RESET}")
        sys.stdout.flush()
        time.sleep(0.008)

    print("\n\n" + "─" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="NecroGit: Forensic Terminal Séance & Día de los Muertos Ofrenda",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--scan", action="store_true", help="Excavate and display repository graveyard")
    parser.add_argument("--seance", type=str, metavar="NAME", help="Summon and converse with the ghost of a deleted function/file")
    parser.add_argument("--haunt", action="store_true", help="Inspect a piped git diff from stdin and evoke spirits")
    parser.add_argument("--repo", type=str, default=".", help="Path to git repository (default: .)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted terminal UI")
    parser.add_argument("--ollama-url", type=str, default="http://localhost:11434", help="Local Ollama daemon URL")
    parser.add_argument("--model", type=str, default="gemma2:2b", help="Gemma model identifier")

    args = parser.parse_args()

    archaeologist = GitArchaeologist(args.repo)
    engine = SeanceEngine(ollama_url=args.ollama_url, model=args.model)

    if args.scan:
        cmd_scan(archaeologist, as_json=args.json)
    elif args.seance:
        cmd_seance(archaeologist, engine, args.seance)
    elif args.haunt:
        cmd_haunt(engine)
    else:
        # Default behavior when no flag passed: run scan
        cmd_scan(archaeologist, as_json=args.json)


if __name__ == "__main__":
    main()
