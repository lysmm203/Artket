import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

ARTPIC_LOC = "backend/instance/artpic/"
ART_HISTORY_LOC = "backend/instance/history.json"

db = SQLAlchemy()


class ArtworkModel(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False, unique=True)
    genre = db.Column(db.String(500), nullable=False)
    medium = db.Column(db.String(200), nullable=False)
    surface = db.Column(db.String(200), nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    artist = db.Column(db.String(500), nullable=False)
    created_date = db.Column(db.String(10), nullable=False)
    created_location = db.Column(db.String(200), nullable=False)
    min_value = db.Column(db.Integer, nullable=False)
    seller = db.Column(db.Integer, nullable=False)  # seller's uid in user db
    is_sold = db.Column(db.Integer, nullable=False, default=0)  # 0 and 1 only

    def to_dict(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "genre": self.genre,
            "medium": self.medium,
            "surface": self.surface,
            "width": self.width,
            "height": self.height,
            "artist": self.artist,
            "created_date": self.created_date,
            "created_location": self.created_location,
            "min_value": self.min_value,
            "seller": self.seller,
            "is_sold": self.is_sold,
        }

    def get_is_sold(self):
        return self.is_sold

    def get_seller_uid(self):
        return self.seller

    def get_min_value(self):
        return self.min_value

    def get_bytestr_artpic(self):
        """
        :return: base64 str repr the picture of the artwork
        """
        with open(f"{ARTPIC_LOC}{self.uid}_base64.txt", "r") as infile:
            return infile.read()

    def get_artwork_history(self):
        """
        :return: dict repr provenance, price and sale history of the artwork
            {
                "price_history": <list of int repr price history>,
                "sale_history": <list of dict (buyer, price)> [
                  {
                    "buyer": <str repr buyer name>,
                    "price": <int repr price the buyer pay for the art>
                  },
                ],
                "provenance": <str repr the literature of the art>
            }
        """
        with open(ART_HISTORY_LOC, "r") as history_database:
            data = json.load(history_database)
            return data[str(self.uid)]

    def update_is_sold(self, sold=False, seller_uid=None):
        self.is_sold = 1 if sold else 0

        if self.is_sold == 1:
            self.set_seller(seller_uid=0)
        else:
            if not seller_uid:
                raise ValueError("seller_uid must not be None or 0")

            self.set_seller(seller_uid=seller_uid)

        db.session.commit()

    def update_history(self, buyer_name, paid_amount):
        if not all(
            [
                isinstance(buyer_name, str),
                isinstance(paid_amount, int),
            ]
        ):
            raise ValueError("buyer_name must be str, paid_amount must be int")

        with open(ART_HISTORY_LOC, "r") as history_database:
            data = json.load(history_database)

        data[str(self.uid)]["price_history"].insert(0, paid_amount)
        data[str(self.uid)]["sale_history"].insert(
            0,
            {
                "buyer": buyer_name,
                "price": paid_amount,
                "sold_date": datetime.today().strftime("%m-%d-%y"),
            },
        )

        with open(ART_HISTORY_LOC, "w") as history_database:
            json.dump(data, history_database)

    def set_seller(self, seller_uid):
        self.seller = seller_uid
        db.session.commit()

    def set_bytestr_artpic(self, bytestr_artpic):
        with open(f"{ARTPIC_LOC}{self.uid}_base64.txt", "w") as outfile:
            outfile.write(bytestr_artpic)

    def __repr__(self):
        return f"ArtworkModel -- uid: {self.uid}, name: {self.name}"

    # In ArtworkJson: price_history, sale_history, provenance


class UserModel(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    mobile = db.Column(db.String(20), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    ranking = db.Column(db.Integer, nullable=False, default=0)
    bought = db.Column(db.BLOB, nullable=False, default=bytearray(set()))
    spend = db.Column(db.Integer, nullable=False, default=0)
    sold = db.Column(db.BLOB, nullable=False, default=bytearray(set()))
    saved = db.Column(db.BLOB, nullable=False, default=bytearray(set()))
    cart = db.Column(db.BLOB, nullable=False, default=bytearray(set()))

    def to_dict(self):
        return {
            "uid": self.uid,
            "email": self.email,
            "mobile": self.mobile,
            "username": self.username,
            "ranking": self.ranking,
            "bought": list(self.bought),
            "spend": self.spend,
            "sold": list(self.sold),
            "saved": list(self.saved),
            "cart": list(self.cart),
        }

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_saved(self):
        return list(self.saved)

    def add_to_saved(self, artwork_id):
        self.saved = set(self.saved)
        self.saved.add(artwork_id)

        self.saved = bytearray(self.saved)
        db.session.commit()

    def remove_from_saved(self, artwork_id):
        self.saved = set(self.saved)
        if artwork_id not in self.saved:
            raise KeyError(
                f"User does not save any artwork with id {artwork_id}"
            )

        self.saved.remove(artwork_id)

        self.saved = bytearray(self.saved)
        db.session.commit()

    def update_bought(self, bought_artwork_uid):
        self.bought = set(self.bought)
        self.bought.add(bought_artwork_uid)

        self.bought = bytearray(self.bought)
        db.session.commit()

        self.update_ranking()

    def update_spend(self, spend_amount):
        self.spend += spend_amount
        db.session.commit()

        self.update_ranking()

    def update_sold(self, sold_artwork_uid):
        self.sold = set(self.sold)
        self.sold.add(sold_artwork_uid)

        self.sold = bytearray(self.sold)
        db.session.commit()

        self.update_ranking()

    def update_ranking(self):
        user_points = 1.5 * len(self.bought) + 0.00001 * self.spend
        user_points += 0.75 * len(self.sold)

        # generate by recursively point += 50 * i ** (i / 2.5), start point = 0
        min_ranking_points = [0, 50, 137, 323, 783, 2033, 5719, 17340]

        ranking = 8
        for i in range(len(min_ranking_points)):
            if user_points < min_ranking_points[i]:
                ranking = i
                break

        self.ranking = ranking
        db.session.commit()


class InvitationCodeModel(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    available_code = db.Column(db.String(20), nullable=False, unique=True)
