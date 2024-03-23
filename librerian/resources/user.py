"""
User resources

Classes:
    UserCollection : Resource
    UserItem : Resource
"""
import json
from werkzeug.exceptions import BadRequest

from flask import Response, request, url_for
from flask_restful import Resource
from flasgger import swag_from, validate
from sqlalchemy.exc import IntegrityError

from librerian.models import User
from librerian import db

class UserCollection(Resource):
    @swag_from("../doc/usercollection/get.yml")
    def get(self):
        #TODO
        body = {"items": []}
        for user in User.query.all():
            body["items"].append(user.serialize(short_form=True))
        return Response(
            response=json.dumps(body, indent=4),
            status=200,
            mimetype="application/json"
        )

    @swag_from("../doc/usercollection/post.yml")
    def post(self):
        if not request.json:
            return "Wrong media type was used", 415
        
        validate(request.json, "User", "../doc/librerian.yml")

        user = User()
        user.deserialize(doc=request.json)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "A user with the same handle or email already exists", 409

        return Response(
            headers={"Location": url_for("api.useritem", user=user)},
            response="New user created succesfully",
            status=201
        )

class UserItem(Resource):
    @swag_from("../doc/useritem/get.yml")
    def get(self, user):
        #TODO
        return Response(
            response=json.dumps(user.serialize(), indent=4),
            status=200,
            mimetype="application/json"
        )
    
    @swag_from("../doc/useritem/put.yml")
    def put(self, user):
        if not request.json:
            return "Wrong media type was used", 415
        
        validate(request.json, "User", "../doc/librerian.yml")

        user.deserialize(doc=request.json)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "A user with the same handle or email already exists", 409
    
        return "The user was updated succesfully", 204

    @swag_from("../doc/useritem/delete.yml")
    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
        return "The user was succesfully deleted", 200
