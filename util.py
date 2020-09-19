import io
from base64 import encodebytes

import cv2


def encode_img_to_data_url(img):
    is_success, buffer = cv2.imencode('.jpg', img)
    io_buf = io.BytesIO(buffer)
    encoded_img = encodebytes(io_buf.getvalue()).decode('ascii')
    data_url = f'data:image/jpeg;base64,{encoded_img}'
    return data_url