import cv2
import tensorflow as tf
import numpy as np

from local_peak_finding import find_local_peaks


class InferenceEngine:
    """
    Class for performing inference on frames.
    """
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path, compile=False)

    def make_inference(self, X: np.ndarray):
        """

        :param X: frame represented as numpy array
        :return: Heatmap of predicted position of objects
        """
        X = np.expand_dims(X, axis=0).astype("float32") / 255.0
        X = tf.image.resize(X, size=[512, 512])
        Y = self.model.predict(X)
        return Y

    @staticmethod
    def find_local_peaks(img, heatmap, threshold=0.2):
        """
        Returns position of local peaks from heatmap
        :param img: frame from video
        :param heatmap: predicted heatmap
        :param threshold: Threshold to determine if a point should be considered a peak
        :return: position of peaks
        """
        heatmap = cv2.resize(heatmap.squeeze(), img.squeeze().shape)
        heatmap = heatmap.reshape((1, heatmap.shape[0], heatmap.shape[1], 1))
        return find_local_peaks(img=heatmap, threshold=threshold)


def test():
    from VideoDecoder import VideoDecoder
    from local_peak_finding import find_local_peaks
    ie = InferenceEngine(model_path='models/best_model.h5')

    decoder = VideoDecoder(path='data/test_clip.15s.mp4')
    for i, frame in enumerate(decoder.decode()):
        v = ie.make_inference(X=frame)
        peak_points, peak_vals, peak_sample_inds, peak_channel_inds = find_local_peaks(img=v)
        print('!')


if __name__ == '__main__':
    test()
