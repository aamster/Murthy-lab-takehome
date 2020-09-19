import cv2
import numpy as np
import plotly.express as px
import plotly
from PIL import Image


def save_for_plot(img, frame_idx):
    filename = f'output/{frame_idx}.jpg'
    cv2.imwrite(filename, img)
    return filename

def preprocess_for_plot(img, pred):
    img = img.squeeze()

    pred = pred.squeeze()
    pred = cv2.resize(pred, img.shape)

    # img = np.array(Image.fromarray(img).convert('RGB'))

    img = img.tolist()
    pred = pred.tolist()

    return img, pred
    # fig = px.imshow()
    # fig.add_heatmap(z=pred, opacity=0.5)
    # return plotly.io.to_html(fig)