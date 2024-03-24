from function_result_output import get_products_on_racks


# Получаем номера заказов от пользователя и вызываем функцию для получения информации о товарах на стеллажах
orders_input = input("Введите номера заказов через запятую: ").split(",")
get_products_on_racks(orders_input)
    