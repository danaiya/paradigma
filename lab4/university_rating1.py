"""Модуль математических и логических расчётов успеваемости."""

PASSING_AVERAGE = 50.0


def calculate_average(scores):
    """Возвращает средний балл или None для пустого списка."""
    return sum(scores) / len(scores) if scores else None


def determine_status(average):
    """Определяет статус допуска к сессии по среднему баллу."""
    if average is None:
        return "нет данных"
    return "допущен" if average >= PASSING_AVERAGE else "не допущен"


def determine_letter_grade(average):
    """
    Индивидуальное расширение (Вариант 1):
    Определяет буквенную оценку по 5-балльной международной шкале.
    """
    if average is None:
        return "-"
    if average >= 90.0:
        return "A"
    if average >= 80.0:
        return "B"
    if average >= 70.0:
        return "C"
    if average >= 50.0:
        return "D"
    return "F"