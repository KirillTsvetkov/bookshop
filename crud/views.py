from flask import Blueprint, jsonify, request, render_template
from models import db, Book, Order, OrderItem, Author, Genre, Publisher, User
from flask_login import login_required
from .services import *

crud = Blueprint('crud', __name__,template_folder='templates', static_folder='static')


@crud.route('/genres-list/<int:page_num>', methods=["GET"])
def genreslist(page_num):
    genres = Genre.list(page_num)
    return render_template("crud/genres-list.html", genres=genres)


@crud.route('/genres-search', methods=["GET"])
def genres_search():
    search = request.args.get('search')
    genres = Genre.search(search)
    return render_template("crud/genres-list.html", genres=genres)


@crud.route('/edit-genre/<int:id>', methods=["GET"])
def edit_genre(id):
    genre = Genre.query.get(id)
    return render_template("crud/edit-genre.html", genre=genre)


@crud.route('/create-genre', methods=["GET"])
def create_genre():
    return render_template("crud/create-genre.html")



@crud.route('/publishers-list/<int:page_num>', methods=["GET"])
def publisherslist(page_num):
    publishers = Publisher.list(page_num)
    return render_template("crud/publishers-list.html", publishers=publishers)


@crud.route('/create-publisher', methods=["GET"])
def create_publisher():
    return render_template("crud/create-publisher.html")


@crud.route('/edit-publisher/<int:id>', methods=["GET"])
@login_required
def edit_publisher(id):
    publisher = Publisher.query.get(id)
    if publisher is None:
        return "Издатель не найден"
    return render_template("crud/edit-publisher.html", publisher=publisher)


@crud.route('/authors-list/<int:page_num>', methods=["GET"])
def authorslist(page_num):
    authors = Author.list(page_num)
    return render_template("crud/authors-list.html", authors=authors)


@crud.route('/create-author', methods=["GET"])
def create_author():
    return render_template("crud/create-author.html")


@crud.route('/edit-author/<int:id>', methods=["GET"])
def edit_author(id):
    author = Author.query.get(id)
    if author is None:
        return "Издатель не найден"
    return render_template("crud/edit-author.html", author=author)


@crud.route('/books-list/<int:page_num>', methods=["GET"])
def bookslist(page_num):
    books = Book.list(page_num)
    return render_template("crud/books-list.html", books=books)


@crud.route('/create-book', methods=["GET"])
def create_book():
    genres = Genre.query.all()
    authors = Author.query.all()
    publishers = Publisher.query.all()
    return render_template("crud/create-book.html", genres=genres, authors=authors, publishers=publishers)


@crud.route('/edit-book/<int:id>', methods=["GET"])
def edit_book(id):
    book = Book.query.get(id)
    if book is None:
        return "Книга не найдена"
    authors = Author.query.all()
    genres = Genre.query.all()
    publishers = Publisher.query.all()
    return render_template("crud/edit-book.html", book=book, authors=authors, genres=genres, publishers=publishers)



@crud.route('/orders-list/<int:page_num>', methods=["GET"])
def orderslist(page_num):
    orders = Order.list(page_num)
    return render_template("crud/orders-list.html", orders=orders)


@crud.route('/create-order', methods=["GET"])
def create_order():
    users = User.get_all_usernames()
    return render_template("crud/create-order.html", users=users)


@crud.route('/edit-order/<int:id>', methods=["GET"])
def edit_order(id):
    order = Order.query.get(id)
    if order is None:
        return "Заказ не найден"
    users = User.query.all()
    return render_template("crud/edit-order.html", order=order, users=users)


@crud.route('/order_items-list/<int:page_num>', methods=["GET"])
def order_itemslist(page_num):
    order_items = OrderItem.list(page_num)
    return render_template("crud/order_items-list.html", order_items=order_items)


@crud.route('/edit-order_item/<int:id>', methods=["GET"])
def edit_order_item(id):
    order_item = OrderItem.query.get(id)
    if order_item is None:
        return "Позиция заказа не найдена"
    books = Book.query.all()
    orders = Order.all_orders()
    return render_template("crud/edit-order_item.html", order_item=order_item, books=books, orders=orders)


@crud.route('/create-order_item', methods=["GET"])
def create_order_item():
    orders = Order.all_orders()
    books = Book.get_all_titles()
    return render_template("crud/create-order_item.html", orders=orders, books=books)


@crud.route('/users-list/<int:page_num>', methods=["GET"])
def userslist(page_num):
    users = User.list(page_num)
    return render_template("crud/users-list.html", users=users)


@crud.route('/create-user', methods=["GET"])
def create_user():
    return render_template("crud/create-user.html")


@crud.route('/edit-user/<int:id>', methods=["GET"])
def edit_user(id):
    user = User.query.get(id)
    if user is None:
        return "Пользователь не найден"
    return render_template("crud/edit-user.html", user=user)