import cv2
import plotly.express as px
from PIL import Image

from Producer import Producer
from Consumer import Consumer

from multiprocessing import Process

from ResultCollector import ResultCollector


def plot_fig(frame_idx, img, pred):
    img = img.squeeze()
    img = img.astype('float32')
    pred = pred.squeeze()
    pred = cv2.resize(pred, img.shape)
    fig = px.imshow(Image.fromarray(img).convert('RGB'))
    fig.add_heatmap(z=pred, opacity=0.5)


    import matplotlib
    matplotlib.use('Agg')

    import matplotlib.pyplot as plt

    plt.clf()
    fig = plt.figure(figsize=(8, 8))
    plt.imshow(img.squeeze(), cmap="gray")
    plt.imshow(
        pred.squeeze(),
        extent=[
            -0.5,
            img.shape[1] - 0.5,
            img.shape[0] - 0.5,
            -0.5,
        ],  # (left, right, top, bottom),
        alpha=0.5
    )
    plt.xlim([200, 700])
    plt.ylim([900, 400])
    plt.savefig(f'output/{frame_idx}.png')
    plt.close(fig)


def main():
    import time

    producer_send_port = '5557'
    consumer_send_port = '5558'

    start = time.time()


    print(f'START: {time.time()}')
    producer = Producer(sender_port=producer_send_port, video_path='data/test_clip.15s.mp4')
    Process(target=producer.run).start()

    result_collector = ResultCollector(receiver_port=consumer_send_port)
    for frame_idx, img, pred in result_collector.run():
        plot_fig(frame_idx=frame_idx, img=img, pred=pred)
    end = time.time()

    print(end - start)


if __name__ == '__main__':
    main()