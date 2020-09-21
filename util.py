import io
from base64 import encodebytes
import numpy as np

import cv2


def encode_img_to_data_url(img: np.ndarray):
    """
    Encodes image as Base64 URL
    :param img: input image
    :return: Base64 encoded image
    """
    is_success, buffer = cv2.imencode('.jpg', img)
    io_buf = io.BytesIO(buffer)
    encoded_img = encodebytes(io_buf.getvalue()).decode('ascii')
    data_url = f'data:image/jpeg;base64,{encoded_img}'
    return data_url