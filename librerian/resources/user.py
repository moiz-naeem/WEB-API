import json
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType

from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from librerian.models import User
from librerian import db

class UserCollection(Resource):
    
    def get(self):
        user_data = []
        user_list = User.query.all()
        for user in user_list:
            user_data.append(user.serialize())
        return user_data, 200
    
    def post(self):
        if not request.json:
            return Response(
                headers={},
                response="Reguest not json",
                status=415
            )
            
        try:
            validate(request.json, User.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e))

        user = User()
        user.deserialize(doc=request.json)
        
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return Response(
                headers={},
                response="User already exits",
                status=409
            )

        return Response(
            headers={"Location": url_for("api.useritem", user=user)},
            response="User creation succesful",
            status=201
        )

class UserItem(Resource):
    def get(self, user):
        if user is None:
            return "", 404
        
        return user.serialize(), 200
    
    def put(self, user):
        pass
    def delete(self, user):
        pass