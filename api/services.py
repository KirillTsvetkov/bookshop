from models import db, Book, Order, OrderItem, Author, Genre, Publisher, User
from libs.util import sqla2dict


def get_book(id):
    book = Book.query.get(id)
    return sqla2dict(book)


def get_books():
    books = db.session.query(Book)
    return [sqla2dict(i) for i in books]


def get_publisher(id):
    publisher = Publisher.query.get(id)
    return sqla2dict(publisher)

def get_publishers():
    publishers = db.session.query(Publisher)
    return [sqla2dict(i) for i in publishers]


def get_user(id):
    user = User.query.get(id)
    return sqla2dict(user)


def get_users():
    users = db.session.query(User)
    return [sqla2dict(i) for i in users]


def get_genre(id):
    genre = Genre.query.get(id)
    return sqla2dict(genre)


def get_genres():
    genres = db.session.query(Genre)
    return [sqla2dict(i) for i in genres]


def get_author(id):
    author = Author.query.get(id)
    return sqla2dict(author)


def get_authors():
    authors = db.session.query(Author)
    return [sqla2dict(i) for i in authors]


def get_order(id):
    order = Order.query.get(id)
    return sqla2dict(order)


def get_orders():
    orders = db.session.query(Order)
    return [sqla2dict(i) for i in orders]



def get_order_item(id):
    order = OrderItem.query.get(id)
    return sqla2dict(order)


def get_order_items():
    order_items = db.session.query(OrderItem)
    return [sqla2dict(i) for i in order_items]
