import os
import json
from datetime import datetime, date
import logging

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask.json import JSONEncoder
from bson.objectid import ObjectId
from flask_restful import Api
from api.admin.update_role import UpdateUserRoleAPI
from extensions import mongo
from api.users import CreateUserAPI, DeleteUserAPI, LoginUserAPI, GetAllUsersAPI, UpdateUserAPI
from api.upload_image import ImageUploadAPI

class CustomJSONEncoder(JSONEncoder):
    """Custom JSON Encoder which can handle mongo types like ObjectId"""
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime('%d-%m-%Y %H:%M:%S %Z')
        elif isinstance(obj, date):
            return obj.strftime('%d-%m-%Y')
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        elif isinstance(obj, json.JSONEncoder):
            return obj.default(obj)
        try:
          return super().default(self, obj)
        except TypeError as te:
          logging.warning(f'{te} in CustomJSONEncoder. Object was serialized as obj.__dict__')
          return obj.__dict__

load_dotenv()


app = Flask(__name__)
CORS(app)
api = Api(app)

###### Configuration ##########
app.json_encoder = CustomJSONEncoder
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
mongo.init_app(app)


####### Endpoints ###########
api.add_resource(CreateUserAPI, "/api/register")
api.add_resource(LoginUserAPI, "/api/login")
api.add_resource(GetAllUsersAPI, "/api/users")
api.add_resource(ImageUploadAPI, "/api/upload")
api.add_resource(UpdateUserRoleAPI, "/api/admin/users")
api.add_resource(UpdateUserAPI, "/api/users/update")
api.add_resource(DeleteUserAPI, "/api/users/delete")

if __name__ == "__main__":
    app.run(debug=True)
