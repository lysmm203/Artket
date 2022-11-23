from datetime import datetime
from http import HTTPStatus as Hsta

from flask_restful import Resource, reqparse

import backend.db_models as dbm


def validate_buy_artwork_query(data_dict):
    required_keys_type = {
        "buyer_uid": int,
        "buyer_password": str,
        "artwork_uid": int,
        "card_number": int,
        "expire_date": str,
        "cvv_code": int,
        "paid_amount": int,
    }

    error_help_msg = (
        "All the following keys must be provided and can not be None or "
        'empty in "data" key in json kwargs of the query.\n'
        "- (as string type): buyer_password, expire_date\n"
        "- (as integer type): buyer_uid, artwork_uid, card_number, cvv_code"
        ", paid_amount\n"
    )
    if not data_dict.keys() >= required_keys_type.keys():
        return (
            False,
            {"error_msg": f"Missing keys.\n{error_help_msg}"},
            Hsta.BAD_REQUEST,
        )

    if not all(data_dict.values()):
        return (
            False,
            {
                "error_msg": (
                    "One or more value is empty, 0, or None"
                    f".\n{error_help_msg}"
                )
            },
            Hsta.BAD_REQUEST,
        )

    if not all(
        [
            type(data_dict[_key]) == required_keys_type[_key]
            for _key in data_dict
        ]
    ):
        return (
            False,
            {
                "error_msg": (
                    f"One or more value has wrong type.\n{error_help_msg}"
                )
            },
            Hsta.BAD_REQUEST,
        )

    return True, {"error_msg": ""}, Hsta.OK


def validate_payment_card(card_number, expire_date, cvv_code):
    # check cvv_code
    if cvv_code < 100 or cvv_code > 999:
        return False

    # check expire_date
    try:
        expire_date = datetime.strptime(expire_date, "%m/%y")
        curr_date = datetime.today()

        if (expire_date - curr_date).days < 0:
            return False

    except ValueError:
        return False

    # check card number: Luhn’s algorithm
    digits = [int(char) for char in str(card_number)]

    if digits[0] not in range(3, 7):
        return False

    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    checksum = sum(odd_digits)
    for num in even_digits:
        checksum += sum([int(char) for char in str(num * 2)])

    return (checksum % 10) == 0


def validate_data_for_buy_artwork(data_dict):
    # validate buyer data
    buyer = dbm.UserModel.query.filter_by(uid=data_dict["buyer_uid"]).first()
    if not buyer:
        error_msg = f'No user with uid {data_dict["buyer_uid"]}'
        return False, {"error_msg": error_msg}, Hsta.NOT_FOUND

    if buyer.get_password() != data_dict["buyer_password"]:
        error_msg = "Incorrect password for the seller account"
        return False, {"error_msg": error_msg}, Hsta.UNAUTHORIZED

    # validate artwork data and paid amount
    artwork = dbm.ArtworkModel.query.filter_by(
        uid=data_dict["artwork_uid"]
    ).first()
    if not artwork:
        error_msg = f'No artwork with uid {data_dict["artwork_uid"]}'
        return False, {"error_msg": error_msg}, Hsta.NOT_FOUND

    if artwork.get_is_sold() == 1:
        error_msg = (
            f'Artwork with uid {data_dict["artwork_uid"]} had been '
            "sold. Can not buy already sold artwork"
        )
        return False, {"error_msg": error_msg}, Hsta.UNAUTHORIZED

    if data_dict["paid_amount"] < artwork.get_min_value():
        error_msg = "Paid amount is smaller than artwork min value"
        return False, {"error_msg": error_msg}, Hsta.UNAUTHORIZED

    # validate payment card
    if not validate_payment_card(
        card_number=data_dict["card_number"],
        expire_date=data_dict["expire_date"],
        cvv_code=data_dict["cvv_code"],
    ):
        error_msg = f"Not a valid debit card or credit card"
        return False, {"error_msg": error_msg}, Hsta.PAYMENT_REQUIRED

    return True, {"error_msg": ""}, Hsta.OK


def buy_artwork(data_dict):
    is_valid, error_msg, status_code = validate_data_for_buy_artwork(data_dict)
    if not is_valid:
        return error_msg, status_code

    artwork = dbm.ArtworkModel.query.filter_by(
        uid=data_dict["artwork_uid"]
    ).first()

    buyer = dbm.UserModel.query.filter_by(uid=data_dict["buyer_uid"]).first()
    buyer.update_bought(data_dict["artwork_uid"])
    buyer.update_spend(data_dict["paid_amount"])

    seller = dbm.UserModel.query.filter_by(
        uid=artwork.get_seller_uid()
    ).first()
    seller.update_sold(data_dict["artwork_uid"])

    artwork.update_is_sold(sold=True)
    artwork.update_history(
        buyer_name=buyer.get_username(),
        paid_amount=data_dict["paid_amount"],
    )

    return {
        "msg": (
            "Successfully buy artwork "
            f'(artwork_uid: {data_dict["artwork_uid"]})'
        )
    }, Hsta.OK


class BuyArtwork(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="data", type=dict, required=True, location="json")

    def post(self):
        data = self.parser.parse_args()["data"]

        is_valid, error_msg, status_code = validate_buy_artwork_query(data)
        if not is_valid:
            return error_msg, status_code

        return buy_artwork(data)
