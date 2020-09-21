import logging

import zmq

log = logging.getLogger(__name__)

class ResultCollector:
    """
    Class for receiving output of many servers
    """
    def __init__(self, receiver_port):
        self.receiver_port = receiver_port

    def run(self):
        """
        Iterates through all frames and returns frames in order.

        I.e server 1 processes frame 1 before server 2 processes frame 0,
        then frame 0 is ensured to return before frame 1

        :return: Generator yielding idx, image, and predicted peaks
        """
        context = zmq.Context()
        receiver = context.socket(zmq.PULL)
        receiver.bind(f'tcp://*:{self.receiver_port}')

        results = {}
        next_idx = 0
        n_frames = float('inf')

        while next_idx < n_frames:
            img, peak_points, frame_idx, n_frames = receiver.recv_pyobj()
            results[frame_idx] = (img, peak_points)
            while next_idx in results:
                img, peak_points = results[next_idx]
                del results[next_idx]
                log.debug(f'RESULT COLLECTOR: Returning results for {next_idx}')
                yield next_idx, img, peak_points
                next_idx += 1

