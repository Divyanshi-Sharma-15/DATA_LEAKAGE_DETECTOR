from Models.db import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    Lastname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    UserRole = db.Column(db.String(100))
    UserId = db.Column(db.String(100), unique=True)
    Verified = db.Column(db.String(100), default="False")
    password = db.Column(db.String(100))

    def __init__(self, firstname, Lastname, email, role, userId, password):
        self.email = email
        self.firstName = firstname
        self.Lastname = Lastname
        self.UserRole = role
        self.UserId = userId
        self.password = password


class Uploaded(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    filename = db.Column(db.String(100))

    def __init__(self, title, filename):
        self.title = title
        self.filename = filename
