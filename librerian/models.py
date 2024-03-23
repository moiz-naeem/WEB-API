"""
Database models and database related helpers

Classes:
    User : Model
    Library : Model
    Book : Model
    Work : Model

Functions:
    init_db_command
    empty_db_command
    random_string
    random_user
    random_library
    random_book
    random_work
    generate_db_command
"""
from datetime import datetime
import click
from flask.cli import with_appcontext
from librerian import db

class User(db.Model):
    """
    User database model

    Methods:
        serialize
        deserialize
    """
    id              = db.Column(db.Integer, primary_key=True)
    handle          = db.Column(db.String(64), nullable=False, unique=True)
    first_name      = db.Column(db.String(64), nullable=True)
    last_name       = db.Column(db.String(64), nullable=True)
    email           = db.Column(db.String(64), nullable=False, unique=True)
    contact_phone   = db.Column(db.String(64), nullable=True)
    libraries       = db.relationship("Library", cascade="all, delete-orphan", back_populates="owner")
    books           = db.relationship("Book", back_populates="borrower")

    def __repr__(self):
        return f"User {self.first_name} {self.last_name} <{self.id}>"

    def serialize(self, short_form=False):
        """
        Serialize user and user libraries into json

        Parameters:
            short_form : bool
                default : False
                if true, serialize only user information 
        """
        serialized_data = {
            "handle": self.handle,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "contact_phone": self.contact_phone
        }
        if not short_form:
            libraries_serialized = []
            for library in self.libraries:
                libraries_serialized.append(library.serialize(short_form=True))
            serialized_data["libraries"] = libraries_serialized
            books_serialized = []
            for book in self.books:
                books_serialized.append(book.serialize(short_form=True))
            serialized_data["books"] = books_serialized
        return serialized_data

    def deserialize(self, doc):
        """
        Deserialize user from json

        Parameters:
            doc : json dict
        """
        self.handle = doc["handle"]
        self.first_name = doc.get("first_name")
        self.last_name = doc.get("last_name")
        self.email = doc["email"]
        self.contact_phone = doc.get("contact_phone")

class Library(db.Model):
    """
    Library database model

    Methods:
        serialize
        deserialize
    """
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(64), nullable=False, unique=True)
    address_line_1  = db.Column(db.String(64), nullable=True)
    address_line_2  = db.Column(db.String(64), nullable=True)
    city            = db.Column(db.String(2), nullable=True)
    country         = db.Column(db.String(64), nullable=True)
    postal_code     = db.Column(db.String(64), nullable=True)
    contact_email   = db.Column(db.String(64), nullable=True)
    owner_id        = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    owner           = db.relationship("User", back_populates="libraries")
    books           = db.relationship("Book", cascade="all, delete-orphan", back_populates="library")

    def __repr__(self):
        return f"Library {self.name} <{self.id}>"

    def serialize(self, short_form=False):
        """
        Serialize library and books in library into json

        Parameters:
        short_form : bool
            default : False
            if true, serialize only library information 
        """
        serialized_data = {
            "name": self.name,
            "address_line_1": self.address_line_1,
            "address_line_2": self.address_line_2,
            "city": self.city,
            "country": self.country,
            "postal_code": self.postal_code,
            "contact_email": self.contact_email,
        }
        if not short_form:
            books_serialized = []
            for book in self.books:
                books_serialized.append(book.serialize(True))
            serialized_data["books"] = books_serialized
        return serialized_data

    def deserialize(self, doc):
        """
        Deserilize library from json dict
        
        Parameters:
            doc : json dict
        """
        self.name = doc["name"]
        self.address_line_1 = doc.get("address_line_1")
        self.address_line_2 = doc.get("address_line_2")
        self.city = doc.get("city")
        self.country = doc.get("country")
        self.postal_code = doc.get("postal_code")
        self.contact_email = doc.get("contact_email")


class Book(db.Model):
    """
    Book database model

    Methods:
        serialize
        deserialize
    """
    id              = db.Column(db.Integer, primary_key=True)
    status          = db.Column(db.Integer, nullable=False)
    notes           = db.Column(db.String(64), nullable=True)
    condition       = db.Column(db.String(64), nullable=True)
    validity_start  = db.Column(db.DateTime, nullable=True)
    validity_end    = db.Column(db.DateTime, nullable=True)
    work_id         = db.Column(db.Integer, db.ForeignKey("work.id"), nullable=False)
    library_id      = db.Column(db.Integer, db.ForeignKey("library.id"), nullable=False)
    borrower_id     = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    work            = db.relationship("Work", back_populates="books")
    library         = db.relationship("Library", back_populates="books")
    borrower        = db.relationship("User", back_populates="books")

    def __repr__(self):
        return f"Book {self.work.title} <{self.id}>"

    def serialize(self, _short_form=False):
        """
        Serialize book into json

        Parameters:
        short_form : bool
            default : False
            currently unused
        """
        serialized_data = {
            "status": self.status,
            "notes": self.notes,
            "condition": self.condition,
            "validity_start": self.validity_start,
            "validity_end": self.validity_end,
            "work_id": self.work_id
        }
        return serialized_data

    def deserialize(self, doc):
        """
        Deserialize book from doc
        """
        self.status = int(doc["status"])
        self.notes = doc.get("notes")
        self.condition = doc.get("condition")
        if "validity_start" in doc:
            self.validity_start = datetime.fromisoformat(doc.get("validity_start"))
        else:
            self.validity_start = None
        if "validity_end" in doc:
            self.validity_end = datetime.fromisoformat(doc.get("validity_end"))
        else:
            self.validity_end = None
        self.work_id = int(doc["work_id"])

        return schema

class Work(db.Model):
    """
    Work database model

    Methods:
        serialize
        deserialize
    """
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(64), nullable=False)
    author          = db.Column(db.String(64), nullable=False)
    cover           = db.Column(db.String(64), nullable=True)
    isbn            = db.Column(db.String(64), nullable=True)
    books           = db.relationship("Book", back_populates="work")

    def __repr__(self):
        return f"Work {self.title} <{self.id}>"

    def serialize(self, _short_form=False):
        """
        Serialize work into json

        Parameters:
        short_form : bool
            default : False
            currently unused
        """
        serialized_data = {
            "title": self.title,
            "author": self.author,
            "cover": self.cover,
            "isbn": self.isbn
        }
        return serialized_data

    def deserialize(self, doc):
        """
        Deserialize book from doc
        """
        self.title = doc["title"]
        self.author = doc["author"]
        self.cover = doc.get("cover")
        self.isbn = doc.get("isbn")


@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Click command for creating database tables
    """
    db.create_all()

@click.command("empty-db")
@with_appcontext
def empty_db_command():
    """
    Click command for emptying database
    Use with care
    """
    Work.query.delete()
    Book.query.delete()
    Library.query.delete()
    User.query.delete()
    db.session.commit()
    print("All db tables cleared")

def random_string(length=10):
    """
    Create random string
    
    Parameters:
        length : int
            defines length of string
    """
    import random
    import string
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def random_user():
    """
    Create random user
    No quaranteed uniqueness
    """
    first = random_string()
    last = random_string()
    user = User(
        handle=random_string(),
        first_name=first,
        last_name=last,
        email=f"{first}.{last}@{random_string(4)}.com",
    )
    return user

def random_library():
    """
    Create random library
    No quaranteed uniqueness
    """
    library = Library(
        name=random_string()
    )
    return library

def random_book():
    """
    Create random book
    No work assinged, otherwise valid
    """
    book = Book(
        status=0
    )
    return book

def random_work():
    """
    Create random work
    No quaranteed uniqueness
    """
    work = Work(
        title=random_string(),
        author=random_string()
    )
    return work


@click.command("gen-db")
@click.option("--count", default=1, type=int)
@with_appcontext
def generate_db_command(count=1):
    """
    Click command for generating database

    Parameters:
    count : int
        Defines how many items are created
    """

    for _i in range(count * 1):
        user = random_user()
        for _j in range(count * 2):
            library = random_library()
            for _k in range(count * 4):
                book = random_book()
                book.work = random_work()
                library.books.append(book)
            user.libraries.append(library)
        db.session.add(user)

    db.session.commit()
    print(f"Added {count} randomized users, {count * 2} libraries and {count * 8} books/works.")
    add_example_library()


def add_example_library():
    """
    Example users Alice and Bob, and Alice's library
    to always have one example that persists in addition to the randomized data
    """
    user = User(
            handle=f"alice123",
            first_name="Alice",
            last_name="McTest",
            email="alice.mctest@email.com",
            contact_phone= "0394111111"
        )
    db.session.add(user)
    user = User(
        handle=f"bob123",
        first_name="Bob",
        last_name="McTest",
        email="bob.mctest@email.com",
        contact_phone= "0394222222"
    )
    db.session.add(user)
    library = Library(
        owner = user,
        name=f"Alice's library",
        address_line_1="Aliceroad 123",
        address_line_2="PO123",
        city=f"Aliceland",
        country="AL",
        postal_code="99999",
        contact_email=f"info@alices.library.com"
    )
    db.session.add(library)
    work = Work(
        title = "Alice's stories",
        author="Alice McTest",
        cover=f"978-4-7659-7000-1.jpg",
        isbn=f"978-4-7659-7000-1"
    )
    db.session.add(work)
    book = Book(
        status = 1,
        notes="Signed by author on the inside front cover",
        condition="Like new",
        #TODO date checks
        #validity_start= datetime.now(), #datetime.date(2024, 1, 1),
        #validity_end = datetime.now(),
        library = library,
        work = work,
        borrower_id = user.handle
    )
    db.session.add(book)
    db.session.commit()
    print("Added example: Alice's library")
