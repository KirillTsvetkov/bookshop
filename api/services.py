from models import db, Book, Order, OrderItem, Author, Genre, Publisher, User
from libs.util import sqla2dict


def get_book(id):
    book = Book.query.get(id)
    return sqla2dict(book)


def get_publisher(id):
    publisher = Publisher.query.get(id)
    return sqla2dict(publisher)


def get_user(id):
    user = User.query.get(id)
    return sqla2dict(user)


def get_genre(id):
    genre = Genre.query.get(id)
    return sqla2dict(genre)


def get_author(id):
    author = Author.query.get(id)
    return sqla2dict(author)


def get_order(id):
    order = Order.query.get(id)
    return sqla2dict(order)


def get_order_item(id):
    order = OrderItem.query.get(id)
    return sqla2dict(order)
