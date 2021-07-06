from flask import Blueprint, jsonify, request, make_response, jsonify
from flask_expects_json import expects_json
from jsonschema import ValidationError
from .schemas import *
from .services import *
from flask_login import current_user, login_required, logout_user

api = Blueprint('api', __name__)

@api.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)
    return error


@api.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        data = request.get_json()
        return login(data)
    else:
        return current_user.username


@api.route('/logout')
@login_required
def logout():
    logout_user()
    return {"result": 0, "msg": "Вы вышли"}



@api.route('/book/<int:id>', methods=["GET"])
def book(id):
    result = get_book(id)
    return jsonify({'result': result})


@api.route('/book/<int:id>', methods=["DELETE"])
@login_required
def delete_book(id):
    return del_book(id)


@api.route('/book/<int:id>', methods=["PUT"])
@login_required
def update_book(id):
    data = request.get_json()
    result = edit_book(id, data)
    return result


@api.route('/books', methods=["GET", "POST"])
@expects_json(book_schema, ignore_for=['GET'])
def handle_books():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.is_json:
                data = request.get_json()
                return create_book(data)
            else:
                return {"result": 1, "error": "The request payload is not in JSON format"}
        else:
            return {"result": 1, "error": "Вы не авторизованы"}
    else:
        print(current_user)
        result = get_books()
        return jsonify({'result': result})


@api.route('/user/<int:id>', methods=["GET"])
def user(id):
    result = get_user(id)
    return jsonify({'result': result})


@api.route('/users', methods=["GET", "POST"])
@expects_json(user_schema, ignore_for=['GET'])
def handle_users():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.is_json:
                data = request.get_json()
                return create_user(data)
            else:
                return {"error": "The request payload is not in JSON format"}
        else:
            return {"result": 1, "error": "Вы не авторизованы"}
    else:
        result = get_users()
        return jsonify({'result': result})


@api.route('/user/<int:id>', methods=["DELETE"])
@login_required
def delete_user(id):
    return del_user(id)


@api.route('/user/<int:id>', methods=["PUT"])
@login_required
def update_user(id):
    data = request.get_json()
    result = edit_user(id, data)
    return result


@api.route('/publishers', methods=["GET", "POST"])
@expects_json(publisher_schema, ignore_for=['GET'])
def handle_publishers():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.is_json:
                data = request.get_json()
                return create_publisher(data)
            else:
                return {"error": "The request payload is not in JSON format"}
        else:
            return {"result": 1, "error": "Вы не авторизованы"}
    else:
        result = get_publishers()
        return jsonify({'result': result})


@api.route('/publisher/<int:id>', methods=["DELETE"])
@login_required
def delete_publisher(id):
    return del_publisher(id)


@api.route('/publisher/<int:id>', methods=["PUT"])
@login_required
def update_publisher(id):
    data = request.get_json()
    result = edit_publisher(id, data)
    return result


@api.route('/publisher/<int:id>', methods=["GET"])
def publisher(id):
    result = get_publisher(id)
    return jsonify({'result': result})


@api.route('/authors', methods=["GET", "POST"])
@expects_json(author_schema, ignore_for=['GET'])
def handle_authors():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.is_json:
                data = request.get_json()
                return create_author(data)
            else:
                return {"error": "The request payload is not in JSON format"}
        else:
            return {"result": 1, "error": "Вы не авторизованы"}
    else:
        result = get_authors()
        return jsonify({'result': result})


@api.route('/author/<int:id>', methods=["DELETE"])
@login_required
def delete_author(id):
    return del_author(id)


@api.route('/author/<int:id>', methods=["PUT"])
@expects_json(author_schema)
@login_required
def update_author(id):
    data = request.get_json()
    result = edit_author(id, data)
    return result


@api.route('/author/<int:id>', methods=["GET"])
def author(id):
    result = get_author(id)
    return jsonify({'result': result})


@api.route('/orders', methods=["GET", "POST"])
@expects_json(order_schema, ignore_for=['GET'])
def handle_orders():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.is_json:
                data = request.get_json()
                return create_order(data)
            else:
                return {"error": "The request payload is not in JSON format"}
        else:
            return {"result": 1, "error": "Вы не авторизованы"}
    else:
        result = get_orders()
        return jsonify({'result': result})


@api.route('/order/<int:id>', methods=["DELETE"])
@login_required
def delete_order(id):
    return del_order(id)


@api.route('/order/<int:id>', methods=["PUT"])
@login_required
@expects_json(order_schema)
def update_order(id):
    data = request.get_json()
    result = edit_order(id, data)
    return result


@api.route('/order/<int:id>', methods=["GET"])
def order(id):
    result = get_order(id)
    return jsonify({'result': result})


@api.route('/order_items', methods=["GET", "POST"])
@expects_json(order_item_schema, ignore_for=['GET'])
def handle_order_items():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.is_json:
                data = request.get_json()
                return create_orderitems(data)
            else:
                return {"result": 1, "error": "The request payload is not in JSON format"}
        else:
            return {"result": 1, "error": "Вы не авторизованы"}
    else:
        result = get_order_items()
        return jsonify({'result': result})


@api.route('/order_item/<int:id>', methods=["GET"])
def order_item(id):
    result = get_order_item(id)
    return jsonify({'result': result})


@api.route('/order_item/<int:id>', methods=["DELETE"])
@login_required
def delete_order_item(id):
    return del_order_item(id)


@api.route('/order_item/<int:id>', methods=["PUT"])
@login_required
@expects_json(edit_order_item_schema)
def update_order_item(id):
    data = request.get_json()
    result = edit_order_item(id, data)
    return result


@api.route('/genres', methods=["GET", "POST"])
@expects_json(genre_schema, ignore_for=['GET'])
def handle_genres():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.is_json:
                data = request.get_json()
                return create_genre(data)
            else:
                return {"result": 1, "error": "The request payload is not in JSON format"}
        else:
            return {"result": 1, "error": "Вы не авторизованы"}
    else:
        result = get_genres()
        return jsonify({'result': result})


@api.route('/genre/<int:id>', methods=["PUT"])
@login_required
@expects_json(genre_schema)
def update_genre(id):
    data = request.get_json()
    result = edit_genre(id, data)
    return result


@api.route('/genre/<int:id>', methods=["GET"])
def genre(id):
    result = get_genre(id)
    return jsonify({'result': result})


@api.route('/genre/<int:id>', methods=["DELETE"])
@login_required
def delete_genre(id):
    return del_genre(id)
