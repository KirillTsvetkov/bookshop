from flask import Flask, request, render_template, session, redirect
from models import db, Book, Order, OrderItem, Author, Genre, Publisher, User
from flask_migrate import Migrate
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user, current_user
from sqlalchemy import asc, desc, or_, and_
import jsonify
from api.views import api
from crud.views import crud


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/bookshop'
app.config['SECRET_KEY'] = 'secret'
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(crud, url_prefix='/crud')


db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
                            Book.annotation, Book.cover_type,\
                            Author.name, Author.surname, Author.patronymic, Genre.genre_name) \
        .join(Author).join(Genre).filter(Book.slug == slug).first()
    return render_template("shop/book-page.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)
