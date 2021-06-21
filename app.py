from flask import Flask, request, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user, current_user
from sqlalchemy import asc, desc, or_, and_
import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/bookshop'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    patronymic = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(30), nullable=False)


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


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('Order', backref=db.backref('orderItems', lazy=True))
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('orderItems', lazy=True))


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
    orders = Order.query.all()
    return render_template("edit-order_item.html", order_item=order_item, books=books, orders=orders)


@app.route('/books-list', methods=["GET"])
def bookslist():
    books = db.session.query(Book.title, Book.id, Book.price, Author.name, Author.surname, Genre.genre_name, Publisher.publisher_name).join(Author).join(Genre).join(Publisher).all()
    return render_template("books-list.html", books=books)


@app.route('/orders-list', methods=["GET"])
def orderslist():
    orders = db.session.query(Order.id, Order.date, Order.total, User.username).join(User).all()
    return render_template("orders-list.html", orders=orders)


@app.route('/order_items-list', methods=["GET"])
def order_itemslist():
    order_items = db.session.query(OrderItem.id, OrderItem.quantity, OrderItem.cost, Order.date, User.username, Book.title).select_from(OrderItem).\
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


@app.route('/genres', methods=["GET", "POST"])
def handle_genres():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            genre = Genre(genre_name=data['genre_name'])
            try:
                db.session.add(genre)
                db.session.commit()
                return {"result": 0, "msg":f"genre {genre} успешно добавлен"}
            except:
                return {"result": 1, "error":"ошибка добавления"}
        else:
            return {"result": 1, "error": "The request payload is not in JSON format"}
    else:
        genres = Genre.query.all()
        results = [
            {
                "genre_name": genre.genre_name
            } for genre in genres]
        return {"coutn": len(results), "genres": results}


@app.route('/genre/<int:id>', methods=["PUT"])
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


@app.route('/genre/<int:id>', methods=["GET"])
def get_genre(id):
    genre = Genre.query.get(id)
    results = {
        "genre_name": genre.genre_name
    }
    return {"genre": results}


@app.route('/genre/<int:id>', methods=["DELETE"])
def delete_genre(id):
    genre = Genre.query.get(id)
    try:
        db.session.delete(genre)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@app.route('/books', methods=["GET", "POST"])
def handle_books():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            book = Book(title = data['title'],
                        price=float(data['price']), number_of_pages=int(data['number_of_pages']),
                        year=int(data['year']), isbn=data['isbn'],
                        cover_type=bool(data['cover_type']),
                        annotation=data['annotation'], slug=data['slug'],
                        genre_id=int(data['genre_id']), publisher_id=int(data['publisher_id']),
                        author_id=int(data['author_id']))
            try:
                db.session.add(book)
                db.session.commit()
                return {"result": 0, "msg":f"book {book} успешно добавлен"}
            except:
                return {"result": 1, "error":"ошибка добавления"}
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


@app.route('/book/<int:id>', methods=["GET"])
def get_book(id):
    book = Book.query.get(id)
    results = {
            "title": book.title,
            "price": book.price
            }

    return {"book": results}


@app.route('/book/<int:id>', methods=["PUT"])
def update_book(id):
    book = Book.query.get(id)
    data = request.get_json()
    book.title=data['title']
    book.price=data['price']
    book.number_of_pages=data['number_of_pages']
    book.year=data['year']
    book.isbn=data['isbn']
    book.cover_type=bool(data['cover_type'])
    book.annotation=data['annotation']
    book.slug=data['slug']
    book.genre_id=int(data['genre_id'])
    book.publisher_id=int(data['publisher_id'])
    book.author_id=int(data['author_id'])
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
        return {"result":0, "book": results}
    except:
        return {"result":1}

@app.route('/book/<int:id>', methods=["DELETE"])
def delete_book(id):
    book = Book.query.get(id)
    try:
        db.session.delete(book)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@app.route('/order_items', methods=["GET", "POST"])
def handle_order_items():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            count=0
            for item in data:
                order_item = OrderItem(order_id=int(item['order_id']), quantity=int(item['quantity']),
                              cost=float(item['cost']), book_id=int(item['book_id']))
                try:
                    db.session.add(order_item)
                    db.session.commit()
                    order = order_item.order
                    order.total += order_item.cost
                    db.session.commit()
                    count=count+1
                except:
                    return {"result": 1, "error": "ошибка добавления"}
            if(count==len(data)):
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


@app.route('/order_item/<int:id>', methods=["GET"])
def get_order_item(id):
    order_item = OrderItem.query.get(id)
    results = {
        "order_id": order_item.order_id,
        "cost": order_item.cost,
        "book_id": order_item.book_id,
        "quantity": order_item.quantity
    }
    return {"order_item": results}


@app.route('/order_item/<int:id>', methods=["DELETE"])
def delete_order_item(id):
    order_item = OrderItem.query.get(id)
    try:
        db.session.delete(order_item)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@app.route('/order_item/<int:id>', methods=["PUT"])
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
        order.total=sum
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@app.route('/test', methods=["GET"])
def test():
    bookInfo = db.session.query(Book.title, Book.price, Author.name, Author.surname).join(Author).join(Genre).join(Publisher).all()

    return "0"


@app.route('/orders', methods=["GET", "POST"])
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


@app.route('/order/<int:id>', methods=["DELETE"])
def delete_order(id):
    order = Order.query.get(id)
    try:
        db.session.delete(order)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@app.route('/order/<int:id>', methods=["PUT"])
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


@app.route('/order/<int:id>', methods=["GET"])
def get_order(id):
    order = Order.query.get(id)
    results = {
        "user_id": order.user_id,
        "total": order.total,
        "date": order.date
    }
    return {"order": results}


@app.route('/authors', methods=["GET", "POST"])
def handle_authors():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            author = Author(name=data['name'], surname=data['surname'], patronymic=data['patronymic'])
            try:
                db.session.add(author)
                db.session.commit()
                return {"result": 0, "msg":f"author {author} успешно добавлен"}
            except:
                return {"result": 1, "error":"ошибка добавления"}
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


@app.route('/author/<int:id>', methods=["DELETE"])
def delete_author(id):
    author = Author.query.get(id)
    try:
        db.session.delete(author)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}



@app.route('/author/<int:id>', methods=["PUT"])
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


@app.route('/author/<int:id>', methods=["GET"])
def get_author(id):
    author = Author.query.get(id)
    results = {
        "name": author.name,
        "surname": author.surname,
        "patronymic": author.patronymic
    }
    return {"author": results}


@app.route('/publishers', methods=["GET", "POST"])
def handle_publishers():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            publisher = Publisher(publisher_name=data['publisher_name'])
            try:
                db.session.add(publisher)
                db.session.commit()
                return {"result": 0, "msg":f"publisher {publisher} успешно добавлен"}
            except:
                return {"result": 1, "error":"ошибка добавления"}
        else:
            return {"error": "The request payload is not in JSON format"}
    else:
        publishers = Publisher.query.all()
        results = [
            {
                "publisher_name": publisher.publisher_name
            } for publisher in publishers]
        return {"coutn": len(results), "publishers": results}


@app.route('/publisher/<int:id>', methods=["DELETE"])
def delete_publisher(id):
    publisher = Publisher.query.get(id)
    try:
        db.session.delete(publisher)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@app.route('/publisher/<int:id>', methods=["PUT"])
def update_publisher(id):
    publisher = Publisher.query.get(id)
    data = request.get_json()
    publisher.publisher_name = data['publisher_name']
    try:
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@app.route('/publisher/<int:id>', methods=["GET"])
def get_publisher(id):
    publisher = Publisher.query.get(id)
    results = {
        "publisher_name": publisher.publisher_name
    }
    return {"publisher_name": results}


@app.route('/users', methods=["GET", "POST"])
def handle_users():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            user = User(username=data['username'], name=data['name'], surname=data['surname'], patronymic=data['patronymic'], email=data['email'], password=data['password'])
            try:
                db.session.add(user)
                db.session.commit()
                return {"result": 0, "msg":f"user {user} успешно добавлен"}
            except:
                return {"result": 1, "error":"ошибка добавления"}
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


@app.route('/user/<int:id>', methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


@app.route('/user/<int:id>', methods=["PUT"])
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


@app.route('/user/<int:id>', methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    results = {
        "name": user.name,
        "surname": user.surname,
        "patronymic": user.patronymic,
        "username": user.username,
        "email": user.email
    }
    return {"user": results}


@app.route('/', methods=["GET"])
def home():
    books = db.session.query(Book.id, Book.title, Book.price, Author.name, Author.surname).join(Author).all()
    return render_template("home.html", books=books)


@app.route('/search', methods=["GET"])
def search():
    search = request.args.get('search')
    books = db.session.query(Book.id, Book.title, Book.price, Author.name, Author.surname).join(Author).\
        filter(or_(Book.title.like(search), Author.name.like(search), Author.surname.like(search),\
                   Author.patronymic.like(search))).all()
    return render_template("home.html", books=books)


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
        return render_template("auth.html")


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
    return 'dsda'


@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return "вы вышли"



if __name__ == "__main__":
    app.run(debug=True)
