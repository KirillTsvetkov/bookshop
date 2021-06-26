from flask import Flask, request, render_template, session, redirect
from models import db, Book, Order, OrderItem, Author, Genre, Publisher, User
from flask_migrate import Migrate
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user, current_user
from sqlalchemy import asc, desc, or_, and_
import jsonify
from api.views import api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/bookshop'
app.config['SECRET_KEY'] = 'secret'
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(api, url_prefix='/api')

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/genres-list', methods=["GET"])
def genreslist():
    genres = Genre.query.all()
    return render_template("genres-list.html", genres=genres)


@app.route('/publishers-list', methods=["GET"])
def publisherslist():
    publishers = Publisher.query.all()
    return render_template("publishers-list.html", publishers=publishers)


@app.route('/authors-list', methods=["GET"])
def authorslist():
    authors = Author.query.all()
    return render_template("authors-list.html", authors=authors)


@app.route('/edit-author/<int:id>', methods=["GET"])
def edit_author(id):
    author = Author.query.get(id)
    if author is None:
        return "Издатель не найден"
    return render_template("edit-author.html", author=author)


@app.route('/edit-user/<int:id>', methods=["GET"])
def edit_user(id):
    user = User.query.get(id)
    print(user.username)
    if user is None:
        return "Пользователь не найден"
    return render_template("edit-user.html", user=user)


@app.route('/edit-publisher/<int:id>', methods=["GET"])
def edit_publisher(id):
    publisher = Publisher.query.get(id)
    if publisher is None:
        return "Издатель не найден"
    return render_template("edit-publisher.html", publisher=publisher)


@app.route('/edit-book/<int:id>', methods=["GET"])
def edit_book(id):
    book = Book.query.get(id)
    if book is None:
        return "Книга не найдена"
    authors = Author.query.all()
    genres = Genre.query.all()
    publishers = Publisher.query.all()
    return render_template("edit-book.html", book=book, authors=authors, genres=genres, publishers=publishers)


@app.route('/edit-order/<int:id>', methods=["GET"])
def edit_order(id):
    order = Order.query.get(id)
    if order is None:
        return "Заказ не найден"
    users = User.query.all()

    return render_template("edit-order.html", order=order, users=users)


@app.route('/edit-order_item/<int:id>', methods=["GET"])
def edit_order_item(id):
    order_item = OrderItem.query.get(id)
    if order_item is None:
        return "Позиция заказа не найдена"
    books = Book.query.all()
    orders = db.session.query(Order.id, Order.date, Order.total, User.username).join(User).all()
    return render_template("edit-order_item.html", order_item=order_item, books=books, orders=orders)


@app.route('/books-list', methods=["GET"])
def bookslist():
    books = db.session.query(Book.title, Book.id, Book.price, Author.name, Author.surname, Genre.genre_name,
                             Publisher.publisher_name).join(Author).join(Genre).join(Publisher).all()
    return render_template("books-list.html", books=books)


@app.route('/orders-list', methods=["GET"])
def orderslist():
    orders = db.session.query(Order.id, Order.date, Order.total, User.username).join(User).all()
    return render_template("orders-list.html", orders=orders)


@app.route('/order_items-list', methods=["GET"])
def order_itemslist():
    order_items = db.session.query(OrderItem.id, OrderItem.quantity, OrderItem.cost, Order.date, User.username,
                                   Book.title).select_from(OrderItem). \
        join(OrderItem.order).join(Book).join(User)
    return render_template("order_items-list.html", order_items=order_items)


@app.route('/users-list', methods=["GET"])
def userslist():
    users = User.query.all()
    return render_template("users-list.html", users=users)


@app.route('/edit-genre/<int:id>', methods=["GET"])
def edit_genre(id):
    genre = Genre.query.get(id)
    return render_template("edit-genre.html", genre=genre)


@app.route('/create-genre', methods=["GET"])
def create_genre():
    return render_template("create-genre.html")


@app.route('/create-user', methods=["GET"])
def create_user():
    return render_template("create-user.html")


@app.route('/create-book', methods=["GET"])
def create_book():
    genres = Genre.query.all()
    authors = Author.query.all()
    publishers = Publisher.query.all()
    return render_template("create-book.html", genres=genres, authors=authors, publishers=publishers)


@app.route('/create-author', methods=["GET"])
def create_author():
    return render_template("create-author.html")


@app.route('/create-publisher', methods=["GET"])
def create_publisher():
    return render_template("create-publisher.html")


@app.route('/create-order', methods=["GET"])
def create_order():
    users = db.session.query(User.id, User.username)
    return render_template("create-order.html", users=users)


@app.route('/create-order_item', methods=["GET"])
def create_order_item():
    orders = db.session.query(Order.id, Order.date, Order.total, User.username).join(User).all()
    books = db.session.query(Book.id, Book.title).all()
    return render_template("create-order_item.html", orders=orders, books=books)


@app.route('/test', methods=["GET"])
def test():
    bookInfo = db.session.query(Book.title, Book.price, Author.name, Author.surname).join(Author).join(Genre).join(
        Publisher).all()

    return "0"


@app.route('/', methods=["GET"])
def home():
    books = db.session.query(Book.id, Book.title, Book.price, Author.name, Author.surname).join(Author).all()
    return render_template("shop/home.html", books=books)


@app.route('/search', methods=["GET"])
def search():
    search = request.args.get('search')
    books = db.session.query(Book.id, Book.title, Book.price, Author.name, Author.surname).join(Author). \
        filter(or_(Book.title.like(search), Author.name.like(search), Author.surname.like(search), \
                   Author.patronymic.like(search))).all()
    return render_template("shop/home.html", books=books)


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user.password == password:
            login_user(user)
            return redirect('/')
        else:
            return "Неверный пароль"
    else:
        return render_template("shop/auth.html")


@app.route('/add_in_bag', methods=['POST'])
def add_in_book():
    book_id = request.form['book_id']
    if 'books' not in session:
        session['books'] = []
    books_list = session['books']
    if book_id not in books_list:
        books_list.append(book_id)
    session['books'] = books_list
    print(session['books'])
    return {"result": 0}


@app.route('/bag', methods=['GET'])
def bag():
    books_in_bag = []
    if 'books' in session:
        for book in session['books']:
            book_in_bag = db.session.query(Book.id, Book.title, Book.price, Author.name, Author.surname).join(Author). \
                filter(Book.id == book).first()
            books_in_bag.append(book_in_bag)
            print(session['books'])
    return render_template("shop/bag.html", books_in_bag=books_in_bag)


@app.route('/order_from_bag', methods=['POST'])
def order_from_bag():
    data = request.get_json()
    user_id = current_user.id
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


@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    books = db.session.query(Book.id, Book.title, Book.price, Author.name, Author.surname).join(Author).all()
    return render_template('shop/home.html', books=books)


@app.route('/old-orders', methods=['GET'])
def old_orders():
    user_id = current_user.id
    orders = Order.query.filter(Order.user_id == user_id).all()
    print(orders)
    return render_template("shop/old-orders.html", orders=orders)


@app.route('/order-page/<int:id>', methods=['GET'])
def order_page(id):
    order = db.session.query(Order.date, Order.total, OrderItem.quantity, OrderItem.cost, Book.title,
                             Book.slug).select_from(Order). \
        join(OrderItem).join(Book).filter(Order.id == id).all()

    print(order[0].total)
    return render_template("shop/order-page.html", order=order)


@app.route('/book-page/<slug>', methods=['GET'])
def book_page(slug):
    book = db.session.query(Book.id, Book.title, Book.price, Book.year, Book.number_of_pages, Book.isbn,
                            Book.annotation, Book.cover_type, \
                            Author.name, Author.surname, Author.patronymic, Genre.genre_name) \
        .join(Author).join(Genre).filter(Book.slug == slug).first()
    return render_template("shop/book-page.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)
