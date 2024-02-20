import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from librerian.models import Work
from librerian import db

class WorkCollection(Resource):
    
    def get(self):
        pass
    def post(self):
        pass

class WorkItem(Resource):
    def get(self, work):
        pass
    def put(self, work):
        pass
    def delete(self, work):
        pass