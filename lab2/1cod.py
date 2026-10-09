# Задание 2: Расчет стоимости покупки
price = int(input("Цена товара: "))
quantity = int(input("Количество: "))
discount_percent = int(input("Скидка: "))

# Изменение состояния: вычисление стоимости без скидки, размера скидки и итоговой суммы
total_no_discount = price * quantity
discount_amount = total_no_discount * (discount_percent / 100)
final_price = total_no_discount - discount_amount

print(f"Стоимость без скидки: {int(total_no_discount)}")
print(f"Размер скидки: {int(discount_amount)}")
print(f"К оплате: {int(final_price)}")