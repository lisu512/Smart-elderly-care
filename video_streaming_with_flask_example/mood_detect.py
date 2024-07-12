import time
import uuid

import cv2
from fer import FER

from FaceRecognitionSystem import FaceRecognizer
from models import Event
from utils import get_DroidCam_url


class MoodDetect(object):
    def __init__(self):
        self.video = cv2.VideoCapture(get_DroidCam_url())
        # self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.emotion_detector = FER(mtcnn=True)  # 使用更快的Haar Cascade检测器
        self.skip_frames = 30  # 每30帧进行一次识别
        self.frame_count = 0
        self.last_emotions = []
        self.last_face_locations = []
        self.last_names = []
        self.last_save_time = 0
        self.face_recognizer = FaceRecognizer()

    def __del__(self):
        self.video.release()

    def process_frame(self, image):
        if self.frame_count % self.skip_frames == 0:
            self.last_names, self.last_face_locations = self.face_recognizer.detect_and_recognize_face(image)
        for (top, right, bottom, left), name in zip(self.last_face_locations, self.last_names):
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(image, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        return image

    def get_face_frame(self):
        success, image = self.video.read()
        if not success:
            return None
        self.frame_count += 1
        if self.frame_count % self.skip_frames == 0:
            self.last_names, self.last_face_locations = self.face_recognizer.detect_and_recognize_face(image)
        for (top, right, bottom, left), name in zip(self.last_face_locations, self.last_names):
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(image, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            current_time = time.time()
            if current_time - self.last_save_time >= 5 * 60:  # 检查是否超过5分钟
                file_name = str(uuid.uuid4()) + '.jpg'
                cv2.imwrite(file_name, image)
                print('Unknow person detected')
                Event.create('陌生人', '走廊', file_name)
                self.last_save_time = current_time  # 更新时间戳
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_mood_frame(self):
        success, image = self.video.read()
        if not success:
            return None
        self.frame_count += 1
        if self.frame_count % self.skip_frames == 0:
            # 每隔几帧进行一次情感识别
            emotions = self.emotion_detector.detect_emotions(image)
            self.last_emotions = emotions
        else:
            emotions = self.last_emotions
        for face in emotions:
            bounding_box = face["box"]
            emotions = face["emotions"]
            dominant_emotion = max(emotions, key=emotions.get)
            (x, y, w, h) = bounding_box
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(image, dominant_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            # 如果心情不好，保存图片
            if dominant_emotion in ['fear', 'sad', 'angry']:
                current_time = time.time()
                if current_time - self.last_save_time >= 5 * 60:
                    save_image = self.process_frame(image)
                    file_name = str(uuid.uuid4()) + '.jpg'
                    cv2.imwrite(file_name, save_image)
                    print('Bad mood detected:' + dominant_emotion)
                    Event.create('心情不好', '房间', file_name)
                    self.last_save_time = current_time  # 更新时间戳

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
