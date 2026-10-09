"""
Лабораторная работа № 6. Вариант 1: Экспорт оценок.
Демонстрация использования Protocol, композиции и полиморфизма.
"""

from typing import Protocol, List, Dict, Any
import json
import unittest


class Exporter(Protocol):
    """Контракт (интерфейс) для экспорта данных журнала оценок."""
    
    def export(self, data: List[Dict[str, Any]]) -> str:
        """Принимает список данных студентов и возвращает отформатированную строку."""
        ...


class TextExporter:
    """Форматирует данные студентов в виде простыня текста."""

    def export(self, data: List[Dict[str, Any]]) -> str:
        lines = [
            f"Студент: {item['name']}, Средний балл: {item['average']:.2f}, Статус: {item['status']}"
            for item in data
        ]
        return "\n".join(lines)


class CsvExporter:
    """Форматирует данные студентов в формат CSV."""

    def export(self, data: List[Dict[str, Any]]) -> str:
        lines = ["name,average,status"]
        for item in data:
            lines.append(f"{item['name']},{item['average']:.2f},{item['status']}")
        return "\n".join(lines)


class MemoryExporter:
    """Тестовый дублёр, сохраняющий данные в память для автоматических проверок."""

    def __init__(self) -> None:
        self.exported_data: List[Dict[str, Any]] = []

    def export(self, data: List[Dict[str, Any]]) -> str:
        self.exported_data = list(data)
        return f"Сохранено записей в память: {len(data)}"


class JsonExporter:
    """Форматирует данные студентов в формат JSON."""

    def export(self, data: List[Dict[str, Any]]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)


class GradeBook:
    """Прикладной класс журнала оценок, использующий Exporter через композицию."""

    def __init__(self, exporter: Exporter) -> None:
        self._exporter = exporter
        self._students: List[Dict[str, Any]] = []

    def add_student(self, name: str, average: float) -> None:
        """Добавляет студента и рассчитывает его статус допуска."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя студента не может быть пустым")
        if isinstance(average, bool) or not isinstance(average, (int, float)):
            raise TypeError("Балл должен быть числом")
        if not (0 <= average <= 100):
            raise ValueError("Средний балл должен быть от 0 до 100")

        status = "допущен" if average >= 50 else "не допущен"
        self._students.append({
            "name": name.strip(),
            "average": float(average),
            "status": status
        })

    def export_data(self) -> str:
        """Делегирует экспорт данных подключённому компоненту."""
        return self._exporter.export(self._students)


# =====================================================================
# Автоматические тесты (unittest)
# =====================================================================

class TestGradeBookExport(unittest.TestCase):
    """Набор тестов для проверки взаимозаменяемости и обработки ошибок."""

    def test_text_exporter(self):
        """Проверка работы с TextExporter."""
        gb = GradeBook(TextExporter())
        gb.add_student("Алиса", 85.5)
        result = gb.export_data()
        self.assertIn("Студент: Алиса, Средний балл: 85.50, Статус: допущен", result)

    def test_csv_exporter(self):
        """Проверка работы с CsvExporter."""
        gb = GradeBook(CsvExporter())
        gb.add_student("Борис", 45.0)
        expected = "name,average,status\nБорис,45.00,не допущен"
        self.assertEqual(gb.export_data(), expected)

    def test_memory_exporter_interchangeability(self):
        """Проверка работы с тестовым дублёром MemoryExporter."""
        mem = MemoryExporter()
        gb = GradeBook(mem)
        gb.add_student("Дана", 90.0)
        gb.export_data()
        
        self.assertEqual(len(mem.exported_data), 1)
        self.assertEqual(mem.exported_data[0]["name"], "Дана")

    def test_json_exporter(self):
        """Проверка выполнения повышенной сложности (JsonExporter)."""
        gb = GradeBook(JsonExporter())
        gb.add_student("Ерлан", 70.0)
        result = gb.export_data()
        self.assertIn('"name": "Ерлан"', result)
        self.assertIn('"status": "допущен"', result)

    def test_empty_name_raises_value_error(self):
        """Ошибочный сценарий: пустое имя студента."""
        gb = GradeBook(TextExporter())
        with self.assertRaisesRegex(ValueError, "Имя студента не может быть пустым"):
            gb.add_student("   ", 80.0)

    def test_invalid_average_score_raises_value_error(self):
        """Ошибочный сценарий: выходящий за границы балл."""
        gb = GradeBook(TextExporter())
        with self.assertRaisesRegex(ValueError, "от 0 до 100"):
            gb.add_student("Аскар", 150.0)


if __name__ == "__main__":
    # Демонстрационный запуск
    print("--- Демонстрация работы полиморфных экспортеров ---")
    
    memory_stub = MemoryExporter()
    gb_demo = GradeBook(memory_stub)
    gb_demo.add_student("Амина", 82.0)
    gb_demo.add_student("Мирас", 40.0)

    print("\n1. Результат с MemoryExporter:")
    print(gb_demo.export_data())

    print("\n2. Быстрая замена канала на JsonExporter:")
    gb_demo._exporter = JsonExporter()
    print(gb_demo.export_data())

    print("\n--- Запуск unittest ---")
    unittest.main()