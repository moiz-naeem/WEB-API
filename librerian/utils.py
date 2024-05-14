"""
Utility Functions and URI converters

Classes:
    UserConverter : BaseConverter
    LibraryConverter : BaseConverter
    BookConverter : BaseConverter
    WorkConverter : BaseConverter
"""

from urllib import parse

from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter

from librerian.models import User, Library, Book, Work

class UserConverter(BaseConverter):
    """
    URI converter for user models

    Methods:
        to_python
        to_url
    """
    def to_python(self, value):
        """
        Get model from uri
        """
        handle = parse.unquote(value)
        db_user = User.query.filter_by(handle=handle).first()
        if db_user is None:
            raise NotFound
        return db_user

    def to_url(self, value):
        """
        Get uri from model
        """
        return parse.quote(value.handle, safe="")

class LibraryConverter(BaseConverter):
    """
    URI converter for library models

    Methods:
        to_python
        to_url
    """
    def to_python(self, value):
        """
        Get model from uri
        """
        name = parse.unquote(value)
        db_library = Library.query.filter_by(name=name).first()
        if db_library is None:
            raise NotFound
        return db_library

    def to_url(self, value):
        """
        Get uri from model
        """
        return parse.quote(value.name, safe="")

class BookConverter(BaseConverter):
    """
    URI converter for book models

    Methods:
        to_python
        to_url
    """
    def to_python(self, value):
        """
        Get model from uri
        """
        db_book = Book.query.filter_by(id=value).first()
        if db_book is None:
            raise NotFound
        return db_book

    def to_url(self, value):
        """
        Get uri from model
        """
        return str(value.id)

class WorkConverter(BaseConverter):
    """
    URI converter for work models

    Methods:
        to_python
        to_url
    """
    def to_python(self, value):
        """
        Get model from uri
        """
        db_work = Work.query.filter_by(id=value).first()
        if db_work is None:
            raise NotFound
        return db_work

    def to_url(self, value):
        """
        Get uri from model
        """
        return str(value.id)
