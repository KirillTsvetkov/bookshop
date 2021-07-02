from flask import Blueprint, jsonify, request, render_template, session, redirect
from flask_login import login_required, logout_user, login_user, current_user

from .services import *

shop = Blueprint('shop', __name__, template_folder='templates', static_folder='static')


@shop.route('/', methods=["GET"])
def home():
    books = Book.get_main_info()
    return render_template("shop/home.html", books=books)


@shop.route('/genre/<int:gener_id>', methods=["GET"])
def genre_page(gener_id):
    books = Book.get_all_books_genre(gener_id)
    return render_template("shop/home.html", books=books)


@shop.route('/author/<int:author_id>', methods=["GET"])
def author_page(author_id):
    books = Book.get_all_books_author(author_id)
    return render_template("shop/home.html", books=books)


@shop.route('/publisher/<int:publisher_id>', methods=["GET"])
def publisher_page(publisher_id):
    books = Book.get_all_books_publisher(publisher_id)
    return render_template("shop/home.html", books=books)


@shop.route('/search', methods=["GET"])
def search():
    search = request.args.get('search')
    books = Book.search(search)
    return render_template("shop/home.html", books=books)



@shop.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == "POST":
        return login(request.form)
    else:
        return render_template("shop/auth.html")


@shop.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        return reg(request.form)
    else:
        return render_template("shop/reg.html")


@shop.route('/add_in_bag', methods=['POST'])
def add_in_book():
    book_id = request.form['book_id']
    return add_item_in_card(book_id)


@shop.route('/bag', methods=['GET'])
def bag():
    books_in_bag = create_shop_card()
    return render_template("shop/bag.html", books_in_bag=books_in_bag)


@shop.route('/order_from_bag', methods=['POST'])
def order_from_bag():
    data = request.get_json()
    user_id = current_user.id
    result = create_order_from_bag(data, user_id)
    return result


@shop.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    books = Book.get_main_info()
    return render_template('shop/home.html', books=books)


@shop.route('/old-orders', methods=['GET'])
def old_orders():
    user_id = current_user.id
    orders = Order.old_orders(user_id)
    return render_template("shop/old-orders.html", orders=orders)


@shop.route('/order-page/<int:id>', methods=['GET'])
def order_page(id):
    order = Order.view_info(id)
    return render_template("shop/order-page.html", order=order)


@shop.route('/book-page/<slug>', methods=['GET'])
def book_page(slug):
    book = Book.info_for_page(slug)
    print(book)
    return render_template("shop/book-page.html", book=book)


