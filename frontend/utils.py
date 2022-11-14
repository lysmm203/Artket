import base64 as b64
import io

from PIL import Image

ARTPIC_LOC = "instance/artpic/"


def convert_artpic_to_base64str(artwork_uid, artpic_path):
    byte_arr = io.BytesIO()

    # reads and convert PIL img to jpeg and store in byte arr
    pil_img = Image.open(artpic_path, mode='r')
    pil_img = pil_img.convert("RGB")
    pil_img.save(byte_arr, format="JPEG")

    # encode as base64
    encoded_img = b64.encodebytes(byte_arr.getvalue()).decode('ascii')

    with open(f"{ARTPIC_LOC}{artwork_uid}_base64.txt", "w") as outfile:
        outfile.write(encoded_img)
