"""
Comprehensive Automated Test Suite for BMI Calculator (Advanced)
OASIS INFOBYTE Internship - Task 2
"""

import unittest
import os
import tempfile
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless test
import matplotlib.pyplot as plt

from bmi_logic import (
    calculate_bmi,
    get_bmi_category,
    calculate_healthy_weight_range,
    validate_inputs
)
import database as db


class TestBMILogic(unittest.TestCase):
    """Test BMI mathematical calculations and categorization boundaries."""

    def test_bmi_calculation(self):
        # 70 kg, 1.75 m -> 70 / (1.75^2) = 22.857... -> 22.86
        self.assertEqual(calculate_bmi(70, 1.75), 22.86)
        # 50 kg, 1.65 m -> 50 / (1.65^2) = 18.365... -> 18.37
        self.assertEqual(calculate_bmi(50, 1.65), 18.37)
        # 90 kg, 1.80 m -> 90 / (1.80^2) = 27.777... -> 27.78
        self.assertEqual(calculate_bmi(90, 1.80), 27.78)

    def test_zero_or_negative_calculation_raises(self):
        with self.assertRaises(ValueError):
            calculate_bmi(70, 0)
        with self.assertRaises(ValueError):
            calculate_bmi(-5, 1.75)
        with self.assertRaises(ValueError):
            calculate_bmi(70, -1.75)

    def test_bmi_categories_and_colors(self):
        # Underweight (< 18.5)
        cat, color, _ = get_bmi_category(17.4)
        self.assertEqual(cat, "Underweight")
        self.assertEqual(color, "#0284c7")

        # Boundary Normal (18.5)
        cat, color, _ = get_bmi_category(18.5)
        self.assertEqual(cat, "Normal")
        self.assertEqual(color, "#16a34a")

        # Boundary Normal (24.9)
        cat, color, _ = get_bmi_category(24.9)
        self.assertEqual(cat, "Normal")

        # Overweight (25.0 - 29.9)
        cat, color, _ = get_bmi_category(25.0)
        self.assertEqual(cat, "Overweight")
        self.assertEqual(color, "#d97706")

        cat, color, _ = get_bmi_category(29.9)
        self.assertEqual(cat, "Overweight")

        # Obese (>= 30.0)
        cat, color, _ = get_bmi_category(30.0)
        self.assertEqual(cat, "Obese")
        self.assertEqual(color, "#dc2626")

        cat, color, _ = get_bmi_category(38.2)
        self.assertEqual(cat, "Obese")

    def test_healthy_weight_range(self):
        min_w, max_w = calculate_healthy_weight_range(1.75)
        self.assertAlmostEqual(min_w, 56.7, places=1)
        self.assertAlmostEqual(max_w, 76.3, places=1)


class TestBMIValidation(unittest.TestCase):
    """Test user input validation and error reporting."""

    def test_valid_input(self):
        ok, msg, data = validate_inputs("Yojna", "65.5", "1.70")
        self.assertTrue(ok)
        self.assertEqual(msg, "")
        self.assertEqual(data["user_name"], "Yojna")
        self.assertEqual(data["weight"], 65.5)
        self.assertEqual(data["height"], 1.7)

    def test_empty_username(self):
        ok, msg, _ = validate_inputs("   ", "70", "1.75")
        self.assertFalse(ok)
        self.assertIn("User Name cannot be empty", msg)

    def test_empty_weight(self):
        ok, msg, _ = validate_inputs("Alice", "", "1.75")
        self.assertFalse(ok)
        self.assertIn("Weight cannot be empty", msg)

    def test_empty_height(self):
        ok, msg, _ = validate_inputs("Alice", "70", "  ")
        self.assertFalse(ok)
        self.assertIn("Height cannot be empty", msg)

    def test_non_numeric_input(self):
        ok, msg, _ = validate_inputs("Bob", "abc", "1.75")
        self.assertFalse(ok)
        self.assertIn("must be a valid numeric number", msg)

        ok, msg, _ = validate_inputs("Bob", "70", "xyz")
        self.assertFalse(ok)
        self.assertIn("must be a valid numeric number", msg)

    def test_zero_or_negative_inputs(self):
        ok, msg, _ = validate_inputs("Charlie", "0", "1.75")
        self.assertFalse(ok)
        self.assertIn("greater than zero", msg)

        ok, msg, _ = validate_inputs("Charlie", "-50", "1.75")
        self.assertFalse(ok)
        self.assertIn("greater than zero", msg)

        ok, msg, _ = validate_inputs("Charlie", "60", "0")
        self.assertFalse(ok)
        self.assertIn("greater than zero", msg)

    def test_centimeters_detection(self):
        # User entered 175 instead of 1.75 m
        ok, msg, _ = validate_inputs("Dave", "75", "175")
        self.assertFalse(ok)
        self.assertIn("appears to be in centimeters", msg)
        self.assertIn("1.75 m", msg)


class TestBMIDatabase(unittest.TestCase):
    """Test SQLite database operations including multi-user isolation."""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_path = self.temp_db.name
        db.init_db(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_insert_and_get_records(self):
        id1 = db.insert_record("Yojna", 65.0, 1.70, 22.49, "Normal", date_time="2026-09-01 10:00:00", db_path=self.db_path)
        id2 = db.insert_record("User2", 85.0, 1.75, 27.76, "Overweight", date_time="2026-09-02 11:00:00", db_path=self.db_path)
        id3 = db.insert_record("Yojna", 63.5, 1.70, 21.97, "Normal", date_time="2026-09-10 09:30:00", db_path=self.db_path)

        self.assertGreater(id1, 0)
        self.assertGreater(id2, 0)
        self.assertGreater(id3, 0)

        # Multi-user retrieval
        yojna_records = db.get_records("Yojna", db_path=self.db_path)
        self.assertEqual(len(yojna_records), 2)
        self.assertEqual(yojna_records[0]["bmi"], 22.49)
        self.assertEqual(yojna_records[1]["bmi"], 21.97)

        user2_records = db.get_records("User2", db_path=self.db_path)
        self.assertEqual(len(user2_records), 1)
        self.assertEqual(user2_records[0]["category"], "Overweight")

        all_users = db.get_all_users(db_path=self.db_path)
        self.assertEqual(sorted(all_users), ["User2", "Yojna"])

    def test_delete_record(self):
        rid = db.insert_record("TestUser", 70.0, 1.75, 22.86, "Normal", db_path=self.db_path)
        self.assertTrue(db.delete_record(rid, db_path=self.db_path))
        records = db.get_records("TestUser", db_path=self.db_path)
        self.assertEqual(len(records), 0)

    def test_clear_user_history(self):
        db.insert_record("TempUser", 70.0, 1.75, 22.86, "Normal", db_path=self.db_path)
        db.insert_record("TempUser", 71.0, 1.75, 23.18, "Normal", db_path=self.db_path)
        deleted_count = db.clear_user_history("TempUser", db_path=self.db_path)
        self.assertEqual(deleted_count, 2)
        self.assertEqual(len(db.get_records("TempUser", db_path=self.db_path)), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
