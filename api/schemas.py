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
                       "maxLength": 50},
    },
    "required": ["genre_name"]
}

author_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string",
                 "minLength": 2,
                 "maxLength": 20
                 },
        "surname": {"type": "string",
                    "minLength": 2,
                    "maxLength": 20
                    },
        "patronymic": {"type": "string",
                       "minLength": 2,
                       "maxLength": 20
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
                       "format": "date"},
    },
    "required": ["user_id", "total", "date"]
}
