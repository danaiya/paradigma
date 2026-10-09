"""Точка входа в приложение."""

from .rating import build_rating
from .report import format_rating


def load_demo_data():
    """Возвращает демонстрационный список студентов."""
    return [
        {"id": 101, "name": "Данайя Р.", "scores": [92, 95, 88]},
        {"id": 102, "name": "Амина", "scores": [88, 92, 79]},
        {"id": 103, "name": "Диас", "scores": [45, 52, 48]},
        {"id": 104, "name": "Мира", "scores": []},
    ]


def main():
    """Основная функция запуска."""
    students = load_demo_data()
    rating = build_rating(students)
    print(format_rating(rating))


if __name__ == "__main__":
    main()