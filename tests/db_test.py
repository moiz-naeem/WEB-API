import os
import pytest
import tempfile
import time
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

from librerian import create_app, db
from librerian.models import User, Library, Book, Work

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def app():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    
    app = create_app(config)
    
    with app.app_context():
        db.create_all()
        yield app
    
    os.close(db_fd)
    os.unlink(db_fname)

def _get_user(handle="matmei", first_name="Matti", last_name="Meikalainen"):
    return User(
        handle=handle,
        first_name=first_name,
        last_name=last_name,
        email="{}.{}@email.com".format(first_name, last_name)
    )

def _get_library(name="Kirjahylly"):
    return Library(
        name=name,
        address_line_1="foobar",
    )

def _get_work(title="Crime And Punishment", author="Fyodor Dostoevsky"):
    return Work(
        title=title,
        author=author,
        cover=None,
        isbn=None
    )

def _get_book(status=0):
    return Book(
        status=status,
        notes="This is a book",
        condition="Very Good",
        validity_start=datetime.now(),
        validity_end=datetime.now()
    )

def test_create_instances(app):
    """
    Tests that we can create one instance of each model and save them to the
    database using valid values for all columns. After creation, test that 
    everything can be found from database, and that all relationships have been
    saved correctly.
    """

    # Create everything
    user = _get_user()
    library = _get_library()
    book = _get_book()
    work = _get_work()

    library.owner = user
    book.library = library
    book.work = work
    book.borrower = user

    db.session.add(user)
    db.session.add(library)
    db.session.add(book)
    db.session.add(work)
    db.session.commit()
    
    # Check that everything exists
    assert User.query.count() == 1
    assert Library.query.count() == 1
    assert Book.query.count() == 1
    assert Work.query.count() == 1
    db_user = User.query.first()
    db_library = Library.query.first()
    db_book = Book.query.first()
    db_work = Work.query.first()
    
    # Check all relationships (both sides)
    assert db_book.borrower == db_user
    assert db_book in db_user.books
    assert db_book.work == db_work
    assert db_book in db_work.books
    assert db_book.library == db_library
    assert db_book in db_library.books
    assert db_library.owner == db_user
    assert db_library in db_user.libraries

def test_delete_instances(app):
    """
    Test delete cascade rules
        library deletions cascade into books
        user deletions cascased into libraries
    """
    user = _get_user()
    library = _get_library()
    book = _get_book()
    work = _get_work()
    
    library.owner = user
    book.library = library
    book.work = work
    book.borrower = user
    
    db.session.add(user)
    db.session.add(library)
    db.session.add(book)
    db.session.add(work)

    db.session.commit()
    db.session.delete(library)
    db.session.commit()
    
    assert User.query.count() == 1
    assert Library.query.count() == 0
    assert Book.query.count() == 0
    assert Work.query.count() == 1

    library = _get_library()
    book = _get_book()

    library.owner = user
    book.library = library
    book.work = work
    book.borrower = user

    db.session.add(library)
    db.session.add(book)

    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    
    assert User.query.count() == 0
    assert Library.query.count() == 0
    assert Book.query.count() == 0
    assert Work.query.count() == 1

def test_user_columns(app):
    """
    Tests user columns' restrictions
        first_name is not null
        last_name is not null
        email is unique
    """
    user1 = _get_user()
    user2 = _get_user()
    db.session.add(user1)
    db.session.add(user2)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()
    
    user1.handle = None
    db.session.add(user1)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

def test_work_columns(app):
    """
    Tests work columns' restrictions
        title is not null
        author is not null
    """
    work = _get_work()
    work.title = None
    db.session.add(work)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

    work = _get_work()
    work.author = None
    db.session.add(work)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

def test_book_columns(app):
    """
    Tests work columns' restrictions
        status is not null
        work_id is not null
        library_id is not null
    """
    user = _get_user()
    library = _get_library()
    book = _get_book(status=None)
    work = _get_work()
    library.owner = user
    book.library = library
    book.work = work
    db.session.add(user)
    db.session.add(library)
    db.session.add(book)
    db.session.add(work)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

    user = _get_user()
    library = _get_library()
    book = _get_book()
    library.owner = user
    book.library = library
    db.session.add(user)
    db.session.add(library)
    db.session.add(book)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

    book = _get_book()
    work = _get_work()
    book.work = work
    db.session.add(book)
    db.session.add(work)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

def test_library_columns(app):
    """
    Tests library columns' restrictions
        name is not null
        owner_id is not null
    """
    user = _get_user()
    library = _get_library(name=None)
    db.session.add(user)
    db.session.add(library)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

    library = _get_library()
    db.session.add(library)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()