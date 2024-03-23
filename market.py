import sqlite3
import time


def get_products_on_racks(orders):

    print("Страница сборки заказов", end=" ")
    print(*orders, sep=",", end="\n\n")

    # Подключение к базе данных SQLite
    connect = sqlite3.connect("market_db.db")
    cursor = connect.cursor()

    placeholders = ",".join("?" * len(orders))

    # функция принимает в себя кортеж с находящимися внутри него кортежами и возвращает один кортеж с извлечёнными данными из кортежей
    def tuple_sort(tuple_argument):
        result_tuple = tuple()
        for tup in tuple_argument:
            result_tuple += tup
        return tuple(set(result_tuple))

    # Запрос для получения id продукта, номера заказа и его количества в заказе
    query = f"""
            SELECT Order_Items.order_product_id, Order_Items.order_id, Order_Items.quantity
            FROM Order_Items            
            WHERE Order_Items.order_id IN ({placeholders})
            ORDER BY Order_Items.order_product_id                         
            """

    cursor.execute(query, orders)
    result_order_id_and_product_id = (
        cursor.fetchall()
    )  # Получаем кортежи в которых содержится id продуктов, номера заказов и количества продукта в заказе

    # Запрос для получения id продукта чтобы впоследствии получить связь id продукта с его именем а также связь id продукта со стелажом
    query = f"""
            SELECT Order_Items.order_product_id
            FROM Order_Items            
            WHERE Order_Items.order_id IN ({placeholders})
            ORDER BY Order_Items.order_id                         
            """

    cursor.execute(query, orders)

    # создаётся кортеж в котором хранятся значения имени стелажа, названия продукта, его id, а также количества товара в заказе    
    )  # Получаем кортежи в котором содержатся id продуктов чтобы в дальнейшем по ним найти связь id продукта с именем и связь id продукта с id стелажа

    # Запрос для получения id продукта и его имени по этому id
    result_tuple_product_id = tuple_sort(
        result_product_id
    )  # Преобразуем кортеж кортежей в один общий кортеж
    placeholders_product_id = ",".join("?" * len(result_tuple_product_id))
    query = f"""
            SELECT Products.p_id, Products.name 
            FROM Products            
            WHERE Products.p_id IN ({placeholders_product_id})
            ORDER BY Products.p_id                         
            """

    cursor.execute(query, result_tuple_product_id)
    result_product_name_id = (
        cursor.fetchall()
    )  # Получаем кортежи в котором содержатся id продуктов и имена продуктов по этим id

    # Запрос для получения id продукта и его связи со стелажём, а также просмотр является ли этот стелаж главным или нет
    query = f"""
        SELECT Product_Racks.rack_id, Product_Racks.product_id, Product_Racks.main_rack 
        FROM Product_Racks            
        WHERE Product_Racks.product_id IN ({placeholders_product_id})
        ORDER BY Product_Racks.rack_id                          
        """

    cursor.execute(query, result_tuple_product_id)
    result_product_id_rack_id_main_rack = (
        cursor.fetchall()
    )  # Получаем кортежи в котором хранятся id стелажа, id продукта и флаг показывающий является ли данный стелаж главным для товара или нет

    # Запрос для получения id стелажа и связанного с id продукта
    query = f"""
        SELECT Product_Racks.rack_id
        FROM Product_Racks            
        WHERE Product_Racks.product_id IN ({placeholders_product_id})
        ORDER BY Product_Racks.rack_id                          
        """

    cursor.execute(query, result_tuple_product_id)
    result_rack_id = (
        cursor.fetchall()
    )  # Получаем кортежи в которых хранятся id стелажей

    # Запрос для получения имени стелажа по его id
    result_tuple_rack_id = tuple_sort(
        result_rack_id
    )  # Преобразуем кортеж кортежей в один общий кортеж
    placeholders_racks_id = ",".join("?" * len(result_tuple_rack_id))
    query = f"""
            SELECT Racks.r_id, Racks.rack_name
            FROM Racks           
            WHERE Racks.r_id IN ({placeholders_racks_id})
            ORDER BY Racks.rack_name                       
            """

    cursor.execute(query, result_tuple_rack_id)
    result_rack_id_name_rack = (
        cursor.fetchall()
    )  # Получаем кортежи в котором хранятся id стелажа и его имя по этому id

    product_dict = {}
    for product in result_order_id_and_product_id:
        product_id = product[0]
        order_id = product[1]
        quantity = product[2]
        if product_id not in product_dict:
            product_dict[product_id] = []
        product_dict[product_id].append({"order_id": order_id, "quantity": quantity})

    for rack in result_rack_id_name_rack:
        main_product_ids = [
            product[1]
            for product in result_product_id_rack_id_main_rack
            if product[0] == rack[0] and product[2]
        ]
        if main_product_ids:
            print(f"===Стеллаж {rack[1]}")
            print(" ")
            for product_id in main_product_ids:
                if product_id in product_dict:
                    product_info_list = product_dict[product_id]
                    product_name = next(
                        (
                            product_name[1]
                            for product_name in result_product_name_id
                            if product_name[0] == product_id
                        ),
                        None,
                    )
                    if product_name:
                        for product_info in product_info_list:
                            print(f"{product_name} (id={product_id})")
                            print(
                                f"заказ {product_info['order_id']}, {product_info['quantity']} шт"
                            )
                            dop_racks = [
                                dop_rack_name[1]
                                for dop_recks in result_product_id_rack_id_main_rack
                                for dop_rack_name in result_rack_id_name_rack
                                if dop_recks[1] == product_id
                                and dop_recks[2] == False
                                and dop_recks[0] == dop_rack_name[0]
                            ]
                            if dop_racks:
                                print("доп стеллажи:", end=" ")
                                print(*dop_racks, sep=", ")
                            print("")

    connect.close()


# Получаем номера заказов от пользователя и вызываем функцию для получения информации о товарах на стеллажах
orders_input = input("Введите номера заказов через запятую: ").split(",")

get_products_on_racks(orders_input)

start_time = time.time()

# Ваш код

end_time = time.time()

execution_time = end_time - start_time
print("Время выполнения программы:", execution_time, "секунд")