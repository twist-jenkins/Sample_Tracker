"""Define REST resources for CRUD on Hamilton/Echo worklists."""

import flask_restful

from flask import Response
from flask.ext.restful import abort

from app import app, db
from app.utils import scoped_session

from twistdb.sampletrack import TransformSpec

api = flask_restful.Api(app)


class WorklistResource(flask_restful.Resource):
    """get / delete / put a single worklist"""

    def get(self, spec_id):
        """Retrieves worklist from a spec (if present)."""
        with scoped_session(db.engine) as sess:
            spec = sess.query(TransformSpec).filter(
                TransformSpec.spec_id == spec_id).first()
            if not spec:
                abort(404, message="Spec {} doesn't exist".format(spec_id))

            try:
                worklist = spec.data_json['details']['worklist']['content']
            except:
                abort(404, message="Spec {} does not contain details.worklist.content?".format(spec_id))

            # return worklist, 200
            return Response(worklist, mimetype='text/csv')
