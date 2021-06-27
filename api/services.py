from models import db, Book, Order, OrderItem, Author, Genre, Publisher, User
from libs.util import sqla2dict


def get_book(id):
    book = Book.query.get(id)
    return sqla2dict(book)


def edit_book(id, data):
    book = Book.query.get(id)
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
        book = Book.query.get(id)
        return {"result": 0, "book": sqla2dict(book)}
    except:
        return {"result": 1}


def get_books():
    books = db.session.query(Book)
    return [sqla2dict(i) for i in books]


def get_publisher(id):
    publisher = Publisher.query.get(id)
    return sqla2dict(publisher)

def get_publishers():
    publishers = db.session.query(Publisher)
    return [sqla2dict(i) for i in publishers]


def edit_publisher(id, data):
    publisher = Publisher.query.get(id)
    publisher.publisher_name = data['publisher_name']
    try:
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


def get_user(id):
    user = User.query.get(id)
    return sqla2dict(user)


def get_users():
    users = db.session.query(User)
    return [sqla2dict(i) for i in users]


def edit_user(id, data):
    user = User.query.get(id)
    user.username = data['username']
    user.patronymic = data['patronymic']
    user.name = data['name']
    user.surname = data['surname']
    user.password = data['password']
    user.email = data['email']
    try:
        db.session.commit()
        user = User.query.get(id)
        return {"result": 0, "user": sqla2dict(user)}
    except:
        return {"result": 1}


def get_genre(id):
    genre = Genre.query.get(id)
    return sqla2dict(genre)


def get_genres():
    genres = db.session.query(Genre)
    return [sqla2dict(i) for i in genres]


def edit_genre(id, data):
    genre = Genre.query.get(id)
    genre.genre_name = data['genre_name']
    try:
        db.session.commit()
        results = {
            "genre_name": genre.genre_name
        }
        return {"result": 0, "genre": results}
    except:
        return {"result": 1}


def get_author(id):
    author = Author.query.get(id)
    return sqla2dict(author)


def get_authors():
    authors = db.session.query(Author)
    return [sqla2dict(i) for i in authors]


def edit_author(id, data):
    author = Author.query.get(id)
    author.name = data['name']
    author.surname = data['surname']
    author.patronymic = data['patronymic']
    try:
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


def get_order(id):
    order = Order.query.get(id)
    return sqla2dict(order)


def get_orders():
    orders = db.session.query(Order)
    return [sqla2dict(i) for i in orders]


def edit_order(id, data):
    order = Order.query.get(id)
    order.user_id = data['user_id']
    order.total = data['total']
    order.date = data['date']
    try:
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


def get_order_item(id):
    order = OrderItem.query.get(id)
    return sqla2dict(order)


def get_order_items():
    order_items = db.session.query(OrderItem)
    return [sqla2dict(i) for i in order_items]


def edit_order_item(id, data):
    order_item = OrderItem.query.get(id)
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