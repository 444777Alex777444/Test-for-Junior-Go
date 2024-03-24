import SQL_requests

def get_products_on_racks(orders):

    print("Страница сборки заказов", end=" ")
    print(*orders, sep=",", end="\n\n")
            
    placeholders = SQL_requests.placeholders(orders)
    
    # Запрос для получения id продукта, номера заказа и его количества в заказе  
    result_order_id_and_product_id = SQL_requests.result_order_id_and_product_id(orders, placeholders) 
   
   # Запрос для получения id продукта чтобы впоследствии получить связь id продукта с его именем а также связь id продукта со стелажом
    result_product_id = SQL_requests.result_product_id(orders, placeholders)    
   
    result_tuple_product_id = SQL_requests.result_tuple_product_id(result_product_id)
    
    placeholders_product_id = SQL_requests.placeholders_product_id(result_tuple_product_id) 

    # Запрос для получения id продукта и его имени по этому id
    result_product_name_id = SQL_requests.result_product_name_id(result_tuple_product_id, placeholders_product_id)
   
    # Запрос для получения id продукта и его связи со стелажём, а также просмотр является ли этот стелаж главным или нет
    result_product_id_rack_id_main_rack = SQL_requests.result_product_id_rack_id_main_rack(result_tuple_product_id, placeholders_product_id)
    
    # Запрос для получения id стелажа и связанного с id продукта
    result_rack_id = SQL_requests.result_rack_id(result_tuple_product_id, placeholders_product_id)    

    result_tuple_rack_id = SQL_requests.result_tuple_rack_id(result_rack_id)
    
    placeholders_racks_id = SQL_requests.placeholders_racks_id(result_tuple_rack_id)
    
    # Запрос для получения имени стелажа по его id
    result_rack_id_name_rack = SQL_requests.result_rack_id_name_rack(result_tuple_rack_id, placeholders_racks_id)
   
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

    

    