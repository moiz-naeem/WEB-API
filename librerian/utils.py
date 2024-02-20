import json
import secrets
from flask import Response, request, url_for
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.routing import BaseConverter

#converters etc
from librerian.models import *

class UserConverter(BaseConverter):
    def to_python(self, user):
        pass
    def to_url(self, db_user):
        pass

class LibraryConverter(BaseConverter):
    def to_python(self, library):
        pass
    def to_url(self, db_library):
        pass

class BookConverter(BaseConverter):
    def to_python(self, book):
        pass
    def to_url(self, db_book):
        pass
