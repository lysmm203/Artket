from flask_sqlalchemy import SQLAlchemy

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

    def update_is_sold(self):
        self.is_sold = not self.is_sold
        db.session.commit()

    def get_seller_uid(self):
        return self.seller

    def get_min_value(self):
        return self.min_value

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

    def get_password(self):
        return self.password

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
        pass

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


class InvitationCodeModel(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    available_code = db.Column(db.String(20), nullable=False, unique=True)
