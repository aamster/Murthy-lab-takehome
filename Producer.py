import logging

import zmq

from VideoDecoder import VideoDecoder

log = logging.getLogger(__name__)


class Producer:
    """
    Producer class for generating frames from a video.
    """
    def __init__(self, sender_port, video_path):
        self.sender_port = sender_port
        self.video_path = video_path

    def run(self):
        """
        Iterates through each frame in video and sends downstream for processing.
        :return: None
        """
        context = zmq.Context()
        sender = context.socket(zmq.PUSH)
        sender.bind(f'tcp://*:{self.sender_port}')

        decoder = VideoDecoder(path=self.video_path)
        n_frames = decoder.get_n_frames()
        for i, frame in enumerate(decoder.decode()):
            # log.debug(f'PRODUCER: Sending frame {i} to consumer')
            sender.send_pyobj((frame, i, n_frames))
