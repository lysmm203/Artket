from flask_restful import Resource, reqparse

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
        endpoint_args = self.get_args.parse_args()

        if "artwork_num" in endpoint_args:
            artwork_num = endpoint_args["artwork_num"]
        else:
            artwork_num = 20

        artworks = dbm.ArtworkModel.query.limit(artwork_num).all()
        for i in range(len(artworks)):
            artworks[i] = artworks[i].to_json()

        return artworks
