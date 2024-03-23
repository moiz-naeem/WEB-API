"""
Work resources

Classes:
    WorkCollection : Resource
    WorkItem : Resource
"""
import json
from werkzeug.exceptions import BadRequest

from flask import Response, request, url_for
from flask_restful import Resource
from flasgger import swag_from, validate
from sqlalchemy.exc import IntegrityError

from librerian.models import Work, Book
from librerian import db

class WorkCollection(Resource):
    @swag_from("../doc/workcollection/get.yml")
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
    
    @swag_from("../doc/workcollection/post.yml")
    def post(self):
        if not request.json:
            return "Wrong media type was used", 415
        
        validate(request.json, "Work", "../doc/librerian.yml")

        work = Work()
        work.deserialize(doc=request.json)

        try:
            db.session.add(work)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "A work with the same ---- already exists", 409

        return Response(
            headers={"Location": url_for("api.workitem", work=work)},
            response="The work was created succesfully",
            status=201
        )

class WorkItem(Resource):
    @swag_from("../doc/workitem/get.yml")
    def get(self, work):
        #TODO
        return Response(
            response=json.dumps(work.serialize(), indent=4),
            status=200,
            mimetype="application/json"
        )

    @swag_from("../doc/workitem/put.yml")
    def put(self, work):
        if not request.json:
            return "Wrong media type was used", 415
        
        validate(request.json, "Work", "../doc/librerian.yml")

        work = Work()
        work.deserialize(doc=request.json)

        try:
            db.session.add(work)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "A work with the same ---- already exists", 409

        return Response(
            headers={"Location": url_for("api.workitem", work=work)},
            response="The work was created succesfully",
            status=201
        )

    @swag_from("../doc/workitem/delete.yml")
    def delete(self, work):
        if not Book.query.filter_by(work=work):
            db.session.delete(work)
            db.session.commit()
            return "The work was succesfully deleted", 200
        return "The work has books associated, cannot be deleted", 409
