import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from librerian.models import Library
from librerian import db

class LibraryCollection(Resource):
    
    def get(self):
        pass
    def post(self):
        pass

class LibraryItem(Resource):
    def get(self, library):
        pass
    def put(self, library):
        pass
    def delete(self, library):
        pass