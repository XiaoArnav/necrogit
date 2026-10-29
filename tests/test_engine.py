"""
Unit Tests: app.engine
Zero external dependencies (pure Python unittest).
"""

import unittest
import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.engine import SeanceEngine


class TestSeanceEngine(unittest.TestCase):

    def setUp(self):
        self.engine = SeanceEngine()
        self.dummy_cert = {
            "entity_type": "function",
            "name": "calculate_hash()",
            "file_path": "crypto/sha.py",
            "death_commit": "a1b2c3d4",
            "death_author": "XiaoArnav",
            "death_date": "2026-10-30",
            "death_message": "refactor: simplify cryptographic pipeline",
            "birth_commit": "00112233",
            "birth_author": "XiaoArnav",
            "lines_lost": 28,
            "resurrected_code": "def calculate_hash(data):\n    return sha256(data)"
        }

    def test_check_ollama_offline_resilience(self):
        """Verify check_ollama returns graceful dictionary even when Ollama is offline."""
        status = self.engine.check_ollama(timeout=0.2)
        self.assertIn("online", status)
        self.assertIn("url", status)
        self.assertIn("available_models", status)
        self.assertIn("model_ready", status)
        self.assertIn("active_model", status)
        self.assertIn("mode", status)

    def test_heuristic_seance_generation(self):
        """Verify heuristic necromancer produces rich, in-character spirit eulogy."""
        eulogy = self.engine.heuristic_seance(self.dummy_cert)

        # Check entity attribution
        self.assertIn("calculate_hash()", eulogy)
        self.assertIn("crypto/sha.py", eulogy)
        self.assertIn("a1b2c3d4", eulogy)
        self.assertIn("XiaoArnav", eulogy)

        # Check Día de los Muertos elements
        self.assertIn("CALAVERA LITERARIA", eulogy)
        self.assertIn("cempasúchil", eulogy.lower())

    def test_fact_validator(self):
        """Verify fact validator scores matching and hallucinated outputs properly."""
        valid_eulogy = (
            "I am calculate_hash(). Slain in commit a1b2c3d4 by XiaoArnav. "
            "May my memory live on in the ofrenda."
        )
        result = self.engine.validate_eulogy(valid_eulogy, self.dummy_cert)
        self.assertTrue(result["passed"])
        self.assertEqual(result["score"], 100)
        self.assertTrue(result["verified_commit"])
        self.assertTrue(result["verified_author"])
        self.assertTrue(result["verified_entity"])

        # Check failing case
        hallucinated = "I am random_code in totally_different_repo by Jane Doe."
        bad_result = self.engine.validate_eulogy(hallucinated, self.dummy_cert)
        self.assertFalse(bad_result["passed"])
        self.assertEqual(bad_result["score"], 0)

    def test_stream_seance(self):
        """Verify stream_seance yields tokens without errors."""
        tokens = list(self.engine.stream_seance(self.dummy_cert))
        self.assertGreater(len(tokens), 10)
        reconstructed = "".join(tokens)
        self.assertIn("calculate_hash()", reconstructed)


if __name__ == "__main__":
    unittest.main()
