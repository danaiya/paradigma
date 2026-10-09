"""
Лабораторная работа № 3. Вариант № 1: Посещаемость.
Автор: Данайя Р., Группа: ТИИ25-21.
"""

import unittest
from typing import List, Dict, Any, Optional

VALID_MARKS = {"present", "absent", "excused"}


def validate_mark(mark: str) -> str:
    """Проверяет корректность одной отметки посещаемости."""
    if not isinstance(mark, str):
        raise TypeError("Отметка посещаемости должна быть строкой")
    clean_mark = mark.strip().lower()
    if clean_mark not in VALID_MARKS:
        raise ValueError(f"Недопустимая отметка: '{mark}'. Допустимы: present, absent, excused")
    return clean_mark


def attendance_rate(marks: List[str]) -> Optional[float]:
    """
    Рассчитывает процент посещаемости.
    Уважительные пропуски ('excused') не уменьшают процент посещаемости.
    """
    if not isinstance(marks, (list, tuple)):
        raise TypeError("Список отметок должен быть списком или кортежем")

    validated = [validate_mark(m) for m in marks]
    evaluable = [m for m in validated if m != "excused"]

    if not evaluable:
        return None

    presents = sum(1 for m in evaluable if m == "present")
    return round((presents / len(evaluable)) * 100, 2)


def determine_access(rate: Optional[float], threshold: float = 70.0) -> str:
    """Определяет статус допуска к сессии по проценту посещаемости."""
    if not (0 <= threshold <= 100):
        raise ValueError("Порог допуска должен быть от 0 до 100")
    if rate is None:
        return "нет данных"
    return "допущен" if rate >= threshold else "не допущен"


def summarize_student(student: Dict[str, Any], threshold: float = 70.0) -> Dict[str, Any]:
    """Формирует новую сводную запись для одного студента."""
    if not isinstance(student, dict):
        raise TypeError("Данные студента должны быть словарём")

    student_id = student.get("id")
    name = student.get("name")
    marks = student.get("marks", [])

    if isinstance(student_id, bool) or not isinstance(student_id, int) or student_id <= 0:
        raise ValueError("Идентификатор студента должен быть положительным целым числом")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Имя студента не должно быть пустым")

    rate = attendance_rate(marks)
    return {
        "id": student_id,
        "name": name.strip(),
        "rate": rate,
        "status": determine_access(rate, threshold),
    }


def build_rating(students: List[Dict[str, Any]], threshold: float = 70.0) -> List[Dict[str, Any]]:
    """Создаёт отсортированный рейтинг посещаемости, не меняя исходные данные."""
    summaries = [summarize_student(s, threshold) for s in students]
    return sorted(
        summaries,
        key=lambda item: (item["rate"] is not None, item["rate"] or 0.0),
        reverse=True,
    )


def format_report(rating: List[Dict[str, Any]]) -> str:
    """Форматирует текстовый отчёт о посещаемости группы без печати."""
    lines = ["Отчёт о посещаемости группы:"]
    for pos, item in enumerate(rating, start=1):
        rate_str = "-" if item["rate"] is None else f"{item['rate']:.1f}%"
        lines.append(f"{pos}. {item['name']}: {rate_str}; {item['status']}")
    return "\n".join(lines)


def main() -> None:
    """Точка входа: координирует вызовы и выполняет вывод."""
    demo_students = [
        {"id": 101, "name": "Данайя Р.", "marks": ["present", "present", "excused", "absent"]},
        {"id": 102, "name": "Амина", "marks": ["present", "present", "present"]},
        {"id": 103, "name": "Диас", "marks": ["absent", "absent", "present"]},
        {"id": 104, "name": "Мира", "marks": []},
    ]
    rating = build_rating(demo_students, threshold=70.0)
    print(format_report(rating))


# =====================================================================
# Набор автоматических тестов (unittest)
# =====================================================================

class TestAttendanceFunctions(unittest.TestCase):
    """Тестирование процедурной логики, нормальных, граничных и ошибочных случаев."""

    def test_attendance_rate_with_excused(self) -> None:
        """Проверка учёта уважительных пропусков."""
        # 2 присутствия, 1 пропуск, 1 уважительный -> 2 из 3 = 66.67%
        rate = attendance_rate(["present", "present", "excused", "absent"])
        self.assertEqual(rate, 66.67)

    def test_empty_marks_returns_none(self) -> None:
        """Проверка пустых отметок."""
        self.assertIsNone(attendance_rate([]))

    def test_determine_access_boundary(self) -> None:
        """Граничные значения порога допуска (70%)."""
        self.assertEqual(determine_access(69.99, threshold=70.0), "не допущен")
        self.assertEqual(determine_access(70.0, threshold=70.0), "допущен")
        self.assertEqual(determine_access(None), "нет данных")

    def test_invalid_mark_raises_value_error(self) -> None:
        """Ошибочный сценарий: недопустимая отметка."""
        with self.assertRaises(ValueError):
            validate_mark("illness")

    def test_invalid_student_id_raises_value_error(self) -> None:
        """Ошибочный сценарий: неверный ID студента."""
        with self.assertRaises(ValueError):
            summarize_student({"id": -10, "name": "Алекс", "marks": []})

    def test_input_data_is_not_mutated(self) -> None:
        """Проверка сохранения неизменяемости исходного списка."""
        original = [{"id": 1, "name": "Тест", "marks": ["present"]}]
        before = [{"id": 1, "name": "Тест", "marks": ["present"]}]
        build_rating(original)
        self.assertEqual(original, before)


if __name__ == "__main__":
    main()