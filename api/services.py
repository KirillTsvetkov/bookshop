from models import db, Book, Order, OrderItem, Author, Genre, Publisher, User
from libs.util import sqla2dict, checkValues


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
    except Exception as error:
        return {"result": 1, "error": str(error.orig)}


def get_books():
    books = db.session.query(Book)
    return [sqla2dict(i) for i in books]


def del_book(id):
    book = Book.query.get(id)
    try:
        db.session.delete(book)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


def create_book(data):
    book = Book(title=data['title'],
                price=float(data['price']), number_of_pages=int(data['number_of_pages']),
                year=int(data['year']), isbn=data['isbn'],
                cover_type=bool(data['cover_type']),
                annotation=data['annotation'], slug=data['slug'],
                genre_id=int(data['genre_id']), publisher_id=int(data['publisher_id']),
                author_id=int(data['author_id']))
    try:
        db.session.add(book)
        db.session.commit()
        return {"result": 0, "msg": f"book {book} успешно добавлен"}
    except Exception as error:
        return {"result": 1, "error": str(error.orig)}


def get_publisher(id):
    publisher = Publisher.query.get(id)
    return sqla2dict(publisher)

def get_publishers():
    publishers = db.session.query(Publisher)
    return [sqla2dict(i) for i in publishers]


def edit_publisher(id, data):
    check = checkValues(data)
    if check['result']:
        return check
    publisher = Publisher.query.get(id)
    publisher.publisher_name = data['publisher_name']
    try:
        db.session.commit()
        return {"result": 0}
    except Exception as error:
        return {"result": 1, "error": str(error.orig)}


def del_publisher(id):
    publisher = Publisher.query.get(id)
    try:
        db.session.delete(publisher)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


def create_publisher(data):
    check = checkValues(data)
    if check['result']:
        return check
    else:
        publisher = Publisher(publisher_name=data['publisher_name'])
        try:
            db.session.add(publisher)
            db.session.commit()
            return {"result": 0, "msg": f"publisher {publisher} успешно добавлен"}
        except Exception as error:
            return {"result": 1, "error": str(error.orig)}


def get_user(id):
    user = User.query.get(id)
    return sqla2dict(user)


def get_users():
    users = db.session.query(User)
    return [sqla2dict(i) for i in users]


def edit_user(id, data):
    check = checkValues(data)
    if check['result']:
        return check
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
    except Exception as error:
        return {"result": 1, "error": str(error.orig)}


def del_user(id):
    user = User.query.get(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


def create_user(data):
    check = checkValues(data)
    if check['result']:
        return check
    username = data['username']
    name = data['name']
    surname = data['surname']
    patronymic = data['patronymic']
    email = data['email']
    password = data['password']
    for key, value in data.items():
        if value == "":
            return {"result": 1, "error": "Поле " + key + " должно быть заполнено"}
    user = User(username=username, name=name, surname=surname,
                patronymic=patronymic, email=email, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        return {"result": 0, "msg": f"user {user} успешно добавлен"}
    except Exception as error:
        return {"result": 1, "error": str(error.orig)}


def get_genre(id):
    genre = Genre.query.get(id)
    return sqla2dict(genre)


def get_genres():
    genres = db.session.query(Genre)
    return [sqla2dict(i) for i in genres]


def edit_genre(id, data):
    check = checkValues(data)
    if check['result']:
        return check
    genre = Genre.query.get(id)
    genre.genre_name = data['genre_name']
    try:
        db.session.commit()
        results = {
            "genre_name": genre.genre_name
        }
        return {"result": 0, "genre": results}
    except Exception as error:
        return {"result": 1, "error": str(error.orig)}


def del_genre(id):
    genre = Genre.query.get(id)
    try:
        db.session.delete(genre)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


def create_genre(data):
    check = checkValues(data)
    if check['result']:
        return check
    genre = Genre(genre_name=data['genre_name'])
    for key, value in data.items():
        if value == "":
            return {"result": 1, "error": "Поле " + key + " должно быть заполнено"}
    try:
        db.session.add(genre)
        db.session.commit()
        return {"result": 0, "msg": f"genre {genre} успешно добавлен"}
    except Exception as error:
        return {"result": 1, "error": str(error.orig)}


def get_author(id):
    author = Author.query.get(id)
    return sqla2dict(author)


def get_authors():
    authors = db.session.query(Author)
    return [sqla2dict(i) for i in authors]


def edit_author(id, data):
    name = data['name']
    if name == '':
        return {"result": 1, "error": "Имя автора не должно быть пустым"}
    author = Author.query.get(id)
    author.name = data['name']
    author.surname = data['surname']
    author.patronymic = data['patronymic']
    try:
        db.session.commit()
        return {"result": 0}
    except Exception as error:
        return {"result": 1, "error": str(error.orig)}


def del_author(id):
    author = Author.query.get(id)
    try:
        db.session.delete(author)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


def create_author(data):
    name = data['name']
    surname = data.get('surname', None)
    patronymic = data.get('patronymic', None)
    author = Author(name=name, surname=surname, patronymic=patronymic)
    try:
        db.session.add(author)
        db.session.commit()
        return {"result": 0, "msg": f"author {author} успешно добавлен"}
    except Exception as error:
        return {"result": 1, "error": str(error.orig)}


def get_order(id):
    order = Order.query.get(id)
    return sqla2dict(order)


def get_orders():
    orders = db.session.query(Order)
    return [sqla2dict(i) for i in orders]


def edit_order(id, data):
    check = checkValues(data)
    if check['result']:
        return check
    order = Order.query.get(id)
    order.user_id = data['user_id']
    order.total = data['total']
    order.date = data['date']
    try:
        db.session.commit()
        return {"result": 0}
    except Exception as error:
        return {"result": 1, "error": str(error.orig)}


def del_order(id):
    order = Order.query.get(id)
    try:
        db.session.delete(order)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


def create_order(data):
    check = checkValues(data)
    if check['result']:
        return check
    order = Order(user_id=data['user_id'], date=data['date'], total=data['total'])
    try:
        db.session.add(order)
        db.session.commit()
        return {"result": 0, "msg": f"order {order} успешно добавлен"}
    except Exception as error:
        return {"result": 1, "error": str(error.orig)}


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
        order_itemslist = OrderItem.all_items_in_order(order)
        sum = 0
        for item in order_itemslist:
            sum += item.cost
        order.total = sum
        db.session.commit()
        return {"result": 0}
    except Exception as error:
        return {"result": 1, "error": str(error.orig)}


def del_order_item(id):
    order_item = OrderItem.query.get(id)
    try:
        db.session.delete(order_item)
        db.session.commit()
        return {"result": 0}
    except:
        return {"result": 1}


def create_orderitems(data):
    count = 0
    for item in data:
        order_item = OrderItem(order_id=int(item['order_id']), quantity=int(item['quantity']),
                               cost=float(item['cost']), book_id=int(item['book_id']))
        try:
            db.session.add(order_item)
            db.session.commit()
            order = order_item.order
            order.total += order_item.cost
            db.session.commit()
            count = count + 1
        except Exception as error:
            return {"result": 1, "error": str(error.orig)}
    if (count == len(data)):
        return {"result": 0, "msg": 'Добавленно "+str(count)+" Записей"'}