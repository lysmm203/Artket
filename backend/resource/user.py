import re

import phonenumbers as pn
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
        user = dbm.UserModel.query.filter_by(
            mobile=pn.format_number(
                pn.parse(mobile), pn.PhoneNumberFormat.E164
            )
        ).first()

    if user.get_password() == password:
        return user.to_dict(), 200
    else:
        return {"error_msg": "Incorrect password"}, 401


class GetUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="data", type=dict, location="json")

    def post(self):
        data = self.parser.parse_args()["data"]

        return get_user(
            uid=data["uid"] if "uid" in data else None,
            email=data["email"] if "email" in data else None,
            mobile=data["mobile"] if "mobile" in data else None,
            password=data["password"] if "password" in data else None,
        )


def validate_create_user_query(data_dict):
    if not all(
        [
            "email" in data_dict,
            "mobile" in data_dict,
            "username" in data_dict,
            "password" in data_dict,
            "invitation_code" in data_dict,
        ]
    ) or not all(data_dict.values()):
        error_msg = (
            'All "email", "mobile", "username", "password", and '
            '"invitation_code" argument must be provided (as type '
            "string and cannot be None) in data field in json of "
            "the query"
        )

        return False, {"error_msg": error_msg}, 400

    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if not re.fullmatch(email_regex, data_dict["email"]):
        return False, {"error_msg": "Invalid email address"}, 400

    if not pn.is_valid_number(pn.parse(data_dict["mobile"])):
        return False, {"error_msg": "Invalid mobile number"}, 400

    return True, {"error_msg": ""}, 200


def create_user(data_dict):
    existed_user = dbm.UserModel.query.filter_by(
        email=data_dict["email"]
    ).first()

    if existed_user:
        return {"error_msg": "Existed user"}, 409

    invite_code = dbm.InvitationCodeModel.query.filter_by(
        available_code=data_dict["invitation_code"]
    ).first()

    if not invite_code:
        return {"error_msg": "Incorrect invitation_code"}, 404

    dbm.db.session.delete(invite_code)

    new_user = dbm.UserModel(
        email=data_dict["email"],
        mobile=pn.format_number(
            pn.parse(data_dict["mobile"]), pn.PhoneNumberFormat.E164
        ),
        username=data_dict["username"],
        password=data_dict["password"],
        ranking=0,
    )
    dbm.db.session.add(new_user)
    dbm.db.session.commit()

    return new_user.to_dict(), 200


class CreateUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="data", type=dict, location="json")

    def put(self):
        data = self.parser.parse_args()["data"]

        is_valid, error_msg, status_code = validate_create_user_query(data)
        if not is_valid:
            return error_msg, status_code

        return create_user(data)
