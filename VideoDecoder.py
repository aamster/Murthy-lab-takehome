import cv2


class VideoDecoder:
    """
    Class for reading video
    """
    def __init__(self, path):
        self.reader = cv2.VideoCapture(path)

    def decode(self):
        """
        Iterates through video and yields frames
        :return: Generator yielding frames
        """
        success = True
        while success:
            success, img = self.reader.read()
            if success:
                img = img[:, :, :1]  # convert to grayscale
                yield img

    def get_n_frames(self):
        """

        :return: Number of frames in video
        """
        return int(self.reader.get(cv2.CAP_PROP_FRAME_COUNT))

def main():
    vd = VideoDecoder(path='data/test_clip.15s.mp4')
    for i, frame in enumerate(vd.decode()):
        print(i, frame.shape)


if __name__ == '__main__':
    main()