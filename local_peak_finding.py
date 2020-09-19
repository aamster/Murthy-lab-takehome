import tensorflow as tf
from typing import Tuple

#https://github.com/murthylab/sleap/blob/master/sleap/nn/data/inference.py#L331
def find_local_peaks(
    img: tf.Tensor, threshold: float = 0.2
) -> Tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    """Find local maxima via non-maximum suppresion.

    Args:
        img: Tensor of shape (samples, height, width, channels).
        threshold: Scalar float specifying the minimum confidence value for peaks. Peaks
            with values below this threshold will not be returned.

    Returns:
        A tuple of (peak_points, peak_vals, peak_sample_inds, peak_channel_inds).

        peak_points: float32 tensor of shape (n_peaks, 2), where the last axis
        indicates peak locations in xy order.

        peak_vals: float32 tensor of shape (n_peaks,) containing the values at the peak
        points.

        peak_sample_inds: int32 tensor of shape (n_peaks,) containing the indices of the
        sample each peak belongs to.

        peak_channel_inds: int32 tensor of shape (n_peaks,) containing the indices of
        the channel each peak belongs to.
    """
    # Build custom local NMS kernel.
    kernel = tf.reshape(
        tf.constant([[0, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=tf.float32), (3, 3, 1)
    )

    # Reshape to have singleton channels.
    height = tf.shape(img)[1]
    width = tf.shape(img)[2]
    channels = tf.shape(img)[3]
    flat_img = tf.reshape(tf.transpose(img, [0, 3, 1, 2]), [-1, height, width, 1])

    # Perform dilation filtering to find local maxima per channel and reshape back.
    max_img = tf.nn.dilation2d(
        flat_img, kernel, [1, 1, 1, 1], "SAME", "NHWC", [1, 1, 1, 1]
    )
    max_img = tf.transpose(
        tf.reshape(max_img, [-1, channels, height, width]), [0, 2, 3, 1]
    )

    # Filter for maxima and threshold.
    argmax_and_thresh_img = (img > max_img) & (img > threshold)

    # Convert to subscripts.
    peak_subs = tf.where(argmax_and_thresh_img)

    # Get peak values.
    peak_vals = tf.gather_nd(img, peak_subs)

    # Convert to points format.
    peak_points = tf.cast(tf.gather(peak_subs, [2, 1], axis=1), tf.float32)

    # Pull out indexing vectors.
    peak_sample_inds = tf.gather(peak_subs, 0, axis=1)
    peak_channel_inds = tf.gather(peak_subs, 3, axis=1)

    return peak_points, peak_vals, peak_sample_inds, peak_channel_inds