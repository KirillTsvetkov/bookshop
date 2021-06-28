from flask import session, redirect
from models import db, Book, Order, OrderItem, User
from datetime import datetime
from flask_login import login_user

def create_order_from_bag(data, user_id):
    total = data['order']['total']
    order = Order(user_id=user_id, date=datetime.utcnow(), total=total)
    try:
        db.session.add(order)
        db.session.commit()
    except:
        return {"result": 1}
    order_items_list = data['order_items_list']
    for item in order_items_list:
        order_item = OrderItem(book_id=int(item['book_id']), quantity=int(item['quantity']), order=order,
                               cost=float(item['cost']))
        try:
            db.session.add(order_item)
            db.session.commit()
        except:
            return {"result": 1}
    session['books'] = []
    return {"result": 0}


def add_item_in_card(book_id):
    if 'books' not in session:
        session['books'] = []
    books_list = session['books']
    if book_id not in books_list:
        books_list.append(book_id)
    session['books'] = books_list
    return {"result": 0}


def create_shop_card():
    books_in_bag = []
    if 'books' in session:
        for book in session['books']:
            book_in_bag = Book.in_bag(book)
            books_in_bag.append(book_in_bag)
    return books_in_bag


def login(data):
    username = data['username']
    password = data['password']
    user = User.get_by_username(username)
    if user.password == password:
        login_user(user)
        return redirect('/shop')
    else:
        return "Неверный пароль"

