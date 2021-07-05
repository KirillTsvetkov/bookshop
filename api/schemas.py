publisher_schema = {
    "type": "object",
    "properties": {
        "publisher_name": {"type": "string",
                           "minLength": 2,
                           "maxLength": 50},
    },
    "required": ["publisher_name"]
}

genre_schema = {
    "type": "object",
    "properties": {
        "genre_name": {"type": "string",
                       "minLength": 3,
                       "maxLength": 50,
                       "pattern": "^[^0-9]+$"},
    },
    "required": ["genre_name"]
}

author_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string",
                 "minLength": 2,
                 "maxLength": 20,
                 "pattern": "^[^0-9]+$"
                 },
        "surname": {"type": ["string", "null"],
                    "minLength": 2,
                    "maxLength": 20,
                    "pattern": "^[^0-9]+$"
                    },
        "patronymic": {"type": ["string", "null"],
                       "minLength": 2,
                       "maxLength": 20,
                       "pattern": "^[^0-9]+$"
                       },
    },
    "required": ["name"]
}

order_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "number"},
        "total": {"type": "number"},
        "date": {"type": "string",
                 "format": "date"
                 },
    },
    "required": ["user_id", "total", "date"]
}

order_item_schema = {
    "type": "object",
    "properties": {
        "order_id": {"type": "number"},
        "quantity": {"type": "number"},
        "cost": {"type": "number"},
        "book_id": {"type": "number"}
    },
    "required": ["order_id", "quantity", "cost", "book_id"]
}

user_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string",
                     "minLength": 5,
                     "maxLength": 15},
        "name": {"type": "string",
                 "minLength": 2,
                 "maxLength": 20,
                 "pattern": "^[^0-9]+$"},
        "surname": {"type": "string",
                    "minLength": 2,
                    "maxLength": 20,
                    "pattern": "^[^0-9]+$"},
        "patronymic": {"type": "string",
                       "minLength": 2,
                       "maxLength": 20,
                       "pattern": "^[^0-9]+$"
                       },
        "email": {"type": "string",
                  "format": "email"},
        "password": {"type": "string",
                     "minLength": 3,
                     "maxLength": 25
                     }
    },
    "required": ["username", "name", "surname", "patronymic", "email", "password"]
}

book_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string",
                  "minLength": 1,
                  "maxLength": 60},
        "price": {"type": "number"},
        "number_of_pages": {"type": "number"},
        "year": {"type": "number"},
        "isbn": {"type": "string"},
        "cover_type": {"type": "bool"},
        "annotation": {"type": "string",
                       "minLength": 10,
                       "maxLength": 500
                       },
        "slug": {"type": "string",
                 "minLength": 2,
                 "maxLength": 30
                 },
        "genre_id": {"type": "number"},
        "publisher_id": {"type": "number"},
        "author_id": {"type": "number"}
    },
    "required": ["title", "price", "number_of_pages", "year", "isbn", "cover_type", "annotation", "slug", "genre_id",
                 "publisher_id", "author_id"]
}
