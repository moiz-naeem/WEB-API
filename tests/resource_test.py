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
