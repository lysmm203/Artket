import base64 as b64
import io

from PIL import Image


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
