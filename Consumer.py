import logging

import zmq

from InferenceEngine import InferenceEngine

log = logging.getLogger(__name__)

class Consumer:
    def __init__(self, receiver_port, sender_port, model_path):
        self.receiver_port = receiver_port
        self.sender_port = sender_port
        self.model_path = model_path

    def run(self):
        context = zmq.Context()
        receiver = context.socket(zmq.PULL)
        receiver.connect(f'tcp://localhost:{self.receiver_port}')

        sender = context.socket(zmq.PUSH)
        sender.connect(f'tcp://localhost:{self.sender_port}')

        inference_engine = InferenceEngine(model_path=self.model_path)

        while True:
            X, frame_idx, n_frames = receiver.recv_pyobj()
            log.debug(f'CONSUMER: Received frame {frame_idx} from producer')
            preds = inference_engine.make_inference(X=X)
            log.debug(f'CONSUMER: Made pred for frame {frame_idx}. Sending to result collector...')
            sender.send_pyobj((X, preds, frame_idx, n_frames))
            # print(f'CONSUMER: Sent pred for frame {frame_idx} to result collector')

