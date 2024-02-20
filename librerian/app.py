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

from models import User, Library, Book, Work

@app.route("/create_main/", methods=["GET"])
def create_test():
    if os.path.exists("./instance/main.db"):
        return "main db exists", 200
    else:
        db.create_all()
        db.session.commit()
        return "main db created", 200
