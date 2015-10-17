import flask_restful
#from flask_restful import reqparse
from flask import request

from app import app
api = flask_restful.Api(app)

plans = {
    'plan_1': {'task': 'build an API'},
    'plan_2': {'task': '?????'},
    'plan_3': {'task': 'profit!'},
}


class Plan(flask_restful.Resource):
    """shows a single plan item, and lets you create / delete a plan item"""

    #def __init__(self):
    #    self.parser = reqparse.RequestParser()
    #    self.parser.add_argument('task')
    #    super(Plan, self).__init__()

    def check_404(self, plan_id):
        if plan_id not in plans:
            flask_restful.abort(
                404,
                message="transfer plan {} doesn't exist".format(plan_id))

    def get(self, plan_id):
        """fetches a single plan"""
        self.check_404(plan_id)
        return plans[plan_id]

    def delete(self, plan_id):
        """deletes a single plan"""
        self.check_404(plan_id)
        del plans[plan_id]
        return '', 204

    def put(self, plan_id):
        """creates or replaces a single specific plan"""
        #args = self.parser.parse_args()
        plans[plan_id] = request.json #{'task': args['task']}
        response_headers = {'location': api.url_for(Plan, plan_id=plan_id),
                            'etag': "plan_id_%s" % plan_id}
        return plans[plan_id], 201, response_headers


class PlanList(flask_restful.Resource):
    """shows a list of all plans, and lets you POST to add new plans"""

    def get(self):
        """returns a list of all plans"""
        return plans

    def post(self):
        """creates new plan returning a nice geeky Location header"""
        plan_id = int(max(plans.keys()).lstrip('plan_')) + 1
        plan_id = 'plan_%i' % plan_id
        return Plan().put(plan_id)

