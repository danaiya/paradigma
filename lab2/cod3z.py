# Задание 3: Проверка баллов и перевод в буквенную оценку
score_input = int(input("Введите балл от 0 до 100: "))

if 90 <= score_input <= 100:
    grade = "A"
elif 75 <= score_input <= 89:
    grade = "B"
elif 50 <= score_input <= 74:
    grade = "C"
elif 0 <= score_input <= 49:
    grade = "F"
else:
    grade = None

if grade:
    print(f"Оценка: {grade}")
else:
    print("Ошибка: балл находится вне допустимого диапазона (0-100)!")