import json

ARTPIC_LOC = "instance/artpic/"
ART_HISTORY_LOC = "instance/history.json"


def get_bytestr_artpic(artwork_uid):
    """
    :param artwork_uid: (int) uid of the artwork
    :return: base64 str repr the picture of the art
    """
    with open(f"{ARTPIC_LOC}{artwork_uid}_base64.txt", "r") as infile:
        return infile.read()


def get_artwork_history(artwork_uid):
    """
    :param artwork_uid: (int) uid of the artwork
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
    with open(ART_HISTORY_LOC) as history_database:
        data = json.load(history_database)
        return data[str(artwork_uid)]
