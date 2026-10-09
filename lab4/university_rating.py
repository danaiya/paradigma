"""Модуль валидации входных данных студентов и оценок."""


def validate_scores(scores):
    """Проверяет корректность списка баллов и возвращает их проверенную копию."""
    if not isinstance(scores, (list, tuple)):
        raise TypeError("scores должен быть списком или кортежем")

    checked = []
    for score in scores:
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError("Балл должен быть числом")
        if not 0 <= score <= 100:
            raise ValueError("Балл должен быть от 0 до 100")
        checked.append(float(score))
    return checked


def validate_student(student):
    """Проверяет наличие всех обязательных полей у объекта студента."""
    if not isinstance(student, dict):
        raise TypeError("Запись студента должна быть словарём")

    required = {"id", "name", "scores"}
    missing = required - student.keys()
    if missing:
        raise ValueError(f"Отсутствуют поля: {sorted(missing)}")