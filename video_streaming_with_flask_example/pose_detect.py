import math
import time
import uuid

import cv2
import mediapipe as mp

from utils import get_DroidCam_url
from models import Event


class PoseDetect(object):
    def __init__(self):
        self.video = cv2.VideoCapture(get_DroidCam_url())
        # self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.pose_detector = PoseDetector()
        self.last_save_time = 0
        self.frame_counter = 0

    def __del__(self):
        self.video.release()

    def get_pose_frame(self):
        success, image = self.video.read()
        if not success:
            return None
        image, results = self.pose_detector.process_frame(image)
        self.frame_counter += 1  # 帧计数器加1
        if self.frame_counter >= 30:  # 每30帧检测一次
            # 检测摔倒
            if self.pose_detector.detect_fall(results):
                cv2.putText(image, 'Fall detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                # 捕捉摔倒的图片
                current_time = time.time()
                if current_time - self.last_save_time >= 5 * 60:  # 检查是否超过5分钟
                    file_name = str(uuid.uuid4()) + '.jpg'
                    cv2.imwrite(file_name, image)
                    print('Fall')
                    Event.create('fall', '走廊', file_name)
                    self.last_save_time = current_time  # 更新时间戳
            self.frame_counter = 0  # 重置帧计数器
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


class PoseDetector:
    def __init__(self, static_image_mode=False, model_complexity=2, smooth_landmarks=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 min_detection_confidence=0.6, min_tracking_confidence=0.6):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(static_image_mode, model_complexity, smooth_landmarks,
                                      enable_segmentation, smooth_segmentation,
                                      min_detection_confidence, min_tracking_confidence)

    def detect_pose(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        return results

    def draw_pose(self, image, results):
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return image

    def process_frame(self, frame):
        results = self.detect_pose(frame)
        frame = self.draw_pose(frame, results)
        return frame, results

    def detect_fall(self, results):
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            nose = landmarks[self.mp_pose.PoseLandmark.NOSE]
            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP]
            left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE]
            right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE]

            # 计算身体倾斜角度
            body_angle = math.atan2(right_hip.y - left_hip.y, right_hip.x - left_hip.x)
            body_angle = math.degrees(body_angle)

            # 计算头部和脚踝的垂直距离
            head_ankle_distance = min(abs(nose.y - left_ankle.y), abs(nose.y - right_ankle.y))
            # 判断是否跌倒
            if abs(body_angle) > 45 and head_ankle_distance < 0.3:
                return True
        return False
