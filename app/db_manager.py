from app.db import db
from app.models import User


def select_user(user_id=None, password=None, scalar=False):
    qs = db.session.query(User)

    if user_id:
        qs = qs.filter(User.user_id == user_id)

    if password:
        qs = qs.filter(User.password == password)

    if scalar:
        return qs.scalar()

    return qs.all()


def insert_user(**kwargs):
    user = User()

    for k, v in kwargs.items():
        setattr(user, k, v)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()






