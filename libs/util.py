def sqla2dict(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}