from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mongo


class CreateUserAPI(Resource):
    def __init__(self):
        self.post_reqparse = reqparse.RequestParser()

        self.post_reqparse.add_argument(
            "first_name", type=str, required=True, location="json"
        )
        self.post_reqparse.add_argument(
            "last_name", type=str, required=True, location="json"
        )
        self.post_reqparse.add_argument(
            "email", type=str, required=True, location="json"
        )
        self.post_reqparse.add_argument(
            "password", type=str, required=True, location="json"
        )
        self.post_reqparse.add_argument(
            "degree", type=str, required=False, location="json"
        )
        self.post_reqparse.add_argument(
            "grad_date", type=str, required=False, location="json"
        )
        self.post_reqparse.add_argument(
            "description", type=str, required=False, location="json"
        )
        self.post_reqparse.add_argument(
            "hobbies", type=list, required=False, location="json"
        )
        self.post_reqparse.add_argument(
            "img", type=str, required=False, location="json"
        )

        super(CreateUserAPI, self).__init__()

    def post(self):

        args = self.post_reqparse.parse_args()

        first_name = args["first_name"]
        last_name = args["last_name"]
        email = args["email"]
        password = args["password"]
        degree = args["degree"]
        grad_date = args["grad_date"]
        description = args["description"]
        hobbies = args["hobbies"]
        img = args["img"]

        if password is not None:
            hashed_password = generate_password_hash(password)

        result_dict = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": hashed_password,
            "degree": degree,
            "grad_date": grad_date,
            "description": description,
            "hobbies": hobbies,
            "img": img,
            "role": 3
        }

        # Check if email already exists
        if mongo.db.users.find_one({"email": email}):
            return make_response(jsonify({"Error": "Email is already in use"}), 400)

        mongo.db.users.insert_one(result_dict)

        return make_response(jsonify(result_dict), 201)


class LoginUserAPI(Resource):
    def __init__(self):
        self.post_reqparse = reqparse.RequestParser()

        self.post_reqparse.add_argument(
            "email", type=str, required=True, location="json"
        )
        self.post_reqparse.add_argument(
            "password", type=str, required=True, location="json"
        )

        super(LoginUserAPI, self).__init__()

    def post(self):

        args = self.post_reqparse.parse_args()

        email = args["email"]
        password = args["password"]

        user = mongo.db.users.find_one({"email": email})

        if user is None:
            return make_response(jsonify({"Error": "The user doen't exist"}), 400)

        if email != user['email'] or not check_password_hash(user['password'], password):
            return make_response(jsonify({"Error": "Email and/or password provided are not correct"}), 400)

        return make_response(jsonify(user), 200)


class GetAllUsersAPI(Resource):
    def __init__(self):
        self.get_reqparse = reqparse.RequestParser()

        self.get_reqparse.add_argument("role", type=int, location="args")

        super(GetAllUsersAPI, self).__init__()

    def get(self):

        args = self.get_reqparse.parse_args()

        role = args['role']

        users = None

        if role:
            users = mongo.db.users.find({"role": role})
        else:
            users = mongo.db.users.find({})

        result = [user for user in users]

        return make_response(jsonify(result), 200)

