import json
import secrets
from flask import Response, request, url_for
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.routing import BaseConverter
import urllib.parse as urlparse

#converters etc
from librerian.models import *

class UserConverter(BaseConverter):
    
    def to_python(self, user):
        handle = urlparse.unquote(user)
        db_user = User.query.filter_by(handle=handle).first()
        if db_user is None:
            raise NotFound
        return db_user

    def to_url(self, db_user):
        return urlparse.quote(db_user.handle, safe="")

class LibraryConverter(BaseConverter):
    
    def to_python(self, library):
        name = urlparse.unquote(library)
        db_library = Library.query.filter_by(name=name).first()
        if db_library is None:
            raise NotFound
        return db_library

    def to_url(self, db_library):
        return urlparse.quote(db_library.name, safe="")

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
