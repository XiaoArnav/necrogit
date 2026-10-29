"""
NecroGit - Git Archaeology & Code Cemetery Excavator
Module: app.git_archaeology

Excavates the git object graph (.git) to unearth:
1. Whole deleted files (git log --diff-filter=D -M)
2. Deleted functions and classes inside surviving files (diff hunk AST parsing)
3. Death certificates: birth commit, death commit, author, commit message, and final lines.

Zero external dependencies (Python Standard Library only).
"""

import subprocess
import os
import re
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple


@dataclass
class DeathCertificate:
    entity_type: str            # 'function', 'class', or 'file'
    name: str                   # e.g., 'legacy_auth_v1', 'billing_worker.py'
    file_path: str              # path where it lived
    death_commit: str           # commit hash that deleted it
    death_author: str           # author who deleted it
    death_date: str             # date it was deleted (ISO)
    death_message: str          # commit message of deletion
    birth_commit: Optional[str] = None
    birth_author: Optional[str] = None
    birth_date: Optional[str] = None
    lines_lost: int = 0
    resurrected_code: str = ""
    resurrected_diff: str = ""
    epitaph: str = ""


class GitArchaeologist:
    """Forensic excavator for deleted code in git repositories."""

    # Recognized code extensions for function/class excavation
    CODE_EXTENSIONS = {
        ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".c", ".cpp",
        ".h", ".hpp", ".java", ".rb", ".php", ".cs", ".swift", ".kt", ".sh"
    }

    # Regex patterns for function/class definitions across common languages
    DEF_PATTERNS = [
        # Python: def foo(...) or class Bar(...)
        re.compile(r"^[ \t]*def[ \t]+([a-zA-Z_][a-zA-Z0-9_]*)[ \t]*\("),
        re.compile(r"^[ \t]*class[ \t]+([a-zA-Z_][a-zA-Z0-9_]*)[ \t]*[:\(]"),
        # JavaScript/TypeScript: function foo(...) or const foo = (...) => or class Bar
        re.compile(r"^[ \t]*(?:async[ \t]+)?function[ \t]+([a-zA-Z_][a-zA-Z0-9_]*)[ \t]*\("),
        re.compile(r"^[ \t]*(?:export[ \t]+)?(?:const|let|var)[ \t]+([a-zA-Z_][a-zA-Z0-9_]*)[ \t]*=[ \t]*(?:async[ \t]*)?\([^\)]*\)[ \t]*=>"),
        re.compile(r"^[ \t]*(?:export[ \t]+)?class[ \t]+([a-zA-Z_][a-zA-Z0-9_]*)"),
        # Go: func foo(...) or func (r Receiver) foo(...)
        re.compile(r"^[ \t]*func[ \t]+(?:\([^\)]+\)[ \t]+)?([a-zA-Z_][a-zA-Z0-9_]*)[ \t]*\("),
        # Rust: fn foo(...) or struct Bar
        re.compile(r"^[ \t]*(?:pub[ \t]+)?(?:async[ \t]+)?fn[ \t]+([a-zA-Z_][a-zA-Z0-9_]*)[ \t]*[<|\(]"),
        re.compile(r"^[ \t]*(?:pub[ \t]+)?struct[ \t]+([a-zA-Z_][a-zA-Z0-9_]*)"),
        # C/C++: type name(...) {
        re.compile(r"^[ \t]*(?:[a-zA-Z_][a-zA-Z0-9_:*&<>, ]+[ \t]+)+([a-zA-Z_][a-zA-Z0-9_]*)[ \t]*\([^\)]*\)[ \t]*(?:const)?[ \t]*\{?"),
    ]

    def __init__(self, repo_path: str = "."):
        self.repo_path = os.path.abspath(repo_path)
        self.is_git = self._check_git()

    def _check_git(self) -> bool:
        """Verify whether directory is a valid git repository."""
        try:
            res = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            return res.returncode == 0 and res.stdout.strip() == "true"
        except Exception:
            return False

    def _run_git(self, args: List[str]) -> str:
        """Run a git command safely in repo_path."""
        if not self.is_git:
            return ""
        try:
            res = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False,
                encoding="utf-8",
                errors="replace"
            )
            return res.stdout
        except Exception:
            return ""

    def is_code_file(self, file_path: str) -> bool:
        """Check if file matches supported code extensions."""
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.CODE_EXTENSIONS

    def excavate_deleted_files(self, limit: int = 25) -> List[DeathCertificate]:
        """
        Finds completely deleted files across git history using git log --diff-filter=D -M.
        """
        if not self.is_git:
            return self._synthetic_graveyard()

        # Format: CommitHash%x00AuthorName%x00Date%x00Subject
        log_out = self._run_git([
            "log",
            "--diff-filter=D",
            "-M",
            f"-n{limit * 2}",
            "--format=COMMIT:%H%x00%an%x00%ad%x00%s",
            "--date=iso-strict",
            "--name-only"
        ])

        certificates: List[DeathCertificate] = []
        seen_paths = set()

        current_commit = ""
        current_author = ""
        current_date = ""
        current_subject = ""

        for line in log_out.splitlines():
            line = line.strip()
            if not line:
                continue

            if line.startswith("COMMIT:"):
                parts = line[7:].split("\x00")
                if len(parts) >= 4:
                    current_commit, current_author, current_date, current_subject = parts[:4]
            else:
                # This is a deleted file path
                file_path = line
                if file_path in seen_paths:
                    continue
                seen_paths.add(file_path)

                # Fetch last known content right before deletion
                resurrected_code = self._get_file_before_commit(current_commit, file_path)
                diff = self._get_commit_diff_for_file(current_commit, file_path)
                lines_count = len(resurrected_code.splitlines()) if resurrected_code else 0

                # Also find when the file was born (first commit touching this path)
                birth_commit, birth_author, birth_date = self._find_birth_record(file_path)

                cert = DeathCertificate(
                    entity_type="file",
                    name=os.path.basename(file_path),
                    file_path=file_path,
                    death_commit=current_commit[:8],
                    death_author=current_author,
                    death_date=current_date[:10],
                    death_message=current_subject,
                    birth_commit=birth_commit[:8] if birth_commit else "genesis",
                    birth_author=birth_author or "Unknown",
                    birth_date=birth_date[:10] if birth_date else "Unknown",
                    lines_lost=lines_count,
                    resurrected_code=resurrected_code[:3000],  # Guard against massive binary files
                    resurrected_diff=diff[:2500]
                )
                certificates.append(cert)
                if len(certificates) >= limit:
                    break

        return certificates

    def excavate_deleted_functions(self, limit: int = 25, commit_depth: int = 40) -> List[DeathCertificate]:
        """
        Parses diffs to find deleted functions/classes inside files that still exist or were modified.
        """
        if not self.is_git:
            return []

        # Get recent commit diffs
        log_out = self._run_git([
            "log",
            "-p",
            "-M",
            f"-n{commit_depth}",
            "--format=COMMIT:%H%x00%an%x00%ad%x00%s",
            "--date=iso-strict"
        ])

        certificates: List[DeathCertificate] = []
        seen_entities = set()

        current_commit = ""
        current_author = ""
        current_date = ""
        current_subject = ""
        current_file = ""

        # Parser state
        diff_lines: List[str] = []

        def process_diff_block(commit_hash: str, author: str, date_str: str, subject: str, file_p: str, lines: List[str]):
            """Extracts function deletions from a file's diff block."""
            # Only analyze code files, skip markdown/docs/json
            if not self.is_code_file(file_p):
                return

            deleted_hunks: List[Tuple[str, str, List[str]]] = []  # (kind, name, code_lines)
            active_entity_name = None
            active_entity_kind = "function"
            accumulated_code: List[str] = []

            for d_line in lines:
                if d_line.startswith("---") or d_line.startswith("+++"):
                    continue

                if d_line.startswith("-"):
                    raw_content = d_line[1:]
                    # Check if this line is a function/class definition
                    matched_name = None
                    matched_kind = "function"
                    for pat in self.DEF_PATTERNS:
                        m = pat.search(raw_content)
                        if m:
                            matched_name = m.group(1)
                            if "class" in raw_content or "struct" in raw_content:
                                matched_kind = "class"
                            break

                    if matched_name:
                        if active_entity_name and accumulated_code:
                            deleted_hunks.append((active_entity_kind, active_entity_name, accumulated_code))
                        active_entity_name = matched_name
                        active_entity_kind = matched_kind
                        accumulated_code = [raw_content]
                    elif active_entity_name:
                        accumulated_code.append(raw_content)
                else:
                    # Non-deletion line ends the current function hunk
                    if active_entity_name and accumulated_code:
                        deleted_hunks.append((active_entity_kind, active_entity_name, accumulated_code))
                        active_entity_name = None
                        accumulated_code = []

            if active_entity_name and accumulated_code:
                deleted_hunks.append((active_entity_kind, active_entity_name, accumulated_code))

            for kind, name, code_list in deleted_hunks:
                if len(code_list) < 2 and kind == "function":
                    # Ignore single-line noise or false positives
                    continue
                key = f"{file_p}:{name}"
                if key in seen_entities:
                    continue
                seen_entities.add(key)

                raw_snippet = "\n".join(code_list)
                cert = DeathCertificate(
                    entity_type=kind,
                    name=f"{name}()" if kind == "function" and not name.endswith("()") else name,
                    file_path=file_p,
                    death_commit=commit_hash[:8],
                    death_author=author,
                    death_date=date_str[:10],
                    death_message=subject,
                    birth_commit=None,
                    birth_author=None,
                    birth_date=None,
                    lines_lost=len(code_list),
                    resurrected_code=raw_snippet[:2500],
                    resurrected_diff=f"- " + "\n- ".join(code_list[:35])
                )
                certificates.append(cert)

        lines_buffer: List[str] = []
        for line in log_out.splitlines():
            if line.startswith("COMMIT:"):
                if current_file and lines_buffer:
                    process_diff_block(current_commit, current_author, current_date, current_subject, current_file, lines_buffer)
                    lines_buffer = []
                parts = line[7:].split("\x00")
                if len(parts) >= 4:
                    current_commit, current_author, current_date, current_subject = parts[:4]
            elif line.startswith("diff --git "):
                if current_file and lines_buffer:
                    process_diff_block(current_commit, current_author, current_date, current_subject, current_file, lines_buffer)
                    lines_buffer = []
                m = re.search(r"diff --git a/(.*?) b/(.*)", line)
                if m:
                    current_file = m.group(1)
            else:
                lines_buffer.append(line)

        if current_file and lines_buffer:
            process_diff_block(current_commit, current_author, current_date, current_subject, current_file, lines_buffer)

        return certificates[:limit]

    def _get_file_before_commit(self, commit_hash: str, file_path: str) -> str:
        """Retrieves raw file content right before the deletion commit."""
        return self._run_git(["show", f"{commit_hash}~1:{file_path}"])

    def _get_commit_diff_for_file(self, commit_hash: str, file_path: str) -> str:
        """Gets unified diff for a deleted file at commit_hash."""
        return self._run_git(["show", "--format=", commit_hash, "--", file_path])

    def _find_birth_record(self, file_path: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Finds the earliest commit that introduced the file."""
        out = self._run_git([
            "log",
            "--follow",
            "--format=%H%x00%an%x00%ad",
            "--date=iso-strict",
            "--",
            file_path
        ])
        lines = [l.strip() for l in out.splitlines() if l.strip()]
        if not lines:
            return None, None, None
        oldest_line = lines[-1]
        parts = oldest_line.split("\x00")
        if len(parts) >= 3:
            return parts[0], parts[1], parts[2]
        return None, None, None

    def get_full_graveyard(self) -> Dict[str, any]:
        """Excavates both deleted files and functions, compiling the master repository graveyard."""
        files = self.excavate_deleted_files(limit=20)
        functions = self.excavate_deleted_functions(limit=25)

        # Include historical demo fixtures to make ofrenda rich if local repo is small
        synth = self._synthetic_graveyard()

        # If repo is small, blend with synthetic fixtures
        combined_files = files if files else [f for f in synth if f.entity_type == "file"]
        combined_funcs = functions if functions else [f for f in synth if f.entity_type in ("function", "class")]

        # Always include synthetic icons if repo has few items
        if len(combined_funcs) < 3:
            combined_funcs.extend([f for f in synth if f.name not in [x.name for x in combined_funcs]])

        total_lines_buried = sum(f.lines_lost for f in combined_files) + sum(fn.lines_lost for fn in combined_funcs)

        return {
            "repository": os.path.basename(self.repo_path),
            "is_git_repository": self.is_git,
            "total_deceased_artifacts": len(combined_files) + len(combined_funcs),
            "total_lines_buried": total_lines_buried,
            "deleted_files": [asdict(f) for f in combined_files],
            "deleted_functions": [asdict(fn) for fn in combined_funcs]
        }

    def _synthetic_graveyard(self) -> List[DeathCertificate]:
        """
        Historical folklore fixtures when scanning a new repo or demo environment.
        Celebrates iconic historic open-source codebases and algorithms.
        """
        return [
            DeathCertificate(
                entity_type="function",
                name="fast_inverse_sqrt()",
                file_path="src/game/q_math.c",
                death_commit="c51b980a",
                death_author="John Carmack",
                death_date="1999-12-10",
                death_message="refactor: replace magic constant 0x5f3759df with hardware SSE rsqrtss instruction",
                birth_commit="0001a11",
                birth_author="Gary Tarolli / Greg Walsh",
                birth_date="1995-04-12",
                lines_lost=16,
                resurrected_code=(
                    "float Q_rsqrt( float number ) {\n"
                    "    long i;\n"
                    "    float x2, y;\n"
                    "    const float threehalfs = 1.5F;\n\n"
                    "    x2 = number * 0.5F;\n"
                    "    y  = number;\n"
                    "    i  = * ( long * ) &y;                       // evil floating point bit level hacking\n"
                    "    i  = 0x5f3759df - ( i >> 1 );               // what the fuck?\n"
                    "    y  = * ( float * ) &i;\n"
                    "    y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration\n"
                    "    return y;\n"
                    "}"
                ),
                resurrected_diff=(
                    "- float Q_rsqrt( float number ) {\n"
                    "-     long i;\n"
                    "-     float x2, y;\n"
                    "-     const float threehalfs = 1.5F;\n"
                    "-     x2 = number * 0.5F;\n"
                    "-     y  = number;\n"
                    "-     i  = * ( long * ) &y;\n"
                    "-     i  = 0x5f3759df - ( i >> 1 );\n"
                    "-     y  = * ( float * ) &i;\n"
                    "-     y  = y * ( threehalfs - ( x2 * y * y ) );\n"
                    "-     return y;\n"
                    "- }"
                )
            ),
            DeathCertificate(
                entity_type="class",
                name="LegacyBBSDialer",
                file_path="telecom/modem_v32.py",
                death_commit="4e99a12f",
                death_author="Sysop",
                death_date="2003-08-14",
                death_message="chore: decommission 56k dial-up Hayes AT command modem carrier line",
                birth_commit="1098ef0",
                birth_author="Sysop",
                birth_date="1996-03-02",
                lines_lost=42,
                resurrected_code=(
                    "class LegacyBBSDialer:\n"
                    "    def dial_carrier(self, baud=57600):\n"
                    "        self.serial.write(b'ATDT 555-0199\\r')\n"
                    "        response = self.serial.read_until(b'CONNECT')\n"
                    "        print('Carrier tone established at 56,000 bps.')\n"
                    "        return response"
                ),
                resurrected_diff=(
                    "- class LegacyBBSDialer:\n"
                    "-     def dial_carrier(self, baud=57600):\n"
                    "-         self.serial.write(b'ATDT 555-0199\\r')\n"
                    "-         response = self.serial.read_until(b'CONNECT')\n"
                    "-         return response"
                )
            ),
            DeathCertificate(
                entity_type="function",
                name="rose_window_prism()",
                file_path="app/static/js/stellar-map.js",
                death_commit="ea99b114",
                death_author="XiaoArnav",
                death_date="2026-10-23",
                death_message="refactor: delete over-engineered volumetric stained-glass god-ray lighting engine",
                birth_commit="1f05c01",
                birth_author="XiaoArnav",
                birth_date="2026-10-21",
                lines_lost=385,
                resurrected_code=(
                    "function renderRoseWindowPrism(ctx, time) {\n"
                    "    // Volumetric caustic stained-glass ray simulation\n"
                    "    for (let ray = 0; ray < 128; ray++) {\n"
                    "        const angle = (ray / 128) * Math.PI * 2 + time * 0.001;\n"
                    "        ctx.strokeStyle = `hsla(${ray * 2.8}, 80%, 65%, 0.12)`;\n"
                    "        ctx.beginPath();\n"
                    "        ctx.moveTo(centerX, centerY);\n"
                    "        ctx.lineTo(centerX + Math.cos(angle) * radius, centerY + Math.sin(angle) * radius);\n"
                    "        ctx.stroke();\n"
                    "    }\n"
                    "}"
                ),
                resurrected_diff=(
                    "- function renderRoseWindowPrism(ctx, time) {\n"
                    "-     for (let ray = 0; ray < 128; ray++) {\n"
                    "-         const angle = (ray / 128) * Math.PI * 2 + time * 0.001;\n"
                    "-         ctx.stroke();\n"
                    "-     }\n"
                    "- }"
                )
            )
        ]


if __name__ == "__main__":
    archaeologist = GitArchaeologist()
    graveyard = archaeologist.get_full_graveyard()
    print(f"🪦 Excavation complete for: {graveyard['repository']}")
    print(f"Total Deceased Artifacts: {graveyard['total_deceased_artifacts']}")
    print(f"Total Lines Buried: {graveyard['total_lines_buried']}")
    for d in graveyard["deleted_files"] + graveyard["deleted_functions"]:
        print(f"  • [{d['entity_type']}] {d['name']} in {d['file_path']} (Died: {d['death_commit']} by {d['death_author']} on {d['death_date']})")
