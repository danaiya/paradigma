"""Модульные тесты для проверки корректности функций и Варианта 1."""

import unittest
from university_rating.calculations import (
    calculate_average,
    determine_status,
    determine_letter_grade,
)
from university_rating.rating import build_rating
from university_rating.validation import validate_scores


class RatingTests(unittest.TestCase):
    """Набор тестов логики и индивидуального расширения."""

    def test_empty_average(self):
        """Проверка пустых оценок."""
        self.assertIsNone(calculate_average([]))

    def test_status_boundary(self):
        """Проверка границы допуска 50 баллов."""
        self.assertEqual(determine_status(49.99), "не допущен")
        self.assertEqual(determine_status(50), "допущен")

    def test_letter_grade_variants(self):
        """Тестирование индивидуального расширения (буквенная оценка)."""
        self.assertEqual(determine_letter_grade(95.0), "A")
        self.assertEqual(determine_letter_grade(85.0), "B")
        self.assertEqual(determine_letter_grade(75.0), "C")
        self.assertEqual(determine_letter_grade(55.0), "D")
        self.assertEqual(determine_letter_grade(40.0), "F")
        self.assertEqual(determine_letter_grade(None), "-")

    def test_invalid_score(self):
        """Проверка вызова исключения при недопустимом балле."""
        with self.assertRaises(ValueError):
            validate_scores([80, 101])

    def test_source_is_not_changed(self):
        """Проверка неизменяемости исходного списка студентов."""
        students = [{"id": 1, "name": "Test", "scores": [70, 80]}]
        before = [{"id": 1, "name": "Test", "scores": [70, 80]}]
        build_rating(students)
        self.assertEqual(students, before)


if __name__ == "__main__":
    unittest.main()