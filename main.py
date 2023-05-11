from flask import Flask, request, json, jsonify, make_response
from crud import Crud
from routes_helper import RoutesHelper
import os

app = Flask(__name__)

#/api/users/register
@app.route('/api/users/register', methods=['POST'])
def create_user():
    #content_type = request.headers.get('Content-Type')
    user_table = Crud('user_')
    users = user_table.get_all_elements()
    json = request.json
    user_in_bd = False
    if all(key in json.keys() for key in ['email', 'pw', 'name']):
        for user in users:
            if(user['email'] == json['email']):
                user_in_bd = True
        if(not user_in_bd):
            cols, values = RoutesHelper.insert_element('user_', json.items())
            user_holder = user_table.getElements_and_operator(cols, values)
            user_row = user_holder[0]
            user_id = user_row['id']
            return make_response({
                'message': 'User created successfully',
                'user_id': user_id
            }),201
        else:
            return make_response({"error": "An account with this email already exists."}), 409
    else:
        message = 'Missing required fields'
        return make_response({'error': message}), 400
    

@app.route('/api/users/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('pw')

    users_table = Crud('user_')
    users = users_table.getElements_and_operator(['email', 'pw'], [email, password])
    if(users):
        for user in users:
            if(user['email'] == email and user['pw'] == password):
                message = {"message": "Logged in successfully.", 'user_id': user['id']}
                return make_response(message), 200
    message = {'error': 'Invalid username or password'}
    return make_response(message), 401

@app.route('/api/users/info', methods=['POST'])
def get_user():
    user_id = request.json.get('id')
    if user_id:
        users_table = Crud('user_')
        user = users_table.get_element_by_pk(user_id, 'id')
        if user:
            return make_response(user)
        else:   
            return make_response({'error':'User not found.'}), 404
    else:
        return make_response({'error':'Missing id field.'}), 404

@app.route('/api/users/update', methods=['POST'])
def update_user():
    json = request.json
    user_id = json.get('id') 
    if user_id:
        handler = Crud('user_')
        for key in json.keys():
            if key not in handler.get_columns():
                return make_response({'error':'Invalid fields for update.'})
        element = handler.get_element_by_pk(user_id, 'id')
        if(element):
            RoutesHelper.update_element('user_', json.items(), user_id)
            return make_response({'message':'Updated.'})
        else:   
            return make_response({'error':'User not found.'}), 404
    else:
        return make_response({'error':'Missing id field.'}), 404


@app.route('/api/products/search', methods=['POST']) # recebe um json com um elemento (coluna:valor) query coluna like valor
def get_products_like():
    json = request.json
    keys = list(json.keys())
    if len(keys) == 1:
        handler = Crud('product')
        db_columns = handler.get_columns()
        search_col = keys[0]
        if(search_col not in db_columns):
            return make_response({'error':'Missing a valid column to search.'}), 404
        search_value = json.get(search_col)
        if search_col:
            handler = Crud('product')
            items = handler.getElementsLike(search_col, search_value)
            return make_response(items)
    else:
        return make_response({'error':'Only 1 parameter can be sent.'})

@app.route('/api/products/info', methods=['POST'])
def get_product():
    product_id = request.json.get('id')
    if product_id:
        handler = Crud('product')
        product = handler.get_element_by_pk(product_id, 'id')
        if product:
            return make_response(product)
        else:   
            return make_response({'error':'Product not found.'}), 404
    else:
        return make_response({'error':'Missing id field.'}), 404

@app.route('/api/products/filter', methods=['POST'])
def get_product_by_filter():
    json = request.json
    handler = Crud('product')
    cols = handler.get_columns()

    if all(key in cols for key in json.keys()):
        cols = []
        values = []
        for col, value in json.items():
            cols.append(col)
            values.append(value)
        
        items = handler.getElements_and_operator(cols, values)
        if items:
            return make_response(items)
        else:
            return make_response({'error':'Products not found'}), 404
    else:
        return make_response({'error':'Invalid fields sent.'}), 400

@app.route('/api/categories/list', methods=['GET'])
def get_categories():
    handler = Crud('categories')
    categories_list = handler.get_all_elements()
    return make_response(categories_list)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
