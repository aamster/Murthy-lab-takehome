import argparse
import json
import logging
import os
from multiprocessing import Process

from flask import Flask, request, Response, render_template, send_file, jsonify

from Consumer import Consumer
from Producer import Producer
from ResultCollector import ResultCollector
from util import encode_img_to_data_url

"""
Entry point for application. 
Starts webserver.
Starts inference server.
"""

app = Flask(__name__, static_folder='frontend/static', template_folder='frontend/templates')

parser = argparse.ArgumentParser()
parser.add_argument('consumer_send_port')
parser.add_argument('producer_send_port')
parser.add_argument('-n_servers', default=1, type=int, required=False)
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s')

log = logging.getLogger(__name__)

for _ in range(args.n_servers):
    consumer = Consumer(model_path='models/best_model.h5', receiver_port=args.producer_send_port,
                        sender_port=args.consumer_send_port)
    Process(target=consumer.run).start()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate_predictions')
def generate_predictions():
    """
    Spawns a producer which reads video frames and result collector to yield results.
    Iterates through result collector and yields results to client as they are available
    Uses event-stream to keep connection open.
    
    :return: Flask response (event-stream)
    """
    video_name = request.args.get('video_name')

    producer = Producer(sender_port=args.producer_send_port, video_path=f'data/{video_name}')
    Process(target=producer.run).start()

    result_collector = ResultCollector(receiver_port=args.consumer_send_port)

    def generate():
        try:
            for frame_idx, img, peak_points in result_collector.run():
                img_data_url = encode_img_to_data_url(img=img)
                peak_points = peak_points.numpy().tolist()
                res = json.dumps({'img': img_data_url, 'peak_points': peak_points, 'frame_idx': frame_idx})
                yield f'data: {res}\n\n'
            yield 'event: done\ndata: {}\n\n'
        except GeneratorExit:
            log.debug('APP: Client closed connection')
    return Response(generate(), mimetype='text/event-stream')


@app.route('/get_available_videos')
def get_available_videos():
    """
    :return: Available video files (assumed to be in data directory)
    """
    videos = os.listdir('data')
    videos = [v for v in videos if os.path.splitext(v)[-1] == '.mp4']
    return jsonify(videos)


if __name__ == '__main__':
    app.run()
