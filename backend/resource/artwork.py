from flask_restful import Resource, reqparse
from http import HTTPStatus as Hsta
import backend.db_models as dbm
import backend.utils as utils


class Artwork(Resource):
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
        if "uid" not in data or not isinstance(data["uid"], int):
            error_msg = (
                'Invalid or missing "uid" field. "uid" field must '
                'have type int and be provided in "data" key in '
                "json kwarg"
            )

            return {"error_msg": error_msg}, Hsta.BAD_REQUEST

        uid = data["uid"]
        artwork_with_uid = dbm.ArtworkModel.query.filter_by(uid=uid).first()

        if not artwork_with_uid:
            error_msg = f"Artwork with uid {uid} does not exist."
            return {"error_msg": error_msg}, Hsta.NOT_FOUND

        response = dict()
        response["info"] = artwork_with_uid.to_dict()
        response["artpic"] = utils.get_bytestr_artpic(artwork_uid=uid)

        artwork_history = utils.get_artwork_history(artwork_uid=uid)
        for field in artwork_history:
            response["info"][field] = artwork_history[field]

        return response, Hsta.OK
