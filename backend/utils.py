import base64 as b64
import glob
import io

from PIL import Image


def get_bytestr_artpic(artwork_uid):
    """
    :param artwork_uid: (int) uid of the artwork
    :return: base64 str repr the picture of the art
    """
    byte_arr = io.BytesIO()
    artpic_path = glob.glob(f"instance/{artwork_uid}" + '*')[0]

    # reads and convert PIL img to jpeg and store in byte arr
    pil_img = Image.open(artpic_path, mode='r')
    pil_img = pil_img.convert("RGB")
    pil_img.save(byte_arr, format="JPEG")

    # encode as base64
    encoded_img = b64.encodebytes(byte_arr.getvalue()).decode('ascii')

    return encoded_img
