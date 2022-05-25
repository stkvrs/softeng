from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from base64 import b64encode, b64decode
from bson.objectid import ObjectId
from werkzeug.datastructures import FileStorage
from extensions import mongo


class ImageUploadAPI(Resource):
    def __init__(self):
        self.post_reqparse = reqparse.RequestParser()

        self.post_reqparse.add_argument("image", type=FileStorage, location="files")
        self.post_reqparse.add_argument("id", type=str, required=True, location="args")
        super(ImageUploadAPI, self).__init__()

    def post(self):

        args = self.post_reqparse.parse_args()

        user_id = args['id']

        uploaded_image = args["image"]

        base64_str = b64encode(uploaded_image.read())

        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"img": base64_str}})

        result = mongo.db.users.find_one({"_id": ObjectId(user_id)})

        return make_response(jsonify(result), 204)
