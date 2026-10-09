"""
Лабораторная работа № 2. Индивидуальное задание № 1: Банковский счет.
Автор: Данайя Р., Группа: ТИИ25-21.
"""

def process_bank_account():
    # 1. Начальное состояние баланса
    balance = 150000.0  # Начальный баланс в тенге
    
    print("=== БАНКОВСКИЙ ТЕРМИНАЛ ===")
    print(f"Текущий баланс счёта: {balance:.2f} тг.")
    
    # Запрос ввода суммы операции
    try:
        withdraw_amount = float(input("\nВведите сумму для снятия (тг): "))
    except ValueError:
        print("Ошибка: введено нечисловое значение!")
        return

    # 2. Проверка условий и управление выполнением
    if withdraw_amount <= 0:
        print("Ошибка: сумма снятия должна быть больше 0!")
    elif withdraw_amount > balance:
        print("\nОТКАЗ В ОПЕРАЦИИ!")
        print(f"Недостаточно средств на счёте. Запрошено: {withdraw_amount:.2f} тг, Доступно: {balance:.2f} тг.")
        print(f"Состояние баланса не изменено: {balance:.2f} тг.")
    else:
        # 3. Изменение состояния баланса
        balance_before = balance
        balance = balance - withdraw_amount  # Явное изменение состояния
        
        print("\nОПЕРАЦИЯ УСПЕШНО ВЫПОЛНЕНА!")
        print(f"Снятая сумма: {withdraw_amount:.2f} тг.")
        print(f"Баланс до операции: {balance_before:.2f} тг.")
        print(f"Новый баланс счёта: {balance:.2f} тг.")

if __name__ == "__main__":
    process_bank_account()