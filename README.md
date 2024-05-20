# Simple Multi-threaded Video Streaming Server

## Overview
This project provides a simple multi-threaded web server implemented in Python for streaming video from multiple cameras connected to the server. The video streams are transmitted via WebSocket, and the server also includes face detection functionality using the OpenCV library.

## Reference
https://gist.github.com/arvind-iyer/90cd941d0885f422bdf90905d86f9e04

## Features
- **WebSocket Transmission:** Real-time video streaming to clients using WebSocket.
- **Face Detection:** Uses OpenCV for detecting faces in the video streams.
- **Multiple Camera Support:** Can handle multiple camera inputs simultaneously.

## Requirements
- Python 3.x
- OpenCV
- WebSocket

## Installation
1. Clone the repository:
   - `git clone https://github.com/ilushinvanya/video-surveillance.git`
   - `cd video-surveillance`

2. Install the required dependencies: `pip install -r requirements.txt`

## Usage
1. Connect your cameras to the server.
2. Run the server `python ./server.py`
   - Will run on localhost on port 8765, default `ws://127.0.0.1:8765/media/0`
     - 127.0.0.1 - server ip address
     - 8765 - port specified when starting the server
     - media - path
     - 0 - index of the cameras that the server recognized; if there are several cameras, they will be available with the values 1,2,3...

3. Open the `client.html` file, the default server address will be written in the input field to view the video streams.
4. Open the `index.html` file, for multi-camera viewing mode, you can add several copies of the client.html file.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

