import json
import secrets
from flask import Response, request, url_for
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.routing import BaseConverter

#converters etc
from librerian.models import *

class UserConverter(BaseConverter):
    
    def to_python(self, user):
        db_user = User.query.filter_by(id=user).first()
        if db_user is None:
            raise NotFound
        return db_user

    def to_url(self, db_user):
        return str(db_user.id)

class LibraryConverter(BaseConverter):
    
    def to_python(self, library):
        db_library = Library.query.filter_by(id=library).first()
        if db_library is None:
            raise NotFound
        return db_library

    def to_url(self, db_library):
        return str(db_library.id)

class BookConverter(BaseConverter):
    def to_python(self, book):
        db_book = Book.query.filter_by(id=book).first()
        if db_book is None:
            raise NotFound
        return db_book

    def to_url(self, db_book):
        return str(db_book.id)

class WorkConverter(BaseConverter):
    def to_python(self, work):
        db_work = Work.query.filter_by(id=work).first()
        if db_work is None:
            raise NotFound
        return db_work

    def to_url(self, db_work):
        return str(db_work.id)
