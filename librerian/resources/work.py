"""
Work resources

Classes:
    WorkCollection : Resource
    WorkItem : Resource
"""
import json

from flask import Response, request, url_for
from flask_restful import Resource
from flasgger import swag_from, validate
from sqlalchemy.exc import IntegrityError

from librerian.models import Work, Book
from librerian import db

def itemize(work):
    data = work.serialize()
    data["links"] = {
        "self": {
            "href": url_for("api.workitem", work=work)
        },
        "collection": {
            "href": url_for("api.workcollection")
        }
    }
    return data

class WorkCollection(Resource):
    """
    Work Collection resource

    Methods:
    - get
    - post
    """
    @swag_from("../doc/workcollection/get.yml")
    def get(self):
        """
        Fetch a list of the works
        """
        work_list = Work.query.all()
        body = {
            "items": [],
            "self": {
                "href": url_for("api.workcollection")
            }
        }
        for work in work_list:
            body["items"].append(itemize(work))
        return Response(response=json.dumps(body), status=200, mimetype="application/json")

    @swag_from("../doc/workcollection/post.yml")
    def post(self):
        """
        Add a work
        """
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
    """
    WorkItem resource

    Methods:
    - get
    - put
    - delete
    """
    @swag_from("../doc/workitem/get.yml")
    def get(self, work):
        """
        Fetch work item
        """
        data = itemize(work)
        data["links"] = {"items": []}
        for book in Book.query(work=work):
            data["links"]["items"].append(book)
        return Response(
            response=json.dumps(itemize(work)),
            status=200,
            mimetype="application/json"
        )

    @swag_from("../doc/workitem/put.yml")
    def put(self, work):
        """
        Modify work item
        """
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
            response="The work was modified succesfully",
            status=201
        )

    @swag_from("../doc/workitem/delete.yml")
    def delete(self, work):
        """
        Delete work item
        """
        if not Book.query.filter_by(work=work):
            db.session.delete(work)
            db.session.commit()
            return "The work was succesfully deleted", 200
        return "The work has books associated, cannot be deleted", 409
