"""
Book resources

Classes:
    BookCollection : Resource
    BookItem : Resource
"""
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import BadRequest

from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from librerian.models import Book, Work
from librerian import db

class BookCollection(Resource):
    def get(self, _user=None, library=None):
        if library is None:
            book_list = Book.query.all()
        else:
            book_list = Book.query.filter_by(library=library)
        body = {"items": []}
        for book in book_list:
            body["items"].append(book.serialize())
        return Response(
            response=json.dumps(body, indent=4),
            status=200,
            mimetype="application/json"
        )

    def post(self, user=None, library=None):
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
            validate(request.json, Book.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        book = Book()
        book.deserialize(doc=request.json)
        book.library = library
        if Work.query.filter_by(id=book.work_id) is None:
            return Response(
                response="Work is invalid",
                status=409
            )
        try:
            db.session.add(book)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return Response(
                response=f"{book} already exits",
                status=409
            )

        return Response(
            headers={"Location": url_for("api.bookitem", library=library, user=user)},
            response=f"{book} creation succesful",
            status=201
        )

class BookItem(Resource):
    def get(self, _user=None, _library=None, book=None):
        #TODO
        return Response(
            response=json.dumps(book.serialize(), indent=4),
            status=200,
            mimetype="application/json"
        )

    def put(self, _user=None, library=None, book=None):
        if not request.json:
            return Response(
                response="Request not json",
                status=215
            )

        try:
            validate(request.json, Book.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        book.deserialize(doc=request.json)
        book.library = library

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return Response(
                response=f"{book} already exits",
                status=409
            )

        return Response(
            response=f"{book} update succesful",
            status=204
        )

    def delete(self, _user=None, _library=None, book=None):
        db.session.delete(book)
        db.session.commit()
        return Response(
            response=f"{book} deleted",
            status=204
        )
