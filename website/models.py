from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class Pendings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    uniqueID = db.Column(db.Integer, unique=True)


class Form_1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nationality = db.Column(db.String(150))
    address = db.Column(db.String(150))
    b_day = db.Column(db.String(150))
    civil_status = db.Column(db.String(150))
    education = db.Column(db.String(150))
    profession = db.Column(db.String(1500))
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    date = db.Column(db.Integer)
    items = db.Column(db.String(1500))
    assistant = db.Column(db.String(30))


class Last(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Integer)


class Cvs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    name = db.Column(db.String(1500))
    date = db.Column(db.Integer)
