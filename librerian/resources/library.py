import json
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType

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

        library_data = []
        for library in library_list:
            library_data.append(library.serialize())
        return Response(
            response=json.dumps(library_data, indent=4), 
            status=200
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
            raise BadRequest(description=str(e))

        library = Library()
        library.deserialize(doc=request.json)
        library.owner = user

        try:
            db.session.add(library)
            db.session.commit()
        except IntegrityError:
            return Response(
                response="Library already exits",
                status=409
            )

        return Response(
            headers={"Location": url_for("api.libraryitem", library=library, user=user)},
            response="Library creation succesful",
            status=201
        )

class LibraryItem(Resource):
    def get(self, user=None, library=None):
        #TODO
        return Response(
            response=json.dumps(library.serialize(), indent=4),
            status=200
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
            raise BadRequest(description=str(e))

        library.deserialize(doc=request.json)
        library.owner = user

        try:
            db.session.commit()
        except IntegrityError:
            return Response(
                response="Library already exits",
                status=409
            )

        return Response(
            response="Library update succesful",
            status=204
        )
        
    def delete(self, user=None, library=None):
        db.session.delete(library)
        db.session.commit()
        return Response(
            response="Library deleted",
            status=204
        )