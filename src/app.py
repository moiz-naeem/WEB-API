from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json
#from sqlalchemy.exc import IntegrityError
#from sqlalchemy.engine import Engine
#from sqlalchemy import event

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=True)
    libraries = db.relationship("Library", back_populates="owner")

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=True)
    address_line_1 = db.Column(db.String(128), nullable=True)
    address_line_2 = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    country = db.Column(db.String(2), nullable=True)
    postal_code = db.Column(db.String(16), nullable=True)
    contact_email = db.Column(db.String(128), nullable=True)
    contact_phone = db.Column(db.String(16), nullable=True)    
    owner = db.relationship("User", back_populates="libraries")
    book_statuses = db.relationship("BookStatus", back_populates="status")

class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    cover = db.Column(db.String(64), nullable=True) # where to find the cover image file
    books = db.relationship("Book")

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work = db.relationship("Work", back_populates="books")
    book_statuses = db.relationship("BookStatus", back_populates="status")

class BookStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    validity_start = db.Column(db.DateTime, nullable=False)
    validity_end = db.Column(db.DateTime, nullable=True)
    book = db.relationship("Book", back_populates="book_statuses")
    library = db.relationship("Library", back_populates="book_statuses")
    status = db.relationship("Status", back_populates="book_statuses")

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=True)
    description = db.Column(db.String(128), nullable=True)
    book_statuses = db.relationship("BookStatus", back_populates="status")


@app.route("/test/", methods=["GET"])
def test():
	db.create_all()
	db.session.commit()
	return "test"