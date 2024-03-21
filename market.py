import sqlite3


def get_products_on_racks(orders):

    print("Страница сборки заказов", end=" ")
    print(*orders, sep=",", end="\n\n")

    # Подключение к базе данных SQLite
    connect = sqlite3.connect("market_db.db")
    cursor = connect.cursor()

    placeholders = ",".join("?" * len(orders))

    # Запрос для получения названий стеллажей и информации о товарах на стеллажах в указанном заказе
    query = f"""
            SELECT Racks.rack_name, Products.name, Products.p_id, Order_Items.order_id, Order_Items.quantity 
            FROM Orders
            JOIN Order_Items ON Orders.o_id = Order_Items.order_id
            JOIN Products ON Order_Items.order_product_id = Products.p_id
            JOIN Product_Racks ON Products.p_id = Product_Racks.product_id
            JOIN Racks ON Product_Racks.rack_id = Racks.r_id
            WHERE Orders.o_id IN ({placeholders}) AND Product_Racks.main_rack = 1            
            ORDER BY Racks.rack_name               
            """

    cursor.execute(query, orders)

    # создаётся кортеж в котором хранятся значения имени стелажа, названия продукта, его id, а также количества товара в заказе    
    results = cursor.fetchall() 

    rack_repeat = None

    # создаётся цикл для того чтобы перебрать значения кортежа и вывести их в удобной для чтения форме     
    for rack in results:
        rack_name, product_name, product_id, order_count, order_quality = rack
        if rack_repeat != rack_name:
            print(f"===Стеллаж {rack_name}")
            rack_repeat = rack_name
        print(f"{product_name} (id={product_id})")
        print(f"заказ {order_count}, {order_quality} шт")

        # создаётся запрос для получения информации о хранении товаров на других стелажах     
        query = """SELECT Racks.rack_name 
                FROM Product_Racks  
                JOIN Racks ON Product_Racks.rack_id = Racks.r_id 
                WHERE Product_Racks.product_id = ? AND Racks.rack_name != ?
                ORDER BY Product_Racks.product_racks_id"""

        cursor.execute(query, (product_id, rack_name))
        additional_shelves = cursor.fetchall()

        if additional_shelves:
            print(f"доп стеллаж:", end=" ")
            print(",".join([shelves[0] for shelves in additional_shelves]))

        print("")

    # закрываем соединение с базой данных 
    connect.close()


# Получаем номера заказов от пользователя и вызываем функцию для получения информации о товарах на стеллажах
orders_input = input("Введите номера заказов через запятую: ").split(",")

get_products_on_racks(orders_input)
