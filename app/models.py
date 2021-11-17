from sqlalchemy import exc
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta, datetime

from app import db
import errors


class BaseModelMixin:

    @classmethod
    def by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        if obj:
            return obj
        else:
            raise errors.NotFound

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadRequest

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(512))
    ads = db.relationship('Ads', backref='owner')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.hash(password)

    def get_token(self, expire_time=1):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password_hash):
            raise errors.AuthError
        return user

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username
        }


class Ads(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(124), nullable=False)
    description = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=1)

    def __repr__(self):
        return '<Advert {}>'.format(self.title)
