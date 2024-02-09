from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
import os

## Foreign Key Snippet
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id				= db.Column(db.Integer, primary_key=True)
    first_name		= db.Column(db.String(64), nullable=False)
    last_name		= db.Column(db.String(64), nullable=False)
    email			= db.Column(db.String(64), nullable=False)
    contact_phone	= db.Column(db.String(64), nullable=True)
    
    libraries		= db.relationship("Library", cascade="all, delete-orphan", back_populates="owner")
    books			= db.relationship("Book", back_populates="borrower")


class Library(db.Model):
    id				= db.Column(db.Integer, primary_key=True)
    name			= db.Column(db.String(64), nullable=False)
    address_line_1	= db.Column(db.String(64), nullable=True)
    address_line_2	= db.Column(db.String(64), nullable=True)
    city			= db.Column(db.String(64), nullable=True)
    country			= db.Column(db.String(64), nullable=True)
    postal_code		= db.Column(db.String(64), nullable=True)
    contact_email	= db.Column(db.String(64), nullable=True)
    contact_phone	= db.Column(db.String(64), nullable=True)
    
    owner_id		= db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    owner			= db.relationship("User", back_populates="libraries")
    books			= db.relationship("Book", cascade="all, delete-orphan", back_populates="library")


class Book(db.Model):
    id				= db.Column(db.Integer, primary_key=True)
    status			= db.Column(db.Integer, nullable=False)
    notes			= db.Column(db.String(64), nullable=True)
    condition		= db.Column(db.String(64), nullable=True)
    validity_start	= db.Column(db.DateTime, nullable=True)
    validity_end	= db.Column(db.DateTime, nullable=True)
    
    work_id			= db.Column(db.Integer, db.ForeignKey("work.id"), nullable=False)
    library_id		= db.Column(db.Integer, db.ForeignKey("library.id"), nullable=False)
    borrower_id		= db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    
    work			= db.relationship("Work", back_populates="books")
    library			= db.relationship("Library", back_populates="books")
    borrower		= db.relationship("User", back_populates="books")


class Work(db.Model):
    id				= db.Column(db.Integer, primary_key=True)
    title			= db.Column(db.String(64), nullable=False)
    author			= db.Column(db.String(64), nullable=False)
    cover			= db.Column(db.String(64), nullable=True)
    isbn			= db.Column(db.String(64), nullable=True)
    
    books			= db.relationship("Book", back_populates="work")


@app.route("/create_main/", methods=["GET"])
def create_test():
    if os.path.exists("./instance/main.db"):
        return "main db exists", 200
    else:
        db.create_all()
        db.session.commit()
        return "main db created", 200
