from http import HTTPStatus as Hsta

from flask_restful import Resource, reqparse

import backend.db_models as dbm


def validate_get_artwork_query(data_dict):
    if "uid" not in data_dict or not isinstance(data_dict["uid"], int):
        error_msg = (
            'Invalid or missing "uid" field. "uid" field must '
            'have type int and be provided in "data" key in '
            "json kwarg"
        )

        return False, {"error_msg": error_msg}, Hsta.BAD_REQUEST

    return True, {"error_msg": ""}, Hsta.OK


class GetArtwork(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="data", type=dict, required=True, location="json")

    def get(self):
        """
        get artwork uid through query argument then return the artwork data

        :return: dict (before jsonify) repr an artwork data
            {
                "info": {
                    "uid": <int>,
                    "name": <str>,
                    "genre": <str>,
                    "medium": <str>,
                    ...
                    # fields list can be seen at db_models.ArtworkModel
                    ...
                    "price_history": <list of int>,
                    "sale_history": <list of dict(buyer, price)>,
                    "provenance": <str>,
                },
                "artpic": <base64 str repr the picture of the art>
            }
        """
        data = self.parser.parse_args()["data"]
        is_valid, error_msg, status_code = validate_get_artwork_query(data)

        if not is_valid:
            return error_msg, status_code

        uid = data["uid"]
        artwork_with_uid = dbm.ArtworkModel.query.filter_by(uid=uid).first()

        if not artwork_with_uid:
            error_msg = f"Artwork with uid {uid} does not exist."
            return {"error_msg": error_msg}, Hsta.NOT_FOUND

        response = dict()
        response["info"] = artwork_with_uid.to_dict()
        response["artpic"] = artwork_with_uid.get_bytestr_artpic()

        artwork_history = artwork_with_uid.get_artwork_history()
        for field in artwork_history:
            response["info"][field] = artwork_history[field]

        return response, Hsta.OK
