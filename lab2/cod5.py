# Задание 5: Поиск максимума без использования функции max()
scores = [67, 82, 45, 91, 76, 88, 54]
maximum = scores[0]

for score in scores:
    maximum_before = maximum
    condition = score > maximum
    if condition:
        maximum = score
    print(f"score = {score:2d} | maximum_before = {maximum_before:2d} | score > maximum: {str(condition):5s} | maximum_after = {maximum:2d}")

print(f"\nМаксимальный балл: {maximum}")