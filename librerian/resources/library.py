"""
Library resources

Classes:
    LibraryGlobalCollection : Resource
    LibraryLocalCollection : Resource
    LibraryItem : Resource
"""
import json

from flask import Response, request, url_for
from flask_restful import Resource
from flasgger import swag_from, validate
from sqlalchemy.exc import IntegrityError

from librerian.models import Library
from librerian import db

def itemize(library):
    data = library.serialize(short_form=True)
    data["links"] = {
        "self": {
            "href": url_for("api.libraryitem", library=library, user=library.owner)
        },
        "up": {
            "href": url_for("api.librarylocalcollection", user=library.owner)
        }
    }

    return data

class LibraryGlobalCollection(Resource):
    """
    LibraryGlobalCollection

    Methods:
    - get
    """
    @swag_from("../doc/libraryglobalcollection/get.yml")
    def get(self):
        """
        Fetch list of all the libraries
        """
        body = {"items": []}
        for library in Library.query.all():
            body["items"].append(itemize(library))
        return Response(response=json.dumps(body), status=200, mimetype="application/json")

class LibraryLocalCollection(Resource):
    """
    LibraryLocalCollection

    Methods:
    - get
    - post
    """
    @swag_from("../doc/librarylocalcollection/get.yml")
    def get(self, user=None):
        """
        Fetch list of libraries of an user
        """
        body = {"items": []}
        for library in Library.query.filter_by(owner=user):
            body["items"].append(itemize(library))
        return Response(response=json.dumps(body), status=200, mimetype="application/json")

    @swag_from("../doc/librarylocalcollection/post.yml")
    def post(self, user=None):
        """
        Add a library
        """
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
    """
    LibraryItem resource

    Methods:
    - get
    - put
    - delete
    """

    @swag_from("../doc/libraryitem/get.yml")
    def get(self, user=None, library=None):
        """
        Fetch library item
        """
        return Response(
            response=json.dumps(itemize(library)),
            status=200,
            mimetype="application/json"
        )

    @swag_from("../doc/libraryitem/put.yml")
    def put(self, user=None, library=None):
        """
        Modify library item
        """
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

    @swag_from("../doc/libraryitem/delete.yml")
    def delete(self, user=None, library=None):
        """
        Delete library item
        """
        db.session.delete(library)
        db.session.commit()
        return "The library was succesfully deleted", 200
