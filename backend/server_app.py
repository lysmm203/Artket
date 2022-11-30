import os

from flask import Flask
from flask_restful import Api

from backend import db_models as dbm
from resource.artwork_get import GetArtwork
from resource.artwork_sell import SellArtwork
from resource.artwork_buy import BuyArtwork
from resource.gallery import Gallery
from resource.user_create import CreateUser
from resource.user_get import GetUser
from resource.user_saved import UserSaved


def init_app():
    app = Flask(__name__)
    app.app_context().push()

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    dbm.db.init_app(app)
    if not os.path.exists(
        os.path.join(os.getcwd(), "instance", "database.db")
    ):
        dbm.db.create_all()

        import backend.db_generator as model

        model.artwork_db_generator(dbm.db.session, dbm.ArtworkModel)
        model.user_db_generator(dbm.db.session, dbm.UserModel)
        model.code_db_generator(dbm.db.session, dbm.InvitationCodeModel)

    return app


def main():
    app = init_app()

    api = Api(app)
    api.add_resource(GetArtwork, "/artwork/get")
    api.add_resource(SellArtwork, "/artwork/sell")
    api.add_resource(BuyArtwork, "/artwork/buy")

    api.add_resource(Gallery, "/gallery")

    api.add_resource(GetUser, "/user/get")
    api.add_resource(CreateUser, "/user/create")
    api.add_resource(UserSaved, "/user/saved")

    app.run(debug=True)


if __name__ == "__main__":
    main()
