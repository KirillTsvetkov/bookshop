from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import LoginManager, UserMixin
import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/bookshop'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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
    book=data['isbn']
    book.cover_type=data['cover_type']
    book.annotation=data['annotation']
    book.slug=data['slug']
    book.genre_id=data['genre_id']
    book.publisher_id=data['publisher_id']
    book.author_id=data['author_id']
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

    return {"book": results}


@app.route('/books', methods=["GET"])
def get_books():
    books = Book.query.all()
    results = [
        {
            "title": book.title,
            "price": book.price
        } for book in books]

    return {"coutn": len(results), "books": results}


@app.route('/authors', methods=["GET", "POST"])
def handle_authors():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            author = Author(name=data['name'], surname=data['surname'], patronymic=data['patronymic'])
            try:
                db.session.add(author)
                db.session.commit()
                return {"msg":f"author {author} успешно добавлен"}
            except:
                return {"error":"ошибка добавления"}
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


@app.route('/genres', methods=["GET", "POST"])
def handle_genres():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            genre = Genre(genre_name=data['genre_name'])
            try:
                db.session.add(genre)
                db.session.commit()
                return {"msg":f"genre {genre} успешно добавлен"}
            except:
                return {"error":"ошибка добавления"}
        else:
            return {"error": "The request payload is not in JSON format"}
    else:
        genres = Genre.query.all()
        results = [
            {
                "genre_name": genre.genre_name
            } for genre in genres]
        return {"coutn": len(results), "genres": results}


@app.route('/publishers', methods=["GET", "POST"])
def handle_publishers():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            publisher = Publisher(publisher_name=data['publisher_name'])
            try:
                db.session.add(publisher)
                db.session.commit()
                return {"msg":f"publisher {publisher} успешно добавлен"}
            except:
                return {"error":"ошибка добавления"}
        else:
            return {"error": "The request payload is not in JSON format"}
    else:
        publishers = Publisher.query.all()
        results = [
            {
                "publisher_name": publisher.publisher_name
            } for publisher in publishers]
        return {"coutn": len(results), "publishers": results}



@app.route('/users', methods=["GET", "POST"])
def handle_users():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            user = User(username=data['username'], name=data['name'], surname=data['surname'], patronymic=data['patronymic'], email=data['email'], password=data['password'])
            try:
                db.session.add(user)
                db.session.commit()
                return {"msg":f"user {user} успешно добавлен"}
            except:
                return {"error":"ошибка добавления"}
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



@app.route('/books', methods=["GET", "POST"])
def handle_books():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            book = Book(title = data['title'],
                        price=float(data['price']), number_of_pages=data['number_of_pages'],
                        year=data['year'], isbn=data['isbn'],
                        cover_type=data['cover_type'],
                        annotation=data['annotation'], slug=data['slug'],
                        genre_id=data['genre_id'], publisher_id=data['publisher_id'],
                        author_id=data['author_id'])
            print(book.title, book.price)
            try:
                db.session.add(book)
                db.session.commit()
                return {"msg":f"book {book} успешно добавлен"}
            except:
                return {"error":"ошибка добавления"}
        else:
            return {"error": "The request payload is not in JSON format"}
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




if __name__ == "__main__":
    app.run(debug=True)
