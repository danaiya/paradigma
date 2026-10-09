"""
Лабораторная работа № 5. Вариант № 1: Учёт посещаемости.
Автор: Данайя Р., Группа: ТИИ25-21.
"""

import unittest
from typing import Tuple, Dict, Any


class StudentAttendance:
    """Класс для индивидуального учёта посещаемости студента."""

    def __init__(self, student_id: int, name: str) -> None:
        if isinstance(student_id, bool) or not isinstance(student_id, int):
            raise TypeError("Идентификатор студента должен быть целым числом")
        if student_id <= 0:
            raise ValueError("Идентификатор студента должен быть положительным")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя студента не должно быть пустым")

        self.student_id = student_id
        self.name = name.strip()
        self._records = []  # Список записей: {'date': str, 'status': str}

    def _add_record(self, date: str, status: str) -> None:
        """Внутренний метод проверки и добавления записи посещаемости."""
        if not isinstance(date, str) or not date.strip():
            raise ValueError("Дата не должна быть пустой")
        clean_date = date.strip()
        if any(rec['date'] == clean_date for rec in self._records):
            raise ValueError(f"Запись за дату {clean_date} уже существует")
        self._records.append({'date': clean_date, 'status': status})

    def mark_present(self, date: str) -> None:
        """Фиксирует присутствие студента."""
        self._add_record(date, "present")

    def mark_absent(self, date: str) -> None:
        """Фиксирует неуважительный пропуск студента."""
        self._add_record(date, "absent")

    def mark_excused(self, date: str) -> None:
        """Фиксирует уважительный пропуск студента."""
        self._add_record(date, "excused")

    @property
    def records(self) -> Tuple[Dict[str, str], ...]:
        """Возвращает неизменяемый снимок записей посещаемости."""
        return tuple(self._records)

    @property
    def attendance_rate(self) -> float:
        """
        Рассчитывает процент посещаемости.
        Уважительные пропуски ('excused') не уменьшают процент посещаемости.
        """
        evaluable_records = [rec for rec in self._records if rec['status'] != 'excused']
        if not evaluable_records:
            return 100.0
        presents = sum(1 for rec in evaluable_records if rec['status'] == 'present')
        return round((presents / len(evaluable_records)) * 100, 2)

    @property
    def status(self) -> str:
        """Определяет статус допуска (порог 70%)."""
        return "допущен" if self.attendance_rate >= 70.0 else "не допущен"

    def __repr__(self) -> str:
        return f"StudentAttendance(student_id={self.student_id!r}, name={self.name!r})"


class AttendanceJournal:
    """Журнал учёта посещаемости академической группы."""

    def __init__(self) -> None:
        self._students = {}

    def register(self, student: StudentAttendance) -> None:
        """Регистрирует нового студента в журнале."""
        if not isinstance(student, StudentAttendance):
            raise TypeError("Ожидается объект типа StudentAttendance")
        if student.student_id in self._students:
            raise ValueError(f"Студент с ID {student.student_id} уже зарегистрирован")
        self._students[student.student_id] = student

    def _get_student(self, student_id: int) -> StudentAttendance:
        """Возвращает студента по ID или вызывает KeyError."""
        if student_id not in self._students:
            raise KeyError(f"Студент с ID {student_id} не найден")
        return self._students[student_id]

    def mark_present(self, student_id: int, date: str) -> None:
        """Делегирует операцию фиксации присутствия."""
        self._get_student(student_id).mark_present(date)

    def mark_absent(self, student_id: int, date: str) -> None:
        """Делегирует операцию фиксации неуважительного пропуска."""
        self._get_student(student_id).mark_absent(date)

    def mark_excused(self, student_id: int, date: str) -> None:
        """Делегирует операцию фиксации уважительного пропуска."""
        self._get_student(student_id).mark_excused(date)

    def get_student(self, student_id: int) -> StudentAttendance:
        """Возвращает объект студента из реестра."""
        return self._get_student(student_id)


# =====================================================================
# Набор автоматических тестов (unittest)
# =====================================================================

class TestAttendanceSystem(unittest.TestCase):
    """Тестирование корректности работы классов и сохранения инвариантов."""

    def setUp(self) -> None:
        self.journal = AttendanceJournal()
        self.student = StudentAttendance(101, "Данайя Р.")
        self.journal.register(self.student)

    def test_attendance_rate_with_excused_absence(self) -> None:
        """Проверка расчета процента с уважительным пропуском."""
        self.journal.mark_present(101, "2026-10-01")
        self.journal.mark_excused(101, "2026-10-02")
        self.journal.mark_absent(101, "2026-10-03")
        # Из 2 учитываемых дней 1 присутствие -> 50%
        self.assertEqual(self.student.attendance_rate, 50.0)
        self.assertEqual(self.student.status, "не допущен")

    def test_border_threshold_status(self) -> None:
        """Проверка граничного значения порога допуска (70%)."""
        self.student.mark_present("2026-10-01")
        self.student.mark_present("2026-10-02")
        self.student.mark_present("2026-10-03")
        self.student.mark_present("2026-10-04")
        self.student.mark_absent("2026-10-05")
        # 4 присутствия из 5 дней -> 80%
        self.assertEqual(self.student.attendance_rate, 80.0)
        self.assertEqual(self.student.status, "допущен")

    def test_duplicate_date_raises_value_error(self) -> None:
        """Ошибочный сценарий: дублирование даты посещения."""
        self.student.mark_present("2026-10-01")
        with self.assertRaises(ValueError):
            self.student.mark_absent("2026-10-01")

    def test_invalid_student_id_raises_value_error(self) -> None:
        """Ошибочный сценарий: некорректный ID студента."""
        with self.assertRaises(ValueError):
            StudentAttendance(-5, "Алиса")

    def test_duplicate_student_registration_raises_error(self) -> None:
        """Ошибочный сценарий: повторная регистрация одного ID в журнале."""
        with self.assertRaises(ValueError):
            self.journal.register(StudentAttendance(101, "Копия"))


if __name__ == "__main__":
    unittest.main()