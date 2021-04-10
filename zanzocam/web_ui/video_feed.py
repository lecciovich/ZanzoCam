# Thanks to https://github.com/miguelgrinberg/flask-video-streaming

import io
import time
import picamera
import threading
import subprocess

try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident



class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """
    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()



class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    stop_camera = False
    event = CameraEvent()

    def __init__(self):
        """Start the background camera thread if it isn't running yet."""
        if Camera.thread is None:
            Camera.last_access = time.time()

            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        """Return the current camera frame."""
        Camera.last_access = time.time()

        # wait for a signal from the camera thread
        Camera.event.wait()
        Camera.event.clear()

        return Camera.frame

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')

        frames_iterator = cls.frames()
        for frame in frames_iterator:
            cls.frame = frame
            cls.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last second then stop the thread
            # FIXME this mechanism sadly doesn't work....
            if time.time() - cls.last_access > 1 or cls.stop_camera:
                frames_iterator.close()
                print('No requests received for more than 5 seconds.')
                break

        print("Stopping camera thread.")
        Camera.thread = None

    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                
                time.sleep(1/30)
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

    def video_streaming_generator(self):
        """
        Generates the stream of pictures for the camera video preview.
        """
        while not Camera.stop_camera:
            frame = self.get_frame()
            if frame:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
