from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))
    first_name = db.Column(db.String(120))
    notes = db.relationship('Note')


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(120), unique=False, nullable=False)
    translation = db.Column(db.String(120))
    sentence = db.Column(db.String(1000))
    part_of_speech = db.Column(db.String(120))
    difficulty = db.Column(db.String(120))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
