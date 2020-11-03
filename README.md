# Interactive model inference

This implements task A: A server that can interactively perform model inference

The overall architecture is:

1. A Flask webserver listens for requests to endpoints
2. When a user queries the /generate_predictions endpoint, it yields a frame and the predicted positions as obtained from local peak finding of the predicted histogram.
3. The results from this endpoint are streamed back to the browser via an event-stream. This keeps the request open for the duration of the request. The results are then plotted using Plotly.

The architecture for performing inference on the video is:
1. A client iterates through a video and yields frames
2. One or many servers listens for incoming batches of frames (currently only 1 frame at a time)
3. A result collector listens for completed inferences, and yields the results in frame order.

## To Run
1. `conda env create -f env.yml`
2. Place video files in a directory called "data". Place model file in directory called "models" (assumes it is called "best_model.h5") off of the root project directory.
3. `python app.py -consumer_send_port <consumer_send_port> -producer_send_port <producer_send_port> -n_servers <n_servers>`
4. Navigate to http://localhost:5000/ and click the "start" button.


The library pyzmq is used for interprocess communication, as suggested.

The client and server run in separate processes. The communication pattern is PUSH-PULL-PUSH-PULL

This has the advantage that as soon as a server is ready, it consumes the batch and starts inference, and the client doesn't block.

## Overall architecture
![Image of overall architecture](https://docs.google.com/drawings/d/e/2PACX-1vQA1avL0E01EzgO2Yg2XG-gA3Xehpl95DRKm7jlq_b4L5QdE5OmRN8hDZegJOdZnSGR1B0N7MsXAwhs/pub?w=960&h=720)

## Architecture for generating predictions
![Image of generate predictions](https://docs.google.com/drawings/d/e/2PACX-1vTXa-MkTo3R7cwMOGVVEvvrKQU0bPVfd-fsorkQV3SWsSiwLe_KwUaTXy4y4JeTYe715YB9frIGtkhE/pub?w=960&h=720)

## Example of running app
Predictions displayed as Xs.
![Image of app](https://docs.google.com/drawings/d/e/2PACX-1vTnH-SmLuhEyqjzL5s1W1JSmjJsrXXRVDvamLKJ_u2p9qH47ahCFIP__a5LsiPMK7JnsQmjbXekt3Me/pub?w=960&h=720)
