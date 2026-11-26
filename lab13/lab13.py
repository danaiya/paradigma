from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from random import Random
from statistics import median
from time import perf_counter, sleep


def summarize(block: list[int]) -> tuple[int, int, int]:
    """Подсчитывает количество оценок, их сумму и число оценок >= 60."""
    count = total = passed = 0
    for grade in block:
        count += 1
        total += grade
        passed += grade >= 60
    return count, total, passed


def load_and_summarize(block: list[int]) -> tuple[int, int, int]:
    """Имитирует задержку ввода-вывода и считает статистику по блоку."""
    sleep(0.1)
    return summarize(block)


def combine(parts: list[tuple[int, int, int]]) -> tuple[int, int, int, float]:
    """Объединяет частичную статистику блоков в итоговый результат."""
    count = sum(part[0] for part in parts)
    total = sum(part[1] for part in parts)
    passed = sum(part[2] for part in parts)
    average = total / count if count else 0.0
    return count, total, passed, average


def run(
    blocks: list[list[int]],
    function,
    pool=None,
    max_workers: int = 2,
) -> tuple[int, int, int, float]:
    """Выполняет обработку блоков последовательно или в указанном пуле."""
    if pool is None:
        parts = list(map(function, blocks))
    else:
        with pool(max_workers=max_workers) as executor:
            parts = list(executor.map(function, blocks))
    return combine(parts)


def measure(
    blocks: list[list[int]],
    function,
    pool=None,
    max_workers: int = 2,
    repeats: int = 3,
) -> tuple[tuple[int, int, int, float], float, list[float]]:
    """Запускает измерение несколько раз и возвращает результат, медиану и замеры."""
    durations: list[float] = []
    result = (0, 0, 0, 0.0)
    for _ in range(repeats):
        started = perf_counter()
        result = run(blocks, function, pool, max_workers=max_workers)
        durations.append(perf_counter() - started)
    return result, median(durations), durations


def make_blocks(seed: int, total_items: int, block_size: int) -> list[list[int]]:
    """Генерирует воспроизводимый список оценок и делит на блоки."""
    rng = Random(seed)
    grades = [rng.randrange(101) for _ in range(total_items)]
    return [grades[i : i + block_size] for i in range(0, len(grades), block_size)]


def main() -> None:
    for workers in (1, 2, 4):
        print(f"\n=== Число работников: {workers} ===")
        for label, total_items, block_size in [
            ("Малый объём (20 000)", 20_000, 5_000),
            ("Базовый объём (200 000)", 200_000, 25_000),
            ("Увеличенный объём (600 000)", 600_000, 75_000),
        ]:
            blocks = make_blocks(seed=13, total_items=total_items, block_size=block_size)
            expected = run(blocks, summarize)
            cases = [
                ("CPU последовательно", summarize, None),
                ("CPU процессы", summarize, ProcessPoolExecutor),
                ("I/O последовательно", load_and_summarize, None),
                ("I/O потоки", load_and_summarize, ThreadPoolExecutor),
            ]
            print(f"--- {label} ---")
            for title, function, pool in cases:
                result, med_sec, times = measure(
                    blocks, function, pool, max_workers=workers, repeats=3
                )
                assert result == expected
                formatted_times = ", ".join(f"{t:.4f}" for t in times)
                print(
                    f"{title:22s} | {result} | медиана: {med_sec:.4f} c | "
                    f"замеры: [{formatted_times}]"
                )


if __name__ == "__main__":
    main()