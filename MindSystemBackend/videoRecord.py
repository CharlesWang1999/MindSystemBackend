import keyboard
import cv2
from threading import Thread


class VideoRecord:
    def __init__(self, record_camera_id):
        print("Getting camera...")
        self._camera_capture = cv2.VideoCapture(record_camera_id)
        if self._camera_capture.isOpened():
            print("Get camera success")
        else:
            print("Get camera FAIL!!!!!!!!!!!!!!!!!!!!")
        self._fps = 30
        self._size = (int(self._camera_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(self._camera_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    def _record_thread(self, save_file_path):
        print("Start camera record")
        video_writer = cv2.VideoWriter(save_file_path, cv2.VideoWriter_fourcc(
            'X', 'V', 'I', 'D'), self._fps, self._size)

        # use to test if camera work
        # index = 0
        while not self._stop_record:
            success, frame = self._camera_capture.read()
            if not success:
                print("record wrong!")
            else:
                video_writer.write(frame)
            #     if index % 100 == 0:
            #         cv2.imshow("test", frame)
            #         cv2.waitKey(25)
            # index = index + 1
        print("Stop camera record")
        video_writer.release()
        print(f'Camera record success to {save_file_path}')

    def start_record(self, saveFilePath):
        self._stop_record = False
        self._current_record_thread = Thread(name='camera record thread',
                                             target=self._record_thread, args=(saveFilePath,))
        self._current_record_thread.start()

    def stop_record(self):
        self._stop_record = True
        self._current_record_thread.join()


if __name__ == "__main__":
    record_camera_id = 0
    save_file_path = './test.avi'
    video_record = VideoRecord(record_camera_id)
    video_record.start_record(save_file_path)
    keyboard.wait('enter')
    video_record.stop_record()
