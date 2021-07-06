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
        "user_id": {"type":["number","string"]},
        "total": {"type": "number"},
        "date": {"type": "string",
                 "format": "date"
                 },
    },
    "required": ["user_id", "total", "date"]
}

order_item_schema = {
    "type": "array",
    "properties": {
        "order_id": {"type": "number"},
        "quantity": {"type": "number"},
        "cost": {"type": "number"},
        "book_id": {"type": "number"}
    },
    "required": ["order_id", "quantity", "cost", "book_id"]
}

edit_order_item_schema = {
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
                  "pattern": "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$"
                  },
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
        "price": {"type": ["string", "number"],
                  "pattern": "^[0-9]*$"},
        "number_of_pages": {"type": ["string", "number"],
                            "pattern": "^[0-9]*$"},
        "year": {"type": ["string", "number"],
                 "pattern": "^[0-9]*$"},
        "isbn": {"type": "string"},
        "cover_type": {"type": ["string", "boolean"]},
        "annotation": {"type": "string",
                       "minLength": 10,
                       "maxLength": 500
                       },
        "slug": {"type": "string",
                 "minLength": 2,
                 "maxLength": 30
                 },
        "genre_id": {"type": ["string", "number"],
                     "pattern": "^[0-9]*$"},
        "publisher_id": {"type": ["string", "number"],
                         "pattern": "^[0-9]*$"},
        "author_id": {"type": ["string", "number"],
                      "pattern": "^[0-9]*$"}
    },
    "required": ["title", "price", "number_of_pages", "year", "isbn", "cover_type", "annotation", "slug", "genre_id",
                 "publisher_id", "author_id"]
}
