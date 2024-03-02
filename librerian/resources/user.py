"""
User resources

Classes:
    UserCollection : Resource
    UserItem : Resource
"""
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import BadRequest

from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from librerian.models import User
from librerian import db

class UserCollection(Resource):
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

    def post(self):
        if not request.json:
            return Response(
                response="Reguest not json",
                status=415
            )

        try:
            validate(request.json, User.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        user = User()
        user.deserialize(doc=request.json)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return Response(
                response=f"{user} already exits",
                status=409
            )

        return Response(
            headers={"Location": url_for("api.useritem", user=user)},
            response=f"{user} creation succesful",
            status=201
        )

class UserItem(Resource):
    def get(self, user):
        #TODO
        return Response(
            response=json.dumps(user.serialize(), indent=4),
            status=200,
            mimetype="application/json"
        )

    def put(self, user):
        if not request.json:
            return Response(
                response="Request not json",
                status=215
            )

        try:
            validate(request.json, User.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        user.deserialize(doc=request.json)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return Response(
                response=f"{user} already exits",
                status=409
            )

        return Response(
            response=f"{user} update succesful",
            status=204
        )

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
        return Response(
            response=f"{user} deleted",
            status=204
        )
