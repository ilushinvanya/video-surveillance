# Reference
# https://gist.github.com/arvind-iyer/90cd941d0885f422bdf90905d86f9e04

import websockets
import cv2
import threading
import time
import asyncio
import base64

face_Cascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")


class Camera(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.cap = cv2.VideoCapture(url)
        ret, self.frame = self.cap.read()
        self.last_frame_time = time.time()
        print(ret)

    def run(self):
        print('Started streaming from ' + str(self.url))
        self.frame_n = 0
        while True:
            self.frame_n += 1
            ret, frame = self.cap.read()
            self.last_frame_time = time.time()
            if not ret:
                print("error fetching stream")
                time.sleep(1)
                continue

            frame = cv2.resize(frame, (1280, 720))
            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_Cascade.detectMultiScale(
                img_gray,
                scaleFactor=1.1,
                minNeighbors=10,
                minSize=(30, 30)
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (155, 0, 0), 1)
            retval, buffer_img = cv2.imencode('.jpg', frame)
            self.frame = base64.b64encode(buffer_img)


def clear_capture(capture):
    capture.release()
    cv2.destroyAllWindows()


def get_available_cameras():
    available_cameras = {}

    for i in range(10):
        try:
            cap = cv2.VideoCapture(i)
            ret, frame = cap.read()
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            clear_capture(cap)
            available_cameras[str(i)] = i

        except:
            clear_capture(cap)
            break
    return available_cameras


cameras = {
    camera: Camera(url) for camera, url in get_available_cameras().items()
}


async def media_server(websocket, path):
    # accepted path: /media/<camera>
    if not path.startswith("/media/"):
        await websocket.send("invalid path")
        return
    camera = path.replace("/media/", "")
    print(f"streaming {camera} to {websocket}")
    last_frame_time = 0
    if camera in cameras:
        stream = cameras[camera]
        while True:
            # check for new frame
            if stream.last_frame_time > last_frame_time:
                last_frame_time = stream.last_frame_time
                # await websocket.send(f"recd frame {stream.frame_n}")
                await websocket.send(stream.frame)
            await asyncio.sleep(0.04)
    await websocket.send(f"bye bye {camera}")


if __name__ == "__main__":
    for cam in cameras.values():
        cam.start()
    start_server = websockets.serve(media_server, "0.0.0.0", 8765)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
