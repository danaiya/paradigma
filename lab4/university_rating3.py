"""Модуль текстового представления результатов."""


def format_average(value):
    """Форматирует числовое значение среднего балла."""
    return "-" if value is None else f"{value:.2f}"


def format_rating(rows):
    """Формирует итоговую текстовую таблицу рейтинга группы."""
    lines = ["Рейтинг группы"]
    for position, row in enumerate(rows, start=1):
        average = format_average(row["average"])
        lines.append(
            f"{position}. {row['name']}: {average} "
            f"({row['letter_grade']}) - {row['status']}"
        )
    return "\n".join(lines)