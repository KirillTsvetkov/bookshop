from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import or_, desc

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    patronymic = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(30), nullable=False)


    @classmethod
    def list(cls):
        return User.query.all()

    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()


    @classmethod
    def get_all_usernames(cls):
        return db.session.query(User.id, User.username)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=True)
    patronymic = db.Column(db.String(40), nullable=True)

    def __repr__(self):
        return '<Author %r>' % self.name


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, default=0)

    @classmethod
    def list(cls):
        return db.session.query(Order.id, Order.date, Order.total, User.username).join(User).all()


    @classmethod
    def old_orders(cls, user_id):
        return Order.query.filter(Order.user_id == user_id).order_by(desc(Order.date)).all()


    @classmethod
    def view_info(cls, id):
        return db.session.query(Order.date, Order.total, OrderItem.quantity, OrderItem.cost, Book.title,
                         Book.slug).select_from(Order). \
            join(OrderItem).join(Book).filter(Order.id == id).all()


    @classmethod
    def all_orders(cls):
        return db.session.query(Order.id, Order.date, Order.total, User.username).join(User).all()


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('Order', backref=db.backref('orderItems', lazy=True))
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('orderItems', lazy=True))


    @classmethod
    def list(cls):
        return db.session.query(OrderItem.id, OrderItem.quantity, OrderItem.cost, Order.date, User.username,
                         Book.title).select_from(OrderItem). \
            join(OrderItem.order).join(Book).join(User)


    @classmethod
    def all_items_in_order(cls, order):
        return OrderItem.query.filter(order == order).all()


class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publisher_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Publisher %r>' % self.publisher_name


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<Genre %r>' % self.genre_name

    @classmethod
    def get_all_genres(cls):
        return Genre.query.all()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    number_of_pages = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(100), nullable=False)
    cover_type = db.Column(db.Boolean, nullable=False)
    annotation = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    genre = db.relationship('Genre', backref=db.backref('books', lazy=True))
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)
    publisher = db.relationship('Publisher', backref=db.backref('books', lazy=True))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return '<Book %r>' % self.title


    @classmethod
    def list(cls):
        return db.session.query(Book.title, Book.id, Book.price, Author.name, Author.surname, Genre.genre_name,
                         Publisher.publisher_name).join(Author).join(Genre).join(Publisher).all()

    @classmethod
    def get_all_titles(cls):
        return db.session.query(Book.id, Book.title).all()


    @classmethod
    def get_main_info(cls):
        return db.session.query(Book.id, Book.slug,Book.title, Book.price, Author.name, Author.surname).join(Author).all()


    @classmethod
    def search(cls, search):
        return db.session.query(Book.id, Book.title, Book.price, Author.name, Author.surname).join(Author). \
            filter(or_(Book.title.like(search), Author.name.like(search), Author.surname.like(search), \
                       Author.patronymic.like(search))).all()


    @classmethod
    def info_for_page(cls, slug):
        return db.session.query(Book.id, Book.title, Book.price, Book.year, Book.number_of_pages, Book.isbn,
                         Book.annotation, Book.cover_type, \
                         Author.name, Author.surname, Author.patronymic, Genre.genre_name) \
            .join(Author).join(Genre).filter(Book.slug == slug).first()


    @classmethod
    def in_bag(cls, book_id):
        return db.session.query(Book.id, Book.title, Book.price, Author.name, Author.surname).join(Author). \
            filter(Book.id == book_id).first()