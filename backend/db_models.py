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
    is_sold = db.Column(db.Integer, nullable=False)  # 0 and 1 only

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

    def __repr__(self):
        return f"ArtworkModel -- uid: {self.uid}, name: {self.name}"

    # In ArtworkJson: price_history, sale_history, provenance


class UserModel(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "uid": self.uid,
            "email": self.email,
            "mobile": self.mobile,
            "password": self.password,
        }

    # In UserJson: saved, cart
