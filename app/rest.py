import flask_restful
from flask import request
from flask.ext.restful import abort
from flask.ext.restful import fields

from sqlalchemy.sql import func

from app import app
from app import db
from app.utils import scoped_session
from dbmodels import SampleTransferPlan

api = flask_restful.Api(app)

#  TODO: Transform Spec

class PlanResource(flask_restful.Resource):
    """shows a single plan item, and lets you create / delete a plan item"""

    # def check_404(self, plan_id):
    #    if plan_id not in plans:
    #        flask_restful.abort(
    #            404,
    #            message="transfer plan {} doesn't exist".format(plan_id))

    def get(self, plan_id):
        """fetches a single plan"""
        with scoped_session(db.engine) as db_session:
            row = db_session.query(SampleTransferPlan).filter(
                SampleTransferPlan.plan_id == plan_id).first()
            if row:
                db_session.expunge(row)
                return row.plan
        abort(404, message="Plan {} doesn't exist".format(plan_id))


    def delete(self, plan_id):
        """deletes a single plan"""
        with scoped_session(db.engine) as db_session:
            plan = db_session.query(SampleTransferPlan).filter(
                SampleTransferPlan.plan_id == plan_id).first()
            if plan:
                db_session.delete(plan)
                db_session.commit()
                return '', 204
            else:
                return '', 404

    def put(self, plan_id, db_session=None):
        """creates or replaces a single specific plan"""
        plan_contents = request.json
        if db_session is None:
            with scoped_session(db.engine) as db_session:
                plan = SampleTransferPlan(plan_id, plan_contents)
                db_session.add(plan)
                db_session.commit()
        else:
            plan = SampleTransferPlan(plan_id, request.json)
            db_session.add(plan)
            db_session.commit()

        response_headers = {'location': api.url_for(PlanResource,
                                                    plan_id=plan_id),
                            'etag': str(plan_id)}
        response = {plan_id: plan_contents}
        return response, 201, response_headers


class PlanListResource(flask_restful.Resource):
    """shows a list of all plans, and lets you POST to add new plans"""

    def get(self):
        """returns a list of all plans"""
        with scoped_session(db.engine) as db_session:
            rows = db_session.query(SampleTransferPlan).all()
            result = {row.plan_id: row.plan for row in rows}
            #for row in rows:
            #    db_session.expunge(rows)
            return result
        return []

    def post(self):
        """creates new plan returning a nice geeky Location header"""
        with scoped_session(db.engine) as db_session:
            row = db_session.query(func.max(SampleTransferPlan.plan_id)
                                       ).one()
            if row is None or row[0] is None:
                max_id = 0
            else:
                max_id = int(row[0].split("_")[1])
            plan_id = 'plan_%i' % (max_id + 1)
        return PlanResource().put(plan_id, db_session=db_session)
