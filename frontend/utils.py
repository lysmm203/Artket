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
