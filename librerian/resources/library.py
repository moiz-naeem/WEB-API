"""
Library resources

Classes:
    LibraryCollection : Resource
    LibraryItem : Resource
"""
import json
from werkzeug.exceptions import BadRequest

from flask import Response, request, url_for
from flask_restful import Resource
from flasgger import swag_from, validate
from sqlalchemy.exc import IntegrityError

from librerian.models import Library
from librerian import db

class LibraryCollection(Resource):
    @swag_from("../doc/librarycollection/get.yml")
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

    @swag_from("../doc/librarycollection/post.yml")
    def post(self, user=None):
        if user is None:
            return "Invalid URL for POST", 415
        if not request.json:
            return "Wrong media type was used", 415
        validate(request.json, "Library", "../doc/librerian.yml")

        library = Library()
        library.deserialize(doc=request.json)
        library.owner = user

        try:
            db.session.add(library)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "A library with the same name already exists", 409

        return Response(
            headers={"Location": url_for("api.libraryitem", library=library, user=user)},
            response=f"{library} creation succesful",
            status=201
        )

class LibraryItem(Resource):
    @swag_from("../doc/libraryitem/get.yml")
    def get(self, _user=None, library=None):
        #TODO
        return Response(
            response=json.dumps(library.serialize(), indent=4),
            status=200,
            mimetype="application/json"
        )

    @swag_from("../doc/libraryitem/put.yml")
    def put(self, user=None, library=None):
        if not request.json:
            return "Wrong media type was used", 415
        validate(request.json, "Library", "../doc/librerian.yml")

        library.deserialize(doc=request.json)
        library.owner = user

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "A library with the same name already exists", 409

        return "The library was updated succesfully", 204
        

    def delete(self, _user=None, library=None):
        db.session.delete(library)
        db.session.commit()
        return "The library was succesfully deleted", 200
