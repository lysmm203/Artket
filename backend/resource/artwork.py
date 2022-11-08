from flask_restful import Resource, reqparse, abort

from backend import db_models as dbm


class Artwork(Resource):
    get_args = reqparse.RequestParser()
    get_args.add_argument(
        name="uid",
        type=int,
        required=True,
        help="uid of the artwork must be provided.",
        location="values",
    )

    def get(self):
        uid = self.get_args.parse_args()["uid"]
        artwork_with_uid = dbm.ArtworkModel.query.filter_by(uid=uid).first()

        if not artwork_with_uid:
            abort(404, message=f"Artwork with uid {uid} does not exist.")

        return artwork_with_uid.to_json()
