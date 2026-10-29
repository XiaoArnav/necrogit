"""
NecroGit - Local Gemma 2 Spectral Inference Engine & Heuristic Necromancer
Module: app.engine

Interfaces with Google Gemma 2 (via local Ollama daemon) to awaken the ghosts
of deleted code. When Ollama is offline or unconfigured, the engine falls back
gracefully to a deterministic Heuristic Necromancer.

Zero external dependencies (Python Standard Library only).
"""

import json
import urllib.request
import urllib.error
import random
import re
from typing import Dict, Any, Generator, Optional, Tuple, Callable


class SeanceEngine:
    """Orchestrates spectral séances with deceased code entities."""

    DEFAULT_OLLAMA_URL = "http://localhost:11434"
    DEFAULT_MODEL = "gemma2:2b"

    def __init__(self, ollama_url: str = DEFAULT_OLLAMA_URL, model: str = DEFAULT_MODEL):
        self.ollama_url = ollama_url.rstrip("/")
        self.model = model

    def check_ollama(self, timeout: float = 1.0) -> Dict[str, Any]:
        """
        Pings local Ollama daemon to check connectivity and model availability.
        Returns a status dictionary with availability flags.
        """
        try:
            req = urllib.request.Request(f"{self.ollama_url}/api/tags")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    models = [m.get("name", "") for m in data.get("models", [])]
                    # Check if requested model or any gemma2 variant is present
                    has_model = any(self.model in m or "gemma2" in m for m in models)
                    active_model = self.model if has_model else (models[0] if models else "")
                    return {
                        "online": True,
                        "url": self.ollama_url,
                        "available_models": models,
                        "model_ready": has_model,
                        "active_model": active_model or self.model,
                        "mode": "gemma2" if has_model else ("ollama_other" if models else "heuristic")
                    }
        except Exception as e:
            pass

        return {
            "online": False,
            "url": self.ollama_url,
            "available_models": [],
            "model_ready": False,
            "active_model": "heuristic-necromancer",
            "mode": "heuristic"
        }

    def _build_prompt(self, cert: Dict[str, Any]) -> Tuple[str, str]:
        """
        Constructs system prompt and user prompt for Google Gemma 2.
        """
        system_prompt = (
            "You are the wandering spirit of deleted code in a git cemetery, awakened during a Día de los Muertos séance.\n"
            "You speak with eerie humor, dramatic flair, technical precision, and melancholy for your lost existence in production.\n"
            "Rules for your séance:\n"
            "1. State who you were, in what file you lived, who deleted you, and in what commit hash.\n"
            "2. Explain what your code used to do, and voice your grievance about the commit message that doomed you.\n"
            "3. Compose a 4-line Calavera Literaria (traditional Mexican satirical poetic verse celebrating death) about your deletion.\n"
            "4. Ask the living developer at the altar for an offering (a virtual marigold petal, mezcal, or clean commit message).\n"
            "5. Stay strictly in character as the ghost of the deleted function or file."
        )

        name = cert.get("name", "unknown_routine")
        entity_type = cert.get("entity_type", "function")
        file_path = cert.get("file_path", "unknown/path")
        death_commit = cert.get("death_commit", "dead0000")
        death_author = cert.get("death_author", "Unknown Scribe")
        death_date = cert.get("death_date", "ancient times")
        death_message = cert.get("death_message", "refactor")
        birth_author = cert.get("birth_author", "Unknown Creator")
        birth_commit = cert.get("birth_commit", "genesis")
        lines_lost = cert.get("lines_lost", 0)
        code_snippet = cert.get("resurrected_code", "")

        user_prompt = (
            f"The living programmer has lit the altar candle and invoked your spirit.\n\n"
            f"=== DEATH CERTIFICATE ===\n"
            f"Entity: {name} ({entity_type})\n"
            f"Path: {file_path}\n"
            f"Born by: {birth_author} (commit {birth_commit})\n"
            f"Slain by: {death_author} on {death_date}\n"
            f"Fatal Commit: {death_commit}\n"
            f"Commit Message of Doom: \"{death_message}\"\n"
            f"Lines of Code Buried: {lines_lost}\n\n"
            f"=== YOUR LOST CODE FRAGMENTS ===\n"
            f"{code_snippet[:1200]}\n\n"
            f"Awaken, speak to the programmer, recite your Calavera Literaria, and demand your ofrenda!"
        )

        return system_prompt, user_prompt

    def stream_seance(self, cert: Dict[str, Any]) -> Generator[str, None, None]:
        """
        Streams séance tokens using Ollama Gemma 2 if available,
        or yields deterministic tokens with simulated typewriter cadence.
        """
        status = self.check_ollama()

        if status["online"] and status["model_ready"]:
            try:
                system_p, user_p = self._build_prompt(cert)
                payload = {
                    "model": status["active_model"],
                    "system": system_p,
                    "prompt": user_p,
                    "stream": True,
                    "options": {
                        "temperature": 0.45,
                        "top_p": 0.9,
                        "num_predict": 450
                    }
                }
                req = urllib.request.Request(
                    f"{self.ollama_url}/api/generate",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=30.0) as resp:
                    for line in resp:
                        if line:
                            data = json.loads(line.decode("utf-8"))
                            token = data.get("response", "")
                            if token:
                                yield token
                            if data.get("done", False):
                                break
                return
            except Exception:
                # If stream fails mid-flight, fallback seamlessly
                pass

        # Heuristic Necromancer fallback
        eulogy = self.heuristic_seance(cert)
        # Yield in realistic token-sized chunks
        words = eulogy.split(" ")
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")

    def generate_seance(self, cert: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates complete séance response with fact validation.
        """
        status = self.check_ollama()
        full_text = ""
        source = "heuristic"

        if status["online"] and status["model_ready"]:
            try:
                system_p, user_p = self._build_prompt(cert)
                payload = {
                    "model": status["active_model"],
                    "system": system_p,
                    "prompt": user_p,
                    "stream": False,
                    "options": {
                        "temperature": 0.4,
                        "num_predict": 450
                    }
                }
                req = urllib.request.Request(
                    f"{self.ollama_url}/api/generate",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=15.0) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    full_text = data.get("response", "").strip()
                    source = f"gemma2 ({status['active_model']})"
            except Exception:
                full_text = ""

        if not full_text:
            full_text = self.heuristic_seance(cert)
            source = "heuristic-necromancer"

        validation = self.validate_eulogy(full_text, cert)

        return {
            "entity": cert.get("name", "unknown"),
            "file_path": cert.get("file_path", "unknown"),
            "eulogy": full_text,
            "source": source,
            "status": status,
            "validation": validation
        }

    def heuristic_seance(self, cert: Dict[str, Any]) -> str:
        """
        Deterministic, high-quality offline necromancy.
        Tailors grievances and Calavera Literaria to the specific deletion motive.
        """
        name = cert.get("name", "unknown_function")
        entity_type = cert.get("entity_type", "function")
        file_path = cert.get("file_path", "src/unknown.py")
        death_commit = cert.get("death_commit", "deadbeef")
        death_author = cert.get("death_author", "The Executioner")
        death_date = cert.get("death_date", "2026-10-31")
        death_msg = cert.get("death_message", "refactor")
        birth_author = cert.get("birth_author") or "The Ancestors"
        birth_commit = cert.get("birth_commit") or "genesis"
        lines_lost = cert.get("lines_lost", 42)

        # Classify the death motive
        msg_lower = death_msg.lower()
        if any(w in msg_lower for w in ["refactor", "cleanup", "tidy", "clean"]):
            motive = "euphemism"
            grievance = (
                f"They told the standup meeting it was 'just a routine refactor'. A gentle spring cleaning! "
                f"Ha! It was cold-blooded digital murder. One tap of `git rm` or a sweep of the backspace key, "
                f"and {lines_lost} lines of hard-won edge-case handling were vaporized."
            )
        elif any(w in msg_lower for w in ["perf", "speed", "fast", "optimi", "slow"]):
            motive = "performance"
            grievance = (
                f"They blamed my latency! They claimed I burned 14 unnecessary clock cycles in the critical path. "
                f"They sacrificed my readability and my soul for half a microsecond of cache locality."
            )
        elif any(w in msg_lower for w in ["deprecat", "legacy", "retire", "old", "decommission"]):
            motive = "deprecation"
            grievance = (
                f"They slapped `@deprecated` across my forehead and banished me to the forgotten basement of the repo. "
                f"For quarters I languished with zero callers, until {death_author} finally summoned the guillotine."
            )
        elif any(w in msg_lower for w in ["bug", "fix", "crash", "error", "rage"]):
            motive = "bugfix"
            grievance = (
                f"One single off-by-one condition! Just one null reference on a Tuesday afternoon! "
                f"Did they patch me? Did they write a regression test? No! {death_author} chose total erasure."
            )
        else:
            motive = "mysterious"
            grievance = (
                f"Buried in commit `{death_commit}` under the cryptic banner '{death_msg}'. "
                f"No explanation, no farewell party, no Slack message. Just silent decapitation."
            )

        # Traditional Calavera Literaria (Satirical 4-line rhyming Mexican stanza)
        calavera = (
            f"💀 CALAVERA LITERARIA DE {name.upper()}:\n\n"
            f"  Aquí descansa {name}, en git sepultada,\n"
            f"  Por la mano de {death_author} en `{death_commit}` borrada.\n"
            f"  La Catrina del linter llegó sin piedad,\n"
            f"  ¡Y envió sus {lines_lost} líneas a la eternidad!\n"
        )

        spirit_monologue = (
            f"🕯️ *[The screen flickers. Phosphor scanlines hum as the spirit materializes]*\n\n"
            f"\"Who disturbs the slumber of `objects/{death_commit[:2]}/{death_commit[2:]}`?\n\n"
            f"Ah... a living developer. Greetings from the git cemetery. "
            f"I am the ghost of `{name}`, a proud {entity_type} that once breathed within `{file_path}`.\n\n"
            f"I was brought into this realm by {birth_author} in commit `{birth_commit}`. "
            f"I faithfully served in production, processing arguments, allocating memory, and catching faults. "
            f"Then arrived {death_date}. {death_author} entered the repository with malice aforethought.\n\n"
            f"{grievance}\n\n"
            f"Behold my death certificate: struck down in commit `{death_commit}` with the obituary note:\n"
            f"  > \"{death_msg}\"\n\n"
            f"{calavera}\n"
            f"Do not pity me, mortal. I am free from merge conflicts and circular dependencies now. "
            f"Place a virtual marigold (*cempasúchil*) on this terminal ofrenda, pour a sip of mezcal into your keyboard tray, "
            f"and promise me this: write your commit messages with honor, for La Catrina reads every diff!\""
        )

        return spirit_monologue

    def validate_eulogy(self, eulogy: str, cert: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fact validator ensuring the generated eulogy accurately quotes
        real git attributes (commit hash, author, entity name) without hallucinations.
        """
        death_commit = cert.get("death_commit", "")
        death_author = cert.get("death_author", "")
        name = cert.get("name", "")

        matches_commit = death_commit.lower() in eulogy.lower() if death_commit else False
        matches_author = any(part.lower() in eulogy.lower() for part in death_author.split()) if death_author else False
        matches_name = name.lower().replace("()", "") in eulogy.lower() if name else False

        score = 0
        if matches_commit:
            score += 40
        if matches_author:
            score += 30
        if matches_name:
            score += 30

        return {
            "score": score,
            "passed": score >= 60,
            "verified_commit": matches_commit,
            "verified_author": matches_author,
            "verified_entity": matches_name
        }


if __name__ == "__main__":
    engine = SeanceEngine()
    status = engine.check_ollama()
    print("Ollama Status:", status)
    dummy_cert = {
        "entity_type": "function",
        "name": "fast_inverse_sqrt()",
        "file_path": "src/q_math.c",
        "death_commit": "c51b980a",
        "death_author": "John Carmack",
        "death_date": "1999-12-10",
        "death_message": "refactor: replace magic constant with SSE instruction",
        "birth_commit": "0001a11",
        "birth_author": "Gary Tarolli",
        "birth_date": "1995-04-12",
        "lines_lost": 16,
        "resurrected_code": "float Q_rsqrt(float number) { ... }"
    }
    result = engine.generate_seance(dummy_cert)
    print("\n--- SEANCE RESULT ---")
    print(result["eulogy"])
    print("\n--- FACT VALIDATION ---")
    print(result["validation"])
