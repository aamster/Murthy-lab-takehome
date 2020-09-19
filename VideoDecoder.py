import cv2


class VideoDecoder:
    def __init__(self, path):
        self.reader = cv2.VideoCapture(path)

    def decode(self):
        success = True
        while success:
            success, img = self.reader.read()
            if success:
                img = img[:, :, :1]  # convert to grayscale
                yield img

    def get_n_frames(self):
        return int(self.reader.get(cv2.CAP_PROP_FRAME_COUNT))

def main():
    vd = VideoDecoder(path='data/test_clip.15s.mp4')
    for i, frame in enumerate(vd.decode()):
        print(i, frame.shape)


if __name__ == '__main__':
    main()