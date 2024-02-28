import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from librerian.models import Work
from librerian import db

class WorkCollection(Resource):
    def get(self):
        work_list = Work.query.all()
        work_data = []
        for work in work_list:
            work_data.append(work.serialize())
        return Response(
            response=json.dumps(work_data, indent=4),
            status=200
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
            raise BadRequest(description=str(e))

        work = Work()
        work.deserialize(doc=request.json)

        try:
            db.session.add(work)
            db.session.commit()
        except IntegrityError:
            return Response(
                response="Work already exits",
                status=409
            )

        return Response(
            headers={"Location": url_for("api.workitem", work=work)},
            response="Work creation succesful",
            status=201
        )

class WorkItem(Resource):
    def get(self, work):
        #TODO
        return Response(
            response=json.dumps(work.serialize(), indent=4),
            status=200
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
            raise BadRequest(description=str(e))

        work = Work()
        work.deserialize(doc=request.json)

        try:
            db.session.add(work)
            db.session.commit()
        except IntegrityError:
            return Response(
                response="Work already exits",
                status=409
            )

        return Response(
            headers={"Location": url_for("api.workitem", work=work)},
            response="Work creation succesful",
            status=201
        )

    def delete(self, work):
        if not Book.query.filter_by(work=work):
            db.session.delete(work)
            db.session.commit(work)
            return Response(
                response="Work deleted",
                status=204
            )
        return Response(
            response="Work has books associated, cannot be deleted",
            status=409
        )
