"""
Book resources

Classes:
    BookGlobalCollection : Resource
    BookLibraryCollection : Resource
    BookItem : Resource
"""
import json
from werkzeug.exceptions import BadRequest

from flask import Response, request, url_for
from flask_restful import Resource
from flasgger import swag_from, validate
from sqlalchemy.exc import IntegrityError

from librerian.models import Book, Work
from librerian import db

class BookGlobalCollection(Resource):
    @swag_from("../doc/bookglobalcollection/get.yml")
    def get(self):
        body = {"items": []}
        for book in Book.query.all():
            body["items"].append(book.serialize())
        return Response(
            response=json.dumps(body, indent=4),
            status=200,
            mimetype="application/json"
        )

class BookLocalCollection(Resource):
    @swag_from("../doc/booklocalcollection/get.yml")
    def get(self, _user=None, library=None):
        body = {"items": []}
        for book in Book.query.filter_by(library=library):
            body["items"].append(book.serialize())
        return Response(
            response=json.dumps(body, indent=4),
            status=200,
            mimetype="application/json"
        )

    @swag_from("../doc/booklocalcollection/post.yml")
    def post(self, user=None, library=None):
        if not request.json:
            return "Wrong media type was used", 415
        
        validate(request.json, "Book", "../doc/librerian.yml")

        book = Book()
        book.deserialize(doc=request.json)
        book.library = library
        if Work.query.filter_by(id=book.work_id) is None:
            return "Work used in book is invalid", 409
        
        try:
            db.session.add(book)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "Book already exits", 409

        return Response(
            headers={"Location": url_for("api.bookitem", library=library, user=user)},
            response=f"{book} creation succesful",
            status=201
        )

class BookItem(Resource):
    @swag_from("../doc/bookitem/get.yml")
    def get(self, _user=None, _library=None, book=None):
        #TODO hypermedia maybe
        return Response(
            response=json.dumps(book.serialize(), indent=4),
            status=200,
            mimetype="application/json"
        )

    @swag_from("../doc/bookitem/put.yml")
    def put(self, _user=None, library=None, book=None):
        if not request.json:
            return "Wrong media type was used", 415
        
        validate(request.json, "Book", "../doc/librerian.yml")

        book.deserialize(doc=request.json)
        book.library = library

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "Book already exits", 409

        return "The book was updated succesfully", 204

    @swag_from("../doc/bookitem/delete.yml")
    def delete(self, _user=None, _library=None, book=None):
        db.session.delete(book)
        db.session.commit()
        return "The book was succesfully deleted", 200
