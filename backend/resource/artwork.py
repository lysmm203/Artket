from flask import jsonify
from flask_restful import Resource, reqparse, abort

import backend.db_models as dbm
import backend.utils as utils


class Artwork(Resource):
    get_args = reqparse.RequestParser()
    get_args.add_argument(
        name="uid",
        type=int,
        required=True,
        help='Missing "uid" arg. uid of the artwork must be provided.',
        location="values",
    )

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
        uid = self.get_args.parse_args()["uid"]
        artwork_with_uid = dbm.ArtworkModel.query.filter_by(uid=uid).first()

        if not artwork_with_uid:
            abort(404, message=f"Artwork with uid {uid} does not exist.")

        response = dict()
        response["info"] = artwork_with_uid.to_dict()
        response["artpic"] = utils.get_bytestr_artpic(artwork_uid=uid)

        artwork_history = utils.get_artwork_history(artwork_uid=uid)
        for field in artwork_history:
            response["info"][field] = artwork_history[field]

        return jsonify(response)
