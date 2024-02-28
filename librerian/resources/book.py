import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from librerian.models import Book
from librerian import db

class BookCollection(Resource):
    
    def get(self, user=None, library=None):
        if library is None:
            book_list = Book.query.all()
        else:
            book_list = Book.query.filter_by(library=library)
        book_data = []
        for book in book_list:
            book_data.append(book.serialize())
        return Response(
            response=json.dumps(book_data,indent=4),
            status=200
        )

    def post(self, user=None, library=None):
        #currently busted, as work is not set
        if not request.json:
            return Response(
                response="Request not json",
                status=415
            )
        try:
            validate(request.json, Book.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e))

        book = Book()
        book.deserialize(doc=request.json)
        book.library = library

        try:
            db.session.add(book)
            db.session.commit()
        except IntegrityError:
            return Response(
                response="Library already exits",
                status=409
            )

        return Response(
            headers={"Location": url_for("api.bookitem", library=library, user=user)},
            response="Library creation succesful",
            status=201
        )

class BookItem(Resource):
    def get(self, user=None, library=None, book=None):
        #TODO
        return Response(
            response=json.dumps(book.serialize(), indent=4),
            status=200
        )
    
    def put(self, user=None, library=None, book=None):
        if not request.json:
            return Response(
                response="Request not json",
                status=215
            )
        
        try:
            validate(request.json, Book.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e))

        book.deserialize(doc=request.json)
        book.library = library

        try:
            db.session.commit()
        except IntegrityError:
            return Response(
                response="Book already exits",
                status=409
            )

        return Response(
            response="Book update succesful",
            status=204
        )

    def delete(self, user=None, library=None, book=None):
        db.session.delete(book)
        db.session.commit()
        return Response(
            response="Book deleted",
            status=204
        )