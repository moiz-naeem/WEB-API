import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from librerian.models import Book
from librerian import db

class BookCollection(Resource):
    
    def get(self):
        pass
    def post(self):
        pass

class BookItem(Resource):
    def get(self, book):
        pass
    def put(self, book):
        pass
    def delete(self, book):
        pass