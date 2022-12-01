from http import HTTPStatus as Hsta

from flask_restful import Resource, reqparse

import backend.db_models as dbm


def validate_user_saved_query(data_dict, action="get"):
    required_keys_type = {
        "user_uid": int,
        "user_password": str,
    }

    if action == "put" or action == "delete":
        required_keys_type["artwork_uid"] = int

    error_help_msg = (
        "All the following keys must be provided and can not be None, 0, or "
        'empty in "data" key in json kwargs of the query.\n'
        "- (as string type): user_password\n"
        "- (as integer type): user_uid, artwork_uid (need in put and delete "
        "method only)\n"
    )
    if not data_dict.keys() >= required_keys_type.keys():
        return (
            False,
            {"error_msg": f"Missing keys.\n{error_help_msg}"},
            Hsta.BAD_REQUEST,
        )

    if not all(data_dict.values()):
        return (
            False,
            {
                "error_msg": (
                    "One or more value is empty, 0, or None"
                    f".\n{error_help_msg}"
                )
            },
            Hsta.BAD_REQUEST,
        )

    if not all(
        [
            type(data_dict[_key]) == required_keys_type[_key]
            for _key in data_dict
        ]
    ):
        return (
            False,
            {
                "error_msg": (
                    f"One or more value has wrong type.\n{error_help_msg}"
                )
            },
            Hsta.BAD_REQUEST,
        )

    return True, {"error_msg": ""}, Hsta.OK


def validate_data_for_user_saved(data_dict):
    user = dbm.UserModel.query.filter_by(uid=data_dict["user_uid"]).first()
    if not user:
        error_msg = f'No user with uid {data_dict["user_uid"]}'
        return False, {"error_msg": error_msg}, Hsta.NOT_FOUND

    if user.get_password() != data_dict["user_password"]:
        error_msg = "Incorrect password for the user account"
        return False, {"error_msg": error_msg}, Hsta.UNAUTHORIZED

    if "artwork_uid" in data_dict:
        artwork = dbm.ArtworkModel.query.filter_by(
            uid=data_dict["artwork_uid"]
        ).first()
        if not artwork:
            error_msg = f'No artwork with uid {data_dict["artwork_uid"]}'
            return False, {"error_msg": error_msg}, Hsta.NOT_FOUND

    return True, {"error_msg": ""}, Hsta.OK


def get_user_saved(data_dict):
    is_valid, error_msg, status_code = validate_data_for_user_saved(data_dict)
    if not is_valid:
        return error_msg, status_code

    user = dbm.UserModel.query.filter_by(uid=data_dict["user_uid"]).first()
    return {"user_saved": user.get_saved()}, Hsta.OK


def put_artwork_to_user_saved(data_dict):
    is_valid, error_msg, status_code = validate_data_for_user_saved(data_dict)
    if not is_valid:
        return error_msg, status_code

    user = dbm.UserModel.query.filter_by(uid=data_dict["user_uid"]).first()
    user.add_to_saved(data_dict["artwork_uid"])

    return {"new_user_saved": user.get_saved()}, Hsta.OK


def delete_artwork_from_user_saved(data_dict):
    is_valid, error_msg, status_code = validate_data_for_user_saved(data_dict)
    if not is_valid:
        return error_msg, status_code

    user = dbm.UserModel.query.filter_by(uid=data_dict["user_uid"]).first()

    try:
        user.remove_from_saved(data_dict["artwork_uid"])
    except KeyError as err:
        return {"error_msg": str(err)}, Hsta.NOT_FOUND

    return {"new_user_saved": user.get_saved()}, Hsta.OK


class UserSaved(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="data", type=dict, required=True, location="json")

    def get(self):
        data = self.parser.parse_args()["data"]
        is_valid, error_msg, status_code = validate_user_saved_query(data)
        if not is_valid:
            return error_msg, status_code

        return get_user_saved(data)

    def put(self):
        data = self.parser.parse_args()["data"]
        is_valid, error_msg, status_code = validate_user_saved_query(
            data_dict=data, action="put"
        )
        if not is_valid:
            return error_msg, status_code

        return put_artwork_to_user_saved(data)

    def delete(self):
        data = self.parser.parse_args()["data"]
        is_valid, error_msg, status_code = validate_user_saved_query(
            data_dict=data, action="delete"
        )
        if not is_valid:
            return error_msg, status_code

        return delete_artwork_from_user_saved(data)
