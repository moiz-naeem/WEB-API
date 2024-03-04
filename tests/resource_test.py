import json
import os
import pytest
import tempfile
import time
from datetime import datetime
from flask.testing import FlaskClient
from jsonschema import validate
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError
from werkzeug.datastructures import Headers

from librerian import create_app, db
from librerian.models import User, Library, Book, Work
from librerian.models import random_string, random_book, random_library, random_user, random_work

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    app = create_app(config)
    
    with app.app_context():
        db.create_all()
        _populate_db()

    yield app.test_client()

    os.close(db_fd)
    os.unlink(db_fname)

def _populate_db():
    for i in range(4):
        user = User(
            handle=f"test-user-handle-{i}",
            first_name=f"test-user-first-name-{i}",
            last_name=f"test-user-last-name-{i}",
            email=f"test.user{i}@email.com"
        )
        db.session.add(user)
        
        library = Library(
            owner = user,
            name=f"test-library-number-{i}",
            address_line_1=f"test-library-address-{i}",
            address_line_2=f"test-library-address2-{i}",
            city=f"test-city-{i}",
            country="FI",
            postal_code=f"9999{i}",
            contact_email=f"test.user.library{i}@email.com"
        )
        db.session.add(library)
        
        # add one work without books, one that will have a book attached
        work = Work(
            title = f"test-title-no-books-{i}",
            author=f"test-author-no-books-{i}",
            cover=f"test-cover-no-books-{i}",
            isbn=f"978-4-7659-7999-{i}" #TODO isbn validation and random examples for 10 and 13 digit?
        )
        db.session.add(work)
        work = Work(
            title = f"test-title-{i}",
            author=f"test-author-{i}",
            cover=f"test-cover-{i}",
            isbn=f"0-2346-1819-{i}" #TODO isbn validation and random examples for 10 and 13 digit?
        )
        db.session.add(work)
        
        book = Book(
            status = i,
            notes=f"test-library-number-{i}",
            condition=f"test-library-address-{i}",
            #TODO date checks
            #validity_start= datetime.now(), #datetime.date(2024, 1, 1),
            #validity_end = datetime.now(),
            library = library,
            work = work
        )
        db.session.add(book)
        
    db.session.commit()

class TestUserCollection(object):

    RESOURCE_URL = "/api/users/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body["items"]) == 4
        for item in body["items"]:
            assert "handle" in item
            assert "first_name" in item
            assert "last_name" in item
            assert "email" in item
            #assert "contact_phone" in item


class TestLibraryCollection(object):

    RESOURCE_URL = "/api/libraries/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body["items"]) == 4
        for item in body["items"]:
            assert "name" in item
            assert "address_line_1" in item
            assert "address_line_2" in item
            assert "city" in item
            assert "country" in item
            assert "postal_code" in item
            assert "contact_email" in item
 
 
class TestWorkCollection(object):

    RESOURCE_URL = "/api/works/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body["items"]) == 8
        for item in body["items"]:
            assert "title" in item
            assert "author" in item
            assert "cover" in item
            assert "isbn" in item
 
 
class TestBookCollection(object):

    RESOURCE_URL = "/api/books/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body["items"]) == 4
        for item in body["items"]:
            assert "status" in item
            assert "notes" in item
            assert "condition" in item
            #assert "validity_start" in item
            #assert "validity_end" in item
            