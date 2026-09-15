"""
Comprehensive Automated Test Suite for Secure Password Generator (Advanced)
OASIS INFOBYTE Internship - Task 3
"""

import unittest
import string
from password_generator import (
    generate_secure_password,
    evaluate_password_strength,
    calculate_entropy,
    CHAR_SETS,
    AMBIGUOUS_CHARACTERS
)


class TestPasswordGenerator(unittest.TestCase):
    """Test cryptographic generation logic, constraints, and validation."""

    def test_minimum_length_enforcement(self):
        with self.assertRaises(ValueError) as ctx:
            generate_secure_password(length=7, use_upper=True, use_lower=True, use_digits=True, use_symbols=False)
        self.assertIn("at least 8 characters", str(ctx.exception))

    def test_maximum_length_enforcement(self):
        with self.assertRaises(ValueError) as ctx:
            generate_secure_password(length=129, use_upper=True, use_lower=True, use_digits=True, use_symbols=False)
        self.assertIn("cannot exceed 128", str(ctx.exception))

    def test_fewer_than_two_character_types_rejected(self):
        # Only 1 type selected
        with self.assertRaises(ValueError) as ctx:
            generate_secure_password(length=12, use_upper=True, use_lower=False, use_digits=False, use_symbols=False)
        self.assertIn("At least TWO character types", str(ctx.exception))

        # 0 types selected
        with self.assertRaises(ValueError) as ctx:
            generate_secure_password(length=12, use_upper=False, use_lower=False, use_digits=False, use_symbols=False)
        self.assertIn("At least TWO character types", str(ctx.exception))

    def test_two_types_valid(self):
        pwd = generate_secure_password(length=10, use_upper=True, use_lower=True, use_digits=False, use_symbols=False)
        self.assertEqual(len(pwd), 10)
        self.assertTrue(any(c.isupper() for c in pwd))
        self.assertTrue(any(c.islower() for c in pwd))
        self.assertFalse(any(c.isdigit() for c in pwd))

    def test_guaranteed_inclusion_of_all_selected_types(self):
        # Run multiple times to verify guarantee holds across iterations
        for _ in range(25):
            pwd = generate_secure_password(
                length=16,
                use_upper=True,
                use_lower=True,
                use_digits=True,
                use_symbols=True
            )
            self.assertEqual(len(pwd), 16)
            self.assertTrue(any(c.isupper() for c in pwd), "Missing guaranteed uppercase character")
            self.assertTrue(any(c.islower() for c in pwd), "Missing guaranteed lowercase character")
            self.assertTrue(any(c.isdigit() for c in pwd), "Missing guaranteed digit")
            self.assertTrue(any(c in CHAR_SETS["symbols"] for c in pwd), "Missing guaranteed symbol")

    def test_exclude_ambiguous_characters(self):
        for _ in range(30):
            pwd = generate_secure_password(
                length=20,
                use_upper=True,
                use_lower=True,
                use_digits=True,
                use_symbols=True,
                exclude_ambiguous=True
            )
            for char in pwd:
                self.assertNotIn(
                    char,
                    AMBIGUOUS_CHARACTERS,
                    f"Ambiguous character '{char}' was found in password '{pwd}' despite exclusion!"
                )

    def test_strength_evaluation(self):
        # Weak password (short 8 chars, 2 types: lower + digits -> score 35)
        level, score, color, advice, _ = evaluate_password_strength("ab123456", pool_size=36)
        self.assertEqual(level, "Weak")
        self.assertLess(score, 40)
        self.assertEqual(color, "#ef4444")

        # Medium password (12 chars, 3 types -> score 55)
        level, score, color, advice, _ = evaluate_password_strength("MySecret1234", pool_size=62)
        self.assertEqual(level, "Medium")
        self.assertTrue(40 <= score < 70)

        # Strong password (14 chars, 4 types -> score 80)
        level, score, color, advice, _ = evaluate_password_strength("MySecret1234!@", pool_size=90)
        self.assertEqual(level, "Strong")
        self.assertTrue(70 <= score < 88)

        # Very Strong password (20 chars, all 4 types -> score 95)
        level, score, color, advice, entropy = evaluate_password_strength("K9#vX!8$mQ@4pL%2wZ*7", pool_size=90)
        self.assertEqual(level, "Very Strong")
        self.assertGreaterEqual(score, 88)
        self.assertEqual(color, "#16a34a")
        self.assertGreater(entropy, 100.0)

    def test_entropy_calculation(self):
        entropy = calculate_entropy("12345678", 10)  # digits pool (10)
        # 8 * log2(10) ≈ 8 * 3.3219 ≈ 26.6 bits
        self.assertAlmostEqual(entropy, 26.6, places=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
