"""
Work resources

Classes:
    WorkCollection : Resource
    WorkItem : Resource
"""
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import BadRequest

from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from librerian.models import Work, Book
from librerian import db

class WorkCollection(Resource):
    def get(self):
        work_list = Work.query.all()
        body = {"items": []}
        for work in work_list:
            body["items"].append(work.serialize())
        return Response(
            response=json.dumps(body, indent=4),
            status=200,
            mimetype="application/json"
        )

    def post(self):
        if not request.json:
            return Response(
                response="Request not json",
                status=415
            )

        try:
            validate(request.json, Work.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        work = Work()
        work.deserialize(doc=request.json)

        try:
            db.session.add(work)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return Response(
                response=f"{work} already exists",
                status=409
            )

        return Response(
            headers={"Location": url_for("api.workitem", work=work)},
            response=f"{work} creation succesful",
            status=201
        )

class WorkItem(Resource):
    def get(self, work):
        #TODO
        return Response(
            response=json.dumps(work.serialize(), indent=4),
            status=200,
            mimetype="application/json"
        )

    def put(self, work):
        if not request.json:
            return Response(
                response="Request not json",
                status=415
            )

        try:
            validate(request.json, Work.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        work = Work()
        work.deserialize(doc=request.json)

        try:
            db.session.add(work)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return Response(
                response=f"{work} already exists",
                status=409
            )

        return Response(
            headers={"Location": url_for("api.workitem", work=work)},
            response=f"{work} creation succesful",
            status=201
        )

    def delete(self, work):
        if not Book.query.filter_by(work=work):
            db.session.delete(work)
            db.session.commit()
            return Response(
                response=f"{work} deleted",
                status=204
            )
        return Response(
            response=f"{work} has books associated, cannot be deleted",
            status=409
        )
