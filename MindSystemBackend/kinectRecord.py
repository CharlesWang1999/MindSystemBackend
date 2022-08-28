from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import cv2
import numpy as np
import keyboard
from threading import Thread


class KinectRecord:
    def __init__(self):
        print('Getting Kinect camera...')
        self._kinect = PyKinectRuntime.PyKinectRuntime(
            PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        print('Get Kinect camera success')
        self._fps = 30
        self._size = (1920, 1080)
        self._frame = np.zeros((1080, 1920, 3))

    def _draw_color_frame(self, frame):
        cv2.imshow("kinect", frame)
        cv2.waitKey(25)

    def _reshape_origin_kinect_frame(self, frame):
        return np.reshape(frame, [1080, 1920, 4])[:, :, 0:3]

    def _record_thread(self, save_file_path):
        print('Start Kinect record!')
        video_writer = cv2.VideoWriter(save_file_path, cv2.VideoWriter_fourcc(
            'X', 'V', 'I', 'D'), self._fps, self._size)

        # use to test if kinect work
        # index = 0

        while not self._stopRecord:

            if self._kinect.has_new_color_frame():
                self._frame = self._reshape_origin_kinect_frame(
                    self._kinect.get_last_color_frame())
            video_writer.write(self._frame)
            # if index % 100 == 0:
            #     self._draw_color_frame(self._frame)
            # index = index + 1
        print('Stop Kinect record!')
        video_writer.release()
        print(f'Kinect record success to {save_file_path}')

    def start_record(self, save_file_path):
        self._stopRecord = False
        self._current_record_thread = Thread(
            name='kinect record thread',
            target=self._record_thread,
            args=(save_file_path, )
        )
        self._current_record_thread.start()

    def stop_record(self):
        self._stopRecord = True
        self._current_record_thread.join()


if __name__ == "__main__":
    kinect_record = KinectRecord()
    index = 0
    while True:
        save_file_path = f'./kinect{index}.avi'
        kinect_record.start_record(save_file_path)
        keyboard.wait('enter')
        video = kinect_record.stop_record()
        index = index + 1
