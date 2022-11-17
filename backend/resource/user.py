from flask import jsonify
from flask_restful import Resource, reqparse

import backend.db_models as dbm


def get_user(uid=None, email=None, mobile=None, password=None):
    if not any([uid, email, mobile]):
        error_msg = (
            "User's uid, email address, or mobile number must " "be provided"
        )
        return {"error_msg": error_msg}, 401

    if not password:
        return {"error_msg": "Password must be provided"}, 401

    user = None
    if uid:
        user = dbm.UserModel.query.filter_by(uid=uid).first()
    elif email:
        user = dbm.UserModel.query.filter_by(email=email).first()
    elif mobile:
        user = dbm.UserModel.query.filter_by(mobile=mobile).first()

    if user.get_password() == password:
        return user.to_dict(), 200
    else:
        return {"error_msg": "Incorrect password"}, 401


class User(Resource):
    post_args = reqparse.RequestParser()
    post_args.add_argument(
        name="action",
        type=str,
        choices=[
            "sign-up",
            "sign-in",
        ],
        required=True,
        help='"action" arg is required. action is the intended action for this'
        ' post request, available action include "sign-up" and "sign-in"',
        location="values",
    )
    post_args.add_argument(
        name="uid",
        type=int,
        location="values",
    )
    post_args.add_argument(
        name="email",
        type=str,
        location="values",
    )
    post_args.add_argument(
        name="mobile",
        type=str,
        location="values",
    )
    post_args.add_argument(
        name="password",
        type=str,
        location="values",
    )

    def post(self):
        endpoint_args = self.post_args.parse_args()

        if endpoint_args["action"] == "sign-in":
            return jsonify(
                get_user(
                    uid=endpoint_args["uid"],
                    email=endpoint_args["email"],
                    mobile=endpoint_args["mobile"],
                    password=endpoint_args["password"],
                )
            )
