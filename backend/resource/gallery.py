from flask import jsonify
from flask_restful import Resource, reqparse

import backend.utils as utils
from backend import db_models as dbm


class Gallery(Resource):
    get_args = reqparse.RequestParser()
    get_args.add_argument(
        name="artwork_num",
        type=int,
        help="Number of artwork will be display in a page.",
        location="values",
    )

    def get(self):
        """
        get number of artwork through query argument then return a list of
        artwork data

        :return: list (before jsonify) of artwork data
            [
                {
                    "info": {
                        "uid": <int>,
                        "name": <str>,
                        "genre": <str>,
                        "medium": <str>,
                        "surface": <str>,
                        "artist": <str>,
                        "created_date": <str>,
                        "created_location": <str>,
                        "min_value": <int>,
                    },
                    "artpic": <base64 str repr the picture of the art>
                },
                {...},
                {...},
            ]
        """
        endpoint_args = self.get_args.parse_args()

        artwork_num = 20
        if "artwork_num" in endpoint_args:
            artwork_num = endpoint_args["artwork_num"]

        artworks = dbm.ArtworkModel.query.limit(artwork_num).all()
        for i in range(len(artworks)):
            item = dict()
            item["info"] = artworks[i].to_dict()
            item["artpic"] = utils.get_bytestr_artpic(
                artwork_uid=item["info"]["uid"]
            )

            artworks[i] = item

        return jsonify(artworks)
