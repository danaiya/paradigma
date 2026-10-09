# Задание 4: Анализ списка с применением счетчиков и накопителей
numbers = [12, 5, 8, 3, 21, 0, 14, -7]

total_sum = 0           # Накопитель общей суммы
pos_sum = 0             # Накопитель суммы положительных чисел
pos_count = 0           # Счетчик положительных чисел
neg_count = 0           # Счетчик отрицательных чисел
zero_count = 0          # Счетчик нулей

print("Итерация | Число | total_sum | pos_sum | pos_count | neg_count | zero_count")
print("-" * 75)

for idx, num in enumerate(numbers, start=1):
    total_sum += num
    if num > 0:
        pos_sum += num
        pos_count += 1
    elif num < 0:
        neg_count += 1
    else:
        zero_count += 1
    print(f"{idx:8d} | {num:5d} | {total_sum:9d} | {pos_sum:7d} | {pos_count:9d} | {neg_count:9d} | {zero_count:10d}")

print("-" * 75)
print(f"Сумма всех чисел: {total_sum}")
print(f"Сумма положительных: {pos_sum}")
print(f"Количество положительных: {pos_count}")
print(f"Количество отрицательных: {neg_count}")
print(f"Количество нулей: {zero_count}")