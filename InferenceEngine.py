import tensorflow as tf
import numpy as np


class InferenceEngine:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path, compile=False)

    def make_inference(self, X):
        X = np.expand_dims(X, axis=0).astype("float32") / 255.0
        X = tf.image.resize(X, size=[512, 512])
        Y = self.model.predict(X)
        return Y


def test():
    from VideoDecoder import VideoDecoder
    ie = InferenceEngine(model_path='models/best_model.h5')

    decoder = VideoDecoder(path='data/test_clip.15s.mp4')
    for i, frame in enumerate(decoder.decode()):
        ie.make_inference(X=frame)
        print(i)


if __name__ == '__main__':
    test()
