import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from librerian.models import User
from librerian import db

class UserCollection(Resource):
    
    def get(self):
        return "User Placeholder GET", 200
    def post(self):
        pass

class UserItem(Resource):
    def get(self, user):
        pass
    def put(self, user):
        pass
    def delete(self, user):
        pass