import logging

import zmq

from InferenceEngine import InferenceEngine

log = logging.getLogger(__name__)

class Consumer:
    """
    Consumer class for processing frames from video.
    """
    def __init__(self, receiver_port, sender_port, model_path, local_peak_threshold=0.2):
        self.receiver_port = receiver_port
        self.sender_port = sender_port
        self.model_path = model_path
        self.local_peak_threshold = local_peak_threshold

    def run(self):
        """
        Loops forever listening for frames. When received performs inference on the frame
        :return: None
        """
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
            log.debug(f'CONSUMER: Made pred for frame {frame_idx}')

            log.debug(f'CONSUMER: Start find local peaks frame {frame_idx}')
            peak_points, _, _, _ = inference_engine.find_local_peaks(img=X, heatmap=preds,
                                                                     threshold=self.local_peak_threshold)
            log.debug(f'CONSUMER: End find local peaks frame {frame_idx}')

            log.debug(f'CONSUMER: Sending results for frame {frame_idx} to result collector...')
            sender.send_pyobj((X, peak_points, frame_idx, n_frames))

