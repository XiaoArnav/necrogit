"""
Unit Tests: app.git_archaeology
Zero external dependencies (pure Python unittest).
"""

import unittest
import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.git_archaeology import GitArchaeologist, DeathCertificate


class TestGitArchaeology(unittest.TestCase):

    def setUp(self):
        self.archaeologist = GitArchaeologist()

    def test_repo_detection(self):
        """Verify git repository detection succeeds on current repo."""
        self.assertTrue(self.archaeologist.is_git)
        self.assertTrue(os.path.isdir(self.archaeologist.repo_path))

    def test_is_code_file_whitelist(self):
        """Verify code extensions are accepted and non-code rejected."""
        valid_code_files = [
            "src/index.js", "app/main.py", "pkg/api.go",
            "kernel/sys.c", "engine/math.rs", "types/user.ts"
        ]
        non_code_files = [
            "README.md", "data.json", "image.png",
            "style.css", "config.yaml", "LICENSE"
        ]

        for path in valid_code_files:
            self.assertTrue(self.archaeologist.is_code_file(path), f"Failed for {path}")

        for path in non_code_files:
            self.assertFalse(self.archaeologist.is_code_file(path), f"Failed for {path}")

    def test_def_patterns_regex(self):
        """Verify function/class regex patterns detect common languages."""
        test_cases = [
            ("def calculate_tax(amount):", "calculate_tax"),
            ("class InvoiceProcessor:", "InvoiceProcessor"),
            ("function verifyToken(req) {", "verifyToken"),
            ("const fetchUserData = async () => {", "fetchUserData"),
            ("func HandleRequest(w http.ResponseWriter) {", "HandleRequest"),
            ("pub fn render_frame() {", "render_frame"),
            ("void init_memory_block() {", "init_memory_block")
        ]

        for snippet, expected_name in test_cases:
            matched = False
            for pat in self.archaeologist.DEF_PATTERNS:
                m = pat.search(snippet)
                if m and m.group(1) == expected_name:
                    matched = True
                    break
            self.assertTrue(matched, f"Pattern failed to match: {snippet}")

    def test_get_full_graveyard(self):
        """Verify get_full_graveyard returns a complete structured dictionary."""
        graveyard = self.archaeologist.get_full_graveyard()
        self.assertIn("repository", graveyard)
        self.assertIn("is_git_repository", graveyard)
        self.assertIn("total_deceased_artifacts", graveyard)
        self.assertIn("total_lines_buried", graveyard)
        self.assertIn("deleted_files", graveyard)
        self.assertIn("deleted_functions", graveyard)

        self.assertGreater(graveyard["total_deceased_artifacts"], 0)
        self.assertGreater(graveyard["total_lines_buried"], 0)

        # Verify attributes on excavated items
        for item in graveyard["deleted_files"] + graveyard["deleted_functions"]:
            self.assertIn("name", item)
            self.assertIn("file_path", item)
            self.assertIn("death_commit", item)
            self.assertIn("death_author", item)
            self.assertIn("lines_lost", item)


if __name__ == "__main__":
    unittest.main()
