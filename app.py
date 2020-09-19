import argparse
import json
import logging
from multiprocessing import Process

from flask import Flask, request, Response, render_template, send_file

from Consumer import Consumer
from Producer import Producer
from ResultCollector import ResultCollector
from plotting import preprocess_for_plot, save_for_plot

app = Flask(__name__, static_folder='frontend/static', template_folder='frontend/templates')

parser = argparse.ArgumentParser()
parser.add_argument('consumer_send_port')
parser.add_argument('producer_send_port')
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s')

log = logging.getLogger(__name__)

for _ in range(1):
    consumer = Consumer(model_path='models/best_model.h5', receiver_port=args.producer_send_port,
                        sender_port=args.consumer_send_port)
    Process(target=consumer.run).start()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate_predictions')
def generate_predictions():
    video_name = request.args.get('video_name')

    producer = Producer(sender_port=args.producer_send_port, video_path=f'data/{video_name}')
    Process(target=producer.run).start()

    result_collector = ResultCollector(receiver_port=args.consumer_send_port)

    def generate():
        for frame_idx, img, pred in result_collector.run():
            img_filename = save_for_plot(img=img, frame_idx=frame_idx)
            res = json.dumps({'filename': img_filename, 'frame_idx': frame_idx})
            yield f'data: {res}\n\n'
    return Response(generate(), mimetype='text/event-stream')


@app.route('/get_image')
def get_image():
    filename = request.args.get('filename')
    return send_file(filename, as_attachment=True, mimetype='image/jpeg')



if __name__ == '__main__':
    app.run()
