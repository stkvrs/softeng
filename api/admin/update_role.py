from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from bson.objectid import ObjectId
from extensions import mongo


class UpdateUserRoleAPI(Resource):
    def __init__(self):
        self.post_reqparse = reqparse.RequestParser()

        self.post_reqparse.add_argument("id", type=str, required=True, location="json")

        super(UpdateUserRoleAPI, self).__init__()

    def post(self):

        args = self.post_reqparse.parse_args()

        user_id = args["id"]

        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": 2}})

        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

        return make_response(jsonify(user), 200)
