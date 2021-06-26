# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from .services import *


api = Blueprint('api', __name__)


@api.route('/book/<int:id>', methods=["GET"])
def book(id):
    result = get_book(id)
    return jsonify({'result': result})


@api.route('/book/<int:id>', methods=["DELETE"])
def delete_book(id):
    book = Book.query.get(id)
    try:
        db.session.delete(book)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@api.route('/book/<int:id>', methods=["PUT"])
def update_book(id):
    book = Book.query.get(id)
    data = request.get_json()
    book.title = data['title']
    book.price = data['price']
    book.number_of_pages = data['number_of_pages']
    book.year = data['year']
    book.isbn = data['isbn']
    book.cover_type = bool(data['cover_type'])
    book.annotation = data['annotation']
    book.slug = data['slug']
    book.genre_id = int(data['genre_id'])
    book.publisher_id = int(data['publisher_id'])
    book.author_id = int(data['author_id'])
    try:
        db.session.commit()
        results = {
            "title": book.title,
            "price": book.price,
            "number_of_pages": book.number_of_pages,
            "year": book.year,
            "isbn": book.isbn,
            "cover_type": book.cover_type,
            "annotation": book.annotation,
            "slug": book.slug,
            "genre_id": book.genre_id,
            "publisher_id": book.publisher_id,
            "author_id": book.author_id
        }
        return {"result": 0, "book": results}
    except:
        return {"result": 1}


@api.route('/books', methods=["GET", "POST"])
def handle_books():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            book = Book(title=data['title'],
                        price=float(data['price']), number_of_pages=int(data['number_of_pages']),
                        year=int(data['year']), isbn=data['isbn'],
                        cover_type=bool(data['cover_type']),
                        annotation=data['annotation'], slug=data['slug'],
                        genre_id=int(data['genre_id']), publisher_id=int(data['publisher_id']),
                        author_id=int(data['author_id']))
            try:
                db.session.add(book)
                db.session.commit()
                return {"result": 0, "msg": f"book {book} успешно добавлен"}
            except:
                return {"result": 1, "error": "ошибка добавления"}
        else:
            return {"result": 1, "error": "The request payload is not in JSON format"}
    else:
        books = Book.query.all()
        results = [
            {
                "title": book.title,
                "price": float(book.price),
                "number_of_pages": book.number_of_pages,
                "year": book.year,
                "isbn": book.isbn,
                "cover_type": book.cover_type,
                "annotation": book.annotation,
                "slug": book.slug,
                "genre_id": book.genre_id,
                "publisher_id": book.publisher_id,
                "author_id": book.author_id
            } for book in books]
        return {"coutn": len(results), "users": results}


@api.route('/user/<int:id>', methods=["GET"])
def user(id):
    result = get_user(id)
    return jsonify({'result': result})


@api.route('/users', methods=["GET", "POST"])
def handle_users():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            user = User(username=data['username'], name=data['name'], surname=data['surname'],
                        patronymic=data['patronymic'], email=data['email'], password=data['password'])
            try:
                db.session.add(user)
                db.session.commit()
                return {"result": 0, "msg": f"user {user} успешно добавлен"}
            except:
                return {"result": 1, "error": "ошибка добавления"}
        else:
            return {"error": "The request payload is not in JSON format"}
    else:
        users = User.query.all()
        results = [
            {
                "username": user.username,
                "name": user.name,
                "surname": user.surname,
                "patronymic": user.patronymic,
                "email": user.email,
                "password": user.password
            } for user in users]
        return {"coutn": len(results), "users": results}


@api.route('/user/<int:id>', methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@api.route('/user/<int:id>', methods=["PUT"])
def update_user(id):
    user = User.query.get(id)
    data = request.get_json()
    user.username = data['username']
    user.patronymic = data['patronymic']
    user.name = data['name']
    user.surname = data['surname']
    user.password = data['password']
    user.email = data['email']
    try:
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@api.route('/publishers', methods=["GET", "POST"])
def handle_publishers():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            publisher = Publisher(publisher_name=data['publisher_name'])
            try:
                db.session.add(publisher)
                db.session.commit()
                return {"result": 0, "msg": f"publisher {publisher} успешно добавлен"}
            except:
                return {"result": 1, "error": "ошибка добавления"}
        else:
            return {"error": "The request payload is not in JSON format"}
    else:
        publishers = Publisher.query.all()
        results = [
            {
                "publisher_name": publisher.publisher_name
            } for publisher in publishers]
        return {"coutn": len(results), "publishers": results}


@api.route('/publisher/<int:id>', methods=["DELETE"])
def delete_publisher(id):
    publisher = Publisher.query.get(id)
    try:
        db.session.delete(publisher)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@api.route('/publisher/<int:id>', methods=["PUT"])
def update_publisher(id):
    publisher = Publisher.query.get(id)
    data = request.get_json()
    publisher.publisher_name = data['publisher_name']
    try:
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@api.route('/publisher/<int:id>', methods=["GET"])
def publisher(id):
    result = get_publisher(id)
    return jsonify({'result': result})


@api.route('/authors', methods=["GET", "POST"])
def handle_authors():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            author = Author(name=data['name'], surname=data['surname'], patronymic=data['patronymic'])
            try:
                db.session.add(author)
                db.session.commit()
                return {"result": 0, "msg": f"author {author} успешно добавлен"}
            except:
                return {"result": 1, "error": "ошибка добавления"}
        else:
            return {"error": "The request payload is not in JSON format"}
    else:
        authors = Author.query.all()
        results = [
            {
                "name": author.name,
                "surname": author.surname,
                "patronymic": author.patronymic
            } for author in authors]
        return {"coutn": len(results), "authors": results}


@api.route('/author/<int:id>', methods=["DELETE"])
def delete_author(id):
    author = Author.query.get(id)
    try:
        db.session.delete(author)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@api.route('/author/<int:id>', methods=["PUT"])
def update_author(id):
    author = Author.query.get(id)
    data = request.get_json()
    author.name = data['name']
    author.surname = data['surname']
    author.patronymic = data['patronymic']
    try:
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@api.route('/author/<int:id>', methods=["GET"])
def author(id):
    result = get_author(id)
    return jsonify({'result': result})


@api.route('/orders', methods=["GET", "POST"])
def handle_orders():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            order = Order(user_id=data['user_id'], date=data['date'], total=data['total'])
            try:
                db.session.add(order)
                db.session.commit()
                return {"result": 0, "msg": f"order {order} успешно добавлен"}
            except:
                return {"result": 1, "error": "ошибка добавления"}
        else:
            return {"error": "The request payload is not in JSON format"}
    else:
        orders = Order.query.all()
        results = [
            {
                "total": order.total,
                "date": order.date,
                "user_id": order.user_id
            } for order in orders]
        return {"coutn": len(results), "orders": results}


@api.route('/order/<int:id>', methods=["DELETE"])
def delete_order(id):
    order = Order.query.get(id)
    try:
        db.session.delete(order)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@api.route('/order/<int:id>', methods=["PUT"])
def update_order(id):
    order = Order.query.get(id)
    data = request.get_json()
    order.user_id = data['user_id']
    order.total = data['total']
    order.date = data['date']
    try:
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@api.route('/order/<int:id>', methods=["GET"])
def order(id):
    result = get_order(id)
    return jsonify({'result': result})


@api.route('/order_items', methods=["GET", "POST"])
def handle_order_items():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            count = 0
            for item in data:
                order_item = OrderItem(order_id=int(item['order_id']), quantity=int(item['quantity']),
                                       cost=float(item['cost']), book_id=int(item['book_id']))
                try:
                    db.session.add(order_item)
                    db.session.commit()
                    order = order_item.order
                    order.total += order_item.cost
                    db.session.commit()
                    count = count + 1
                except:
                    return {"result": 1, "error": "ошибка добавления"}
            if (count == len(data)):
                return {"result": 0, "msg": 'Добавленно "+str(count)+" Записей"'}
        else:
            return {"result": 1, "error": "The request payload is not in JSON format"}
    else:
        orders = Order.query.all()
        results = [
            {
                "total": order.total,
                "date": order.date,
                "user_id": order.user_id
            } for order in orders]
        return {"coutn": len(results), "orders": results}


@api.route('/order_item/<int:id>', methods=["GET"])
def order_item(id):
    result = get_order_item(id)
    return jsonify({'result': result})


@api.route('/order_item/<int:id>', methods=["DELETE"])
def delete_order_item(id):
    order_item = OrderItem.query.get(id)
    try:
        db.session.delete(order_item)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@api.route('/order_item/<int:id>', methods=["PUT"])
def update_order_item(id):
    order_item = OrderItem.query.get(id)
    data = request.get_json()
    order_item.book_id = data['book_id']
    order_item.cost = float(data['cost'])
    order_item.order_id = data['order_id']
    order_item.quantity = data['quantity']
    order = order_item.order
    try:
        db.session.commit()
        order_itemslist = OrderItem.query.filter(order == order).all()
        sum = 0
        for item in order_itemslist:
            sum += item.cost
        order.total = sum
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@api.route('/genres', methods=["GET", "POST"])
def handle_genres():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            genre = Genre(genre_name=data['genre_name'])
            try:
                db.session.add(genre)
                db.session.commit()
                return {"result": 0, "msg": f"genre {genre} успешно добавлен"}
            except:
                return {"result": 1, "error": "ошибка добавления"}
        else:
            return {"result": 1, "error": "The request payload is not in JSON format"}
    else:
        genres = Genre.query.all()
        results = [
            {
                "genre_name": genre.genre_name
            } for genre in genres]
        return {"coutn": len(results), "genres": results}


@api.route('/genre/<int:id>', methods=["PUT"])
def update_genre(id):
    genre = Genre.query.get(id)
    data = request.get_json()
    genre.genre_name = data['genre_name']
    try:
        db.session.commit()
        results = {
            "genre_name": genre.genre_name
        }
        return {"result": 0, "genre": results}
    except:
        return {"result": 1}


@api.route('/genre/<int:id>', methods=["GET"])
def genre(id):
    result = get_genre(id)
    return jsonify({'result': result})


@api.route('/genre/<int:id>', methods=["DELETE"])
def delete_genre(id):
    genre = Genre.query.get(id)
    try:
        db.session.delete(genre)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}
