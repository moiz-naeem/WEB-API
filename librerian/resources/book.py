"""
Book resources

Classes:
    BookGlobalCollection : Resource
    BookLocalCollection : Resource
    BookItem : Resource
"""
import json

from flask import Response, request, url_for
from flask_restful import Resource
from flasgger import swag_from, validate
from sqlalchemy.exc import IntegrityError

from librerian.models import Book, Work
from librerian import db

def itemize(book):
    """
    Itemize book data
    """
    data = book.serialize()
    data["links"] = {
        "self": {
            "href": url_for("api.bookitem", book=book, library=book.library, user=book.library.owner)
        },
        "collection": {
            "href": url_for("api.booklocalcollection", library=book.library, user=book.library.owner)
        },
        "up": {
            "href": url_for("api.bookglobalcollection")
        },
        "type": {
            "href": url_for("api.workitem", work=book.work)
        }
    }
    return data

class BookGlobalCollection(Resource):
    """
    BookGlobalCollection resource
    
    Methods:
    - get
    """
    @swag_from("../doc/bookglobalcollection/get.yml")
    def get(self):
        """
        Fetch list of all the books
        """
        body = {
            "items": [],
            "links": {
                "self": {
                    "href": url_for("api.bookglobalcollection")
                }
            }
        }
        for book in Book.query.all():
            body["items"].append(itemize(book))
        return Response(response=json.dumps(body), status=200, mimetype="application/json")

class BookLocalCollection(Resource):
    """
    BookLocalCollection resource
    
    Methods
    - get
    - post
    """
    @swag_from("../doc/booklocalcollection/get.yml")
    def get(self, user=None, library=None):
        """
        Fetch list of all the books in a library
        """
        body = {
            "items": [],
            "links": {
                "self": {
                    "href": url_for("api.booklocalcollection", library=library, user=user)
                }
            }
        }
        for book in Book.query.filter_by(library=library):
            body["items"].append(itemize(book))
        return Response(response=json.dumps(body), status=200, mimetype="application/json")

    @swag_from("../doc/booklocalcollection/post.yml")
    def post(self, user=None, library=None):
        """
        Add a book into a library
        """
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
            headers={"Location": url_for("api.bookitem", library=library, user=user, book=book)},
            response="Book creation succesful",
            status=201
        )

class BookItem(Resource):
    """
    BookItem resource

    Methods:
    - get
    - put
    - delete
    """
    @swag_from("../doc/bookitem/get.yml")
    def get(self, user=None, library=None, book=None):
        """
        Fetch book item
        """
        return Response(
            response=json.dumps(itemize(book)),
            status=200,
            mimetype="application/json"
        )

    @swag_from("../doc/bookitem/put.yml")
    def put(self, user=None, library=None, book=None):
        """
        Modify book item
        """
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
    def delete(self, user=None, library=None, book=None):
        """
        Delete book item
        """
        db.session.delete(book)
        db.session.commit()
        return "The book was succesfully deleted", 200
