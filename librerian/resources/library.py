"""
Library resources

Classes:
    LibraryCollection : Resource
    LibraryItem : Resource
"""
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import BadRequest

from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from librerian.models import Library
from librerian import db

class LibraryCollection(Resource):
    def get(self, user=None):
        if user is None:
            library_list = Library.query.all()
        else:
            library_list = Library.query.filter_by(owner=user)

        body = {"items": []}
        for library in library_list:
            body["items"].append(library.serialize())
        return Response(
            response=json.dumps(body, indent=4),
            status=200,
            mimetype="application/json"
        )

    def post(self, user=None):
        if user is None:
            return Response(
                response="Invalid URL for POST",
                status=415
            )
        if not request.json:
            return Response(
                response="Request not json",
                status=415
            )

        try:
            validate(request.json, Library.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        library = Library()
        library.deserialize(doc=request.json)
        library.owner = user

        try:
            db.session.add(library)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return Response(
                response=f"{library} already exits",
                status=409
            )

        return Response(
            headers={"Location": url_for("api.libraryitem", library=library, user=user)},
            response=f"{library} creation succesful",
            status=201
        )

class LibraryItem(Resource):
    def get(self, _user=None, library=None):
        #TODO
        return Response(
            response=json.dumps(library.serialize(), indent=4),
            status=200,
            mimetype="application/json"
        )

    def put(self, user=None, library=None):
        if not request.json:
            return Response(
                response="Request not json",
                status=215
            )

        try:
            validate(request.json, Library.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        library.deserialize(doc=request.json)
        library.owner = user

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return Response(
                response=f"{library} already exits",
                status=409
            )

        return Response(
            response=f"{library} update succesful",
            status=204
        )

    def delete(self, _user=None, library=None):
        db.session.delete(library)
        db.session.commit()
        return Response(
            response=f"{library} deleted",
            status=204
        )
