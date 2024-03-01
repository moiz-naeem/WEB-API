import click
from flask.cli import with_appcontext
from librerian import db

class User(db.Model):
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
        serialized_data = {
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
        self.first_name = doc["first_name"]
        self.last_name = doc["last_name"]
        self.email = doc["email"]
        self.contact_phone = doc.get("contact_phone")

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["handle", "email"],
            "properties": {
                "handle": {
                    "description": "Handle of the user, unique to user",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                },
                "first_name": {
                    "description": "First name of the user",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                },
                "last_name": {
                    "description": "Last name of the user",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                },
                "email": {
                    "description": "Email address of the user",
                    "type": "string",
                    "format": "idn-email",
                    "minLength": 1,
                    "maxLength": 64
                },
                "contact_phone": {
                    "description": "phone number of the user",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                }
            }
        }
        return schema

class Library(db.Model):
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
                books_serialized.append(book.serialize(short_form=True))
            serialized_data["books"] = books_serialized
        return serialized_data
    
    def deserialize(self, doc):
        self.name = doc["name"]
        self.address_line_1 = doc.get("address_line_1")
        self.address_line_2 = doc.get("address_line_2")
        self.city = doc.get("city")
        self.country = doc.get("country")
        self.postal_code = doc.get("postal_code")
        self.contact_email = doc.get("contact_email")

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {
                    "description": "Name of the library",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                },
                "address_line_1": {
                    "description": "",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                },
                "address_line_2": {
                    "description": "",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                },
                "city": {
                    "description": "",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                },
                "country": {
                    "description": "",
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 2
                },
                "postal_code": {
                    "description": "",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                },
                "contact_email": {
                    "description": "",
                    "type": "string",
                    "format": "idn-email",
                    "minLength": 1,
                    "maxLength": 64
                }
            }
        }
        return schema

class Book(db.Model):
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

    def serialize(self, short_form=False):
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

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["status"],
            "properties": {
                "status": {
                    "description": "Status code of book, range from (0-N)",
                    "type": "integer",
                    "enum": [0, 1, 2, 3, 4, 5]
                },
                "notes": {
                    "description": "User defined notes for book",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                },
                "condition": {
                    "description": "",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                },
                "validity_start": {
                    "description": "Datetime when books was borrowed",
                    "type": "string",
                    "format": "date-time"
                },
                "validity_end": {
                    "description": "Datetime when book is due",
                    "type": "string",
                    "format": "date-time"
                },
                "work_id": {
                    "description": "ID of work that book is instance of",
                    "type": "integer"
                }
            }
        }
        return schema

class Work(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(64), nullable=False)
    author          = db.Column(db.String(64), nullable=False)
    cover           = db.Column(db.String(64), nullable=True)
    isbn            = db.Column(db.String(64), nullable=True)
    
    books           = db.relationship("Book", back_populates="work")

    def __repr__(self):
        return f"Work {self.title} <{self.id}>"

    def serialize(self, short_form=False):
        serialized_data = {
            "title": self.title,
            "author": self.author,
            "cover": self.cover,
            "isbn": self.isbn
        }
        return serialized_data

    def deserialize(self, doc):
        self.title = doc["title"]
        self.author = doc["author"]
        self.cover = doc.get("cover")
        self.isbn = doc.get("isbn")

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["title", "author"],
            "properties": {
                "title": {
                    "description": "Title of work",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                },
                "author": {
                    "description": "Name works author",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                },
                "cover": {
                    "description": "URI to cover of the work",
                    "type": "string",
                    "format": "uri",
                    "minLength": 1,
                    "maxLength": 64
                },
                "isbn": {
                    "description": "ISBN of the work",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                }
            }
        }
        return schema

@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()

@click.command("nuke-db")
@with_appcontext
def nuke():
    Work.query.delete()
    Book.query.delete()
    Library.query.delete()
    User.query.delete()
    db.session.commit()
    print("All db tables cleared")
    pass

def random_string(length=10):
    import random, string
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def random_user():
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
    library = Library(
        name=random_string()
    )
    return library

def random_book():
    book = Book(
        status=0
    )
    return book

def random_work():
    work = Work(
        title=random_string(),
        author=random_string()
    )
    return work


@click.command("gen-db")
@click.option("--count", default=1, type=int)
@with_appcontext
def generate_db_command(count=1):
    import datetime
    import random

    for i in range(count * 1):
        user = random_user()
        for j in range(count * 2):
            library = random_library()
            for k in range(count * 4):
                book = random_book()
                book.work = random_work()
                library.books.append(book)
            user.libraries.append(library)
        db.session.add(user)
    
    db.session.commit()
    print(f"Added {count} users, {count * 2} libraries and {count * 8} books/works.")