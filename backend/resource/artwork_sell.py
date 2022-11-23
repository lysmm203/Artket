from http import HTTPStatus as Hsta

from flask_restful import Resource, reqparse

import backend.db_models as dbm
from backend.common_vars import ART_MEDIUM


def validate_sell_artwork_query(data_dict):
    required_keys_type = {
        "name": str,
        "genre": str,
        "medium": str,
        "surface": str,
        "width": int,
        "height": int,
        "artist": str,
        "created_date": str,
        "created_location": str,
        "min_value": int,
        "seller_uid": int,
        "seller_password": str,
    }

    error_help_msg = (
        "All the following keys must be provided and can not be None or "
        'empty in "data" key in json kwargs of the query.\n'
        "- (as string type): name, genre, medium, surface, artist, "
        "created_date, created_location, seller_password\n"
        "- (as integer type): width, height, min_value, seller_uid\n"
    )
    if not data_dict.keys() >= required_keys_type.keys():
        return (
            False,
            {"error_msg": f"Missing keys.\n{error_help_msg}"},
            Hsta.BAD_REQUEST,
        )

    if not all(data_dict.values()):
        error_msg = "One or more value is empty, 0, or None."
        return (
            False,
            {"error_msg": f"{error_msg}\n{error_help_msg}"},
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
                "error_msg": f"One or more value has wrong type.\n{error_help_msg}"
            },
            Hsta.BAD_REQUEST,
        )

    return True, {"error_msg": ""}, Hsta.OK


def validate_data_for_artwork(data_dict):
    seller = dbm.UserModel.query.filter_by(uid=data_dict["seller_uid"]).first()
    if not seller:
        error_msg = f'No user with uid {data_dict["seller_uid"]}'
        return False, {"error_msg": error_msg}, Hsta.NOT_FOUND

    if seller.get_password() != data_dict["seller_password"]:
        error_msg = "Incorrect password for the seller account"
        return False, {"error_msg": error_msg}, Hsta.UNAUTHORIZED

    artwork = dbm.ArtworkModel.query.filter_by(name=data_dict["name"]).first()
    if artwork:
        error_msg = f'Artwork with name {data_dict["name"]} already exist'
        return False, {"error_msg": error_msg}, Hsta.CONFLICT

    if data_dict["medium"] not in ART_MEDIUM:
        error_msg = (
            "Invalid medium. "
            f"Medium must be one of the following: {ART_MEDIUM}"
        )
        return False, {"error_msg": error_msg}, Hsta.UNPROCESSABLE_ENTITY

    if data_dict["width"] < 1:
        error_msg = (
            "Invalid width. Width must be integer and in millimeters scale"
        )
        return False, {"error_msg": error_msg}, Hsta.UNPROCESSABLE_ENTITY

    if data_dict["height"] < 1:
        error_msg = (
            "Invalid height. Height must be integer and in millimeters scale"
        )
        return False, {"error_msg": error_msg}, Hsta.UNPROCESSABLE_ENTITY

    if data_dict["min_value"] < 0:
        error_msg = (
            "Invalid min_value. min_value must be integer repr value in USD"
        )
        return False, {"error_msg": error_msg}, Hsta.UNPROCESSABLE_ENTITY

    return True, {"error_msg": ""}, Hsta.OK


def create_artwork_for_sell(data_dict):
    is_valid, error_msg, status_code = validate_data_for_artwork(data_dict)
    if not is_valid:
        return error_msg, status_code

    new_artwork = dbm.ArtworkModel(
        name=data_dict["name"],
        genre=data_dict["genre"],
        medium=data_dict["medium"],
        surface=data_dict["surface"],
        width=data_dict["width"],
        height=data_dict["height"],
        artist=data_dict["artist"],
        created_date=data_dict["created_date"],
        created_location=data_dict["created_location"],
        min_value=data_dict["min_value"],
        seller=data_dict["seller_uid"],
    )
    dbm.db.session.add(new_artwork)
    dbm.db.session.commit()

    return new_artwork.to_dict(), 200


class SellArtwork(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="data", type=dict, required=True, location="json")

    def put(self):
        data = self.parser.parse_args()["data"]

        is_valid, error_msg, status_code = validate_sell_artwork_query(data)
        if not is_valid:
            return error_msg, status_code

        return create_artwork_for_sell(data)
