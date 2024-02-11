import os
import pytest
import tempfile
import time
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

import app
from app import User, Library, Book, Work

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.app.config["TESTING"] = True
    
    ctx = app.app.app_context()
    ctx.push()
    app.db.create_all()
        
    yield app.db
    
    app.db.session.rollback()
    app.db.drop_all()
    app.db.session.remove()
    ctx.pop()
    os.close(db_fd)
    os.unlink(db_fname)

def _get_user(first_name="Matti", last_name="Meikalainen"):
    return User(
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

def test_create_instances(db_handle):
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

    db_handle.session.add(user)
    db_handle.session.add(library)
    db_handle.session.add(book)
    db_handle.session.add(work)
    db_handle.session.commit()
    
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

def test_delete_instance(db_handle):
    user = _get_user()
    library = _get_library()
    book = _get_book()
    work = _get_work()
    
    library.owner = user
    book.library = library
    book.work = work
    book.borrower = user
    
    db_handle.session.add(user)
    db_handle.session.add(library)
    db_handle.session.add(book)
    db_handle.session.add(work)
    
    db_handle.session.commit()
    db_handle.session.delete(work)
    
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()


def test_user_columns(db_handle):
    """
    Tests user columns' restrictions
        first_name is not null
        last_name is not null
        email is unique
    """
    user1 = _get_user()
    user2 = _get_user()
    db_handle.session.add(user1)
    db_handle.session.add(user2)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()
    
    user1.first_name = None
    user1.last_name = None
    db_handle.session.add(user1)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()

def test_work_columns(db_handle):
    """
    Tests work columns' restrictions
        title is not null
        author is not null
    """
    work = _get_work()
    work.title = None
    db_handle.session.add(work)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()

    work = _get_work()
    work.author = None
    db_handle.session.add(work)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()

def test_book_columns(db_handle):
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
    db_handle.session.add(user)
    db_handle.session.add(library)
    db_handle.session.add(book)
    db_handle.session.add(work)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()

    user = _get_user()
    library = _get_library()
    book = _get_book()
    library.owner = user
    book.library = library
    db_handle.session.add(user)
    db_handle.session.add(library)
    db_handle.session.add(book)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()


    book = _get_book()
    work = _get_work()
    book.work = work
    db_handle.session.add(book)
    db_handle.session.add(work)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()


    


def test_library_columns(db_handle):
    """
    Tests library columns' restrictions
        name is not null
        owner_id is not null
    """
    user = _get_user()
    library = _get_library(name=None)
    db_handle.session.add(user)
    db_handle.session.add(library)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()

    library = _get_library()
    db_handle.session.add(library)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()