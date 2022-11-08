import os

from flask import Flask
from flask_restful import Api

from backend import db_models as dbm
from resource.artwork import Artwork
from resource.gallery import Gallery


def init_app():
    app = Flask(__name__)
    app.app_context().push()

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    dbm.db.init_app(app)
    if not os.path.exists(
        os.path.join(os.getcwd(), "instance", "database.db")
    ):
        dbm.db.create_all()

    return app


def main():
    app = init_app()

    api = Api(app)
    api.add_resource(Artwork, "/artwork")
    api.add_resource(Gallery, "/gallery")

    app.run(debug=True)


if __name__ == "__main__":
    main()
