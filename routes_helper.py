from crud import Crud
from flask import jsonify


class RoutesHelper:
    @staticmethod
    def get_all_elements(table_name):
        handler = Crud(table_name)
        cols = handler.get_columns()
        elements_list = handler.get_all_elements()
        elements = []
        for element in elements_list:
            elements.append({cols[x]: element[x] for x in range(len(cols))})    
        return jsonify(data = elements)
    
    @staticmethod
    def insert_element(table_name, json_items):
        handler = Crud(table_name)
        cols = []
        values = []
        
        for col, value in json_items:
            if col == 'id' or col == 'updated_at':
                pass
            else:
                cols.append(col)
                values.append(value)
        print(cols)
        print(values)
        handler.insert(cols, values)
        return cols, values

    @staticmethod
    def update_element(table_name, json_items, id_value):
        handler = Crud(table_name)
        cols = []
        values = []

        for col, value in json_items:
            if col == 'updated_at' or col == 'id':
                pass
            else:
                cols.append(col)
                values.append(value)
    
        handler.update_element(id_value, cols, values, 'id')
