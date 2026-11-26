from concurrent.futures import ThreadPoolExecutor
from threading import Lock


def main() -> None:
    remaining = 5
    lock = Lock()

    def register(student: int) -> tuple[int, bool]:
        nonlocal remaining
        with lock:
            if remaining == 0:
                return student, False
            remaining -= 1
            return student, True

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(register, range(20)))

    accepted = sum(success for _, success in results)
    assert accepted == 5 and remaining == 0
    print("Зарегистрировано:", accepted)
    print("Осталось мест:", remaining)


if __name__ == "__main__":
    main()