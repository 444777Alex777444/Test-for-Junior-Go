import sqlite3


# Подключение к базе данных SQLite
connect = sqlite3.connect("market_db.db")
cursor = connect.cursor()

def placeholders(orders):
    placeholders = ",".join("?" * len(orders))
    return placeholders    

# функция принимает в себя кортеж с находящимися внутри него кортежами и возвращает один кортеж с извлечёнными данными из кортежей
def tuple_sort(tuple_argument):
    result_tuple = tuple()
    for tup in tuple_argument:
        result_tuple += tup
        if result_tuple:
            connect.close            
    return tuple(set(result_tuple))    

def result_order_id_and_product_id(orders, placeholders):
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
    if result_order_id_and_product_id:
            connect.close
    return result_order_id_and_product_id

def result_product_id(orders, placeholders):
# Запрос для получения id продукта чтобы впоследствии получить связь id продукта с его именем а также связь id продукта со стелажом
    query = f"""
            SELECT Order_Items.order_product_id
            FROM Order_Items            
            WHERE Order_Items.order_id IN ({placeholders})
            ORDER BY Order_Items.order_id                         
            """

    cursor.execute(query, orders)
    result_product_id = (
        cursor.fetchall()
    )  # Получаем кортежи в котором содержатся id продуктов чтобы в дальнейшем по ним найти связь id продукта с именем и связь id продукта с id стелажа
    if result_product_id:
            connect.close
    return result_product_id

def result_tuple_product_id(result_product_id):
    
    result_tuple_product_id = tuple_sort(
        result_product_id
    )  
    if result_tuple_product_id:
            connect.close
    return result_tuple_product_id

def placeholders_product_id(result_tuple_product_id):
    placeholders_product_id = ",".join("?" * len(result_tuple_product_id)) # Преобразуем кортеж кортежей в один общий кортеж
    if placeholders_product_id:
            connect.close
    return placeholders_product_id


def result_product_name_id(result_tuple_product_id, placeholders_product_id): # Запрос для получения id продукта и его имени по этому id
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
    if result_product_name_id:
            connect.close
    return result_product_name_id

def result_product_id_rack_id_main_rack(result_tuple_product_id, placeholders_product_id):
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
    if result_product_id_rack_id_main_rack:
            connect.close
    return result_product_id_rack_id_main_rack

def result_rack_id(result_tuple_product_id, placeholders_product_id):
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
    if result_rack_id:
            connect.close
    return result_rack_id


def result_tuple_rack_id(result_rack_id):
    # Запрос для получения имени стелажа по его id
    result_tuple_rack_id = tuple_sort(
        result_rack_id
    )  # Преобразуем кортеж кортежей в один общий кортеж
    if result_tuple_rack_id:
            connect.close
    return(result_tuple_rack_id)

def placeholders_racks_id(result_tuple_rack_id):
    placeholders_racks_id = ",".join("?" * len(result_tuple_rack_id))
    if placeholders_racks_id:
            connect.close
    return placeholders_racks_id


def result_rack_id_name_rack(result_tuple_rack_id,placeholders_racks_id):
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
    if result_rack_id_name_rack:
            connect.close            
    return result_rack_id_name_rack


