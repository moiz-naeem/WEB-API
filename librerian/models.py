# Database modesl for app
from app import app, db

class User(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    first_name      = db.Column(db.String(64), nullable=False)
    last_name       = db.Column(db.String(64), nullable=False)
    email           = db.Column(db.String(64), nullable=False, unique=True)
    contact_phone   = db.Column(db.String(64), nullable=True)
    
    libraries       = db.relationship("Library", cascade="all, delete-orphan", back_populates="owner")
    books           = db.relationship("Book", back_populates="borrower")

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
            "required": ["first_name", "last_name", "email"],
            "properties": {
                "first_name": {
                    "description": "First name of the user",
                    "type": "string"
                },
                "last_name" : {
                    "description": "Last name of the user",
                    "type": "string"
                },
                "email": {
                    "description": "Email address of the user",
                    "type": "string",
                    "format": "email"
                }
            }
        }
        return schema

class Library(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(64), nullable=False)
    address_line_1  = db.Column(db.String(64), nullable=True)
    address_line_2  = db.Column(db.String(64), nullable=True)
    city            = db.Column(db.String(64), nullable=True)
    country         = db.Column(db.String(64), nullable=True)
    postal_code     = db.Column(db.String(64), nullable=True)
    contact_email   = db.Column(db.String(64), nullable=True)
    contact_phone   = db.Column(db.String(64), nullable=True)
    
    owner_id        = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    owner           = db.relationship("User", back_populates="libraries")
    books           = db.relationship("Book", cascade="all, delete-orphan", back_populates="library")

    def serialize(self, short_form=False):
        serialized_data = {
            "name": self.name,
            "address_line_1": self.address_line_1,
            "address_line_2": self.address_line_2,
            "city": self.city,
            "country": self.country,
            "postal_code": self.postal_code,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone
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
        self.contact_phone = doc.get("contact_phone")

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {
                    "description": "Name of the library",
                    "type": "string"
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

    def serialize(self, short_form=False):
        serialized_data = {
            "status": self.status,
            "notes": self.notes,
            "condition": self.condition,
            "validity_start": self.validity_start,
            "validity_end": self.validity_end
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

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["status"],
            "properties": {
                "status": {
                    "description": "Status code of book, range from (0-N)",
                    "type": "int"
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
                    "type": "string"
                },
                "author": {
                    "description": "Name works author",
                    "type": "string"
                }
            }
        }
        return schema