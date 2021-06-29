def sqla2dict(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}


def checkValues(data):
    for key, value in data.items():
        if value == "":
            return {"result": 1, "error": "Поле " + key + " должно быть заполнено"}
    return {"result": 0}