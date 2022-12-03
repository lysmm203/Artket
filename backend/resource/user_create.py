import re
from http import HTTPStatus as Hsta

import phonenumbers as pn
from flask_restful import Resource, reqparse

import backend.db_models as dbm


def validate_create_user_query(data_dict):
    required_keys_type = {
        "email": str,
        "mobile": str,
        "username": str,
        "password": str,
        "invitation_code": str,
    }

    if (
        not data_dict.keys() >= required_keys_type.keys()
        or not all(
            [
                type(data_dict[_key]) == required_keys_type[_key]
                for _key in data_dict
            ]
        )
        or not all(data_dict.values())
    ):
        error_msg = (
            'Missing fields. All "email", "mobile", "username", "password", '
            "and "
            '"invitation_code" argument must be provided (as type '
            "string and cannot be None) in data field in json of "
            "the query"
        )

        return False, {"error_msg": error_msg}, Hsta.BAD_REQUEST

    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if not re.fullmatch(email_regex, data_dict["email"]):
        return False, {"error_msg": "Invalid email address."}, Hsta.BAD_REQUEST

    if not all(
        [
            len(data_dict["mobile"]) > 10,
            data_dict["mobile"][0] == "+",
            data_dict["mobile"][1:].isnumeric(),
        ]
    ) or not pn.is_valid_number(pn.parse(data_dict["mobile"])):
        return False, {"error_msg": "Invalid phone number."}, Hsta.BAD_REQUEST

    return True, {"error_msg": ""}, Hsta.OK


def create_user(data_dict):
    existed_user = dbm.UserModel.query.filter_by(
        email=data_dict["email"]
    ).first()
    if existed_user:
        error_msg = "Existed user with provided email."
        return {"error_msg": error_msg}, Hsta.CONFLICT

    existed_mobile = dbm.UserModel.query.filter_by(
        mobile=pn.format_number(
            pn.parse(data_dict["mobile"]), pn.PhoneNumberFormat.E164
        ),
    ).first()
    if existed_mobile:
        error_msg = "Existed user with provided phone number."
        return {"error_msg": error_msg}, Hsta.CONFLICT

    invite_code = dbm.InvitationCodeModel.query.filter_by(
        available_code=data_dict["invitation_code"]
    ).first()

    if not invite_code:
        return {"error_msg": "Incorrect invitation code."}, Hsta.UNAUTHORIZED

    dbm.db.session.delete(invite_code)

    new_user = dbm.UserModel(
        email=data_dict["email"],
        mobile=pn.format_number(
            pn.parse(data_dict["mobile"]), pn.PhoneNumberFormat.E164
        ),
        username=data_dict["username"],
        password=data_dict["password"],
    )
    dbm.db.session.add(new_user)
    dbm.db.session.commit()

    return new_user.to_dict(), Hsta.OK


class CreateUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="data", type=dict, required=True, location="json")

    def put(self):
        data = self.parser.parse_args()["data"]

        is_valid, error_msg, status_code = validate_create_user_query(data)
        if not is_valid:
            return error_msg, status_code

        return create_user(data)
