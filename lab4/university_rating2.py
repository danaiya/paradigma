"""Модуль формирования и сортировки рейтинга студентов."""

from .calculations import (
    calculate_average,
    determine_status,
    determine_letter_grade,
)
from .validation import validate_scores, validate_student


def build_student_result(student):
    """Формирует итоговую структуру данных одного студента."""
    validate_student(student)
    scores = validate_scores(student["scores"])
    average = calculate_average(scores)

    return {
        "id": student["id"],
        "name": student["name"],
        "average": average,
        "status": determine_status(average),
        "letter_grade": determine_letter_grade(average),
    }


def _sort_key(item):
    """Внутренний ключ сортировки: записи без оценок идут в конец."""
    average = item["average"]
    return average is not None, average or 0.0


def build_rating(students):
    """Создаёт отсортированный рейтинг, не изменяя исходные данные."""
    results = [build_student_result(item) for item in students]
    return sorted(results, key=_sort_key, reverse=True)