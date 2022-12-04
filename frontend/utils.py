import base64 as b64
import io

from PIL import Image
from flask import url_for


def convert_artpic_to_base64str(artpic_path):
    byte_arr = io.BytesIO()

    # reads and convert PIL img to jpeg and store in byte arr
    pil_img = Image.open(artpic_path, mode="r")
    pil_img = pil_img.convert("RGB")
    pil_img.save(byte_arr, format="JPEG")

    # encode as base64
    encoded_img = b64.encodebytes(byte_arr.getvalue()).decode("ascii")

    return encoded_img


def get_missing_vars(var_names, var_values):
    missing_vars = list()
    for i, value in enumerate(var_values):
        if not value:
            missing_vars.append(var_names[i])

    return missing_vars


def get_session_redirect_from(session):
    if "redirect_from" in session:
        value = session["redirect_from"]
        session.pop("redirect_from", None)

        return value

    return None


def get_session_error_msg(session):
    if "error_msg" in session:
        value = session["error_msg"]
        session.pop("error_msg", None)

        return value

    return None


def redirect_signin_error(session, redirect_from, remember_redirect_from=True):
    site_name = url_for(redirect_from).replace("_", " ").replace("/", "")
    session["error_msg"] = f"You must login to see {site_name} site"

    if remember_redirect_from:
        session["redirect_from"] = redirect_from
