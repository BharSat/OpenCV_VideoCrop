from cv2 import *
import numpy as np


class VideoCropper:
    current_frame = None

    def __init__(self, file, ROI=None):
        self.file = file
        self.capture = VideoCapture(file)
        self.read_frames = []
        if not ROI:
            self.ask_ROI()
        elif type(ROI) is str:
            if ROI == '1/4':
                ROI = [0, int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)//4), 0, int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)//4)]
            elif ROI == '1/2':
                ROI = [0, int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)//2), 0, int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)//2)]
            elif ROI == '1/8':
                ROI = [0, self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)//8, 0, self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)//8]
            elif ROI == 'LT':
                ROI = [0, int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)//2), 0, int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)//2)]
            elif ROI == 'RT':
                ROI = [int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)//2), int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)), 0, int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)//2)]
            elif ROI == 'LB':
                ROI = [0, int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)//2), int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)//2), int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))]
            elif ROI == 'RB':
                ROI = [int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)//2), int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)//2), int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))]
        self.ROI = ROI
        self.points = []
        self.can_cut = False

    def reset(self):
        self.capture.release()
        self.capture = VideoCapture(self.file)
        self.read_frames = []

    def next_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return None
        elif ret:
            self.current_frame = frame
            self.read_frames.append(frame)
            ROI = self.ROI
            new_frame = frame[ROI[0]:ROI[1], ROI[2]:ROI[3]]
            return new_frame

    def release(self):
        self.capture.release()

    def ask_ROI(self):
        if not self.current_frame:
            self.current_frame = self.capture.read()[1]
        cv2.namedWindow('Image Cropper')
        cv2.setMouseCallback('Image Cropper', lambda *args: self._record_points(args[0], args[1], args[2]))
        cv2.imshow('Image Cropper', self.current_frame)
        k = cv2.waitKey(0)
        if k == ord('c') and self.can_cut:
            points = self.points
            final = self.current_frame[points[1]:points[3], points[0]:points[2]]
            self.ROI = [points[1], points[3], points[0], points[2]]
        else:
            final = self.current_frame
        cv2.destroyAllWindows()
        return final

    def _record_points(self, event, x, y):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append(int(x))
            self.points.append(int(y))
            print(x, y)
            if len(self.points) == 4:
                new_frame = cv2.rectangle(self.current_frame, pt1=(int(self.points[0]), int(self.points[1])), pt2=(int(self.points[2]), int(self.points[3])), color=(100, 255, 20), thickness=4)
                self.can_cut = True
                cv2.imshow('to crop', new_frame)
                cv2.waitKey(0)
            elif len(self.points) > 4:
                self.points = []

    def list_frames(self):
        self.reset()
        frames = []
        while 1:
            frame = self.next_frame()
            if not frame:
                break
            elif frame:
                frames.append([frame])
        return np.array(frames, dtype=np.uint8)


if __name__ == '__main__':
    cropper = VideoCropper('../Gun.mp4', '1/2')
    crop1 = cropper.ask_ROI()
    cv2.imshow('cropped', crop1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
