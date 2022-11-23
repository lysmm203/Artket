from http import HTTPStatus as Hsta

import phonenumbers as pn
from flask_restful import Resource, reqparse

import backend.db_models as dbm


def get_user(uid=None, email=None, mobile=None, password=None):
    # validate input arg
    if not any([uid, email, mobile]):
        error_msg = (
            "User's uid, email address, or mobile number must be provided"
        )
        return {"error_msg": error_msg}, Hsta.UNAUTHORIZED

    if not password:
        return {"error_msg": "Password must be provided"}, Hsta.UNAUTHORIZED

    # find the user with uid, email, or mobile
    user = None
    if not user and uid:
        user = dbm.UserModel.query.filter_by(uid=uid).first()

    if not user and email:
        user = dbm.UserModel.query.filter_by(email=email).first()

    if not user and mobile:
        user = dbm.UserModel.query.filter_by(
            mobile=pn.format_number(
                pn.parse(mobile), pn.PhoneNumberFormat.E164
            )
        ).first()

    if not user:
        error_msg = "No user with provided uid, email, or mobile"
        return {"error_msg": error_msg}, Hsta.NOT_FOUND

    # check the user's password with match data
    if user.get_password() == password:
        return user.to_dict(), Hsta.OK
    else:
        return {"error_msg": "Incorrect password"}, Hsta.UNAUTHORIZED


class GetUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="data", type=dict, required=True, location="json")

    def post(self):
        data = self.parser.parse_args()["data"]

        return get_user(
            uid=data["uid"] if "uid" in data else None,
            email=data["email"] if "email" in data else None,
            mobile=data["mobile"] if "mobile" in data else None,
            password=data["password"] if "password" in data else None,
        )
