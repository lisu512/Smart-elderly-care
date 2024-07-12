import time
import uuid

import cv2
from ultralytics import YOLO

from models import Event
from utils import get_DroidCam_url


class ObjectDetect(object):
    def __init__(self):
        self.video = cv2.VideoCapture(get_DroidCam_url())
        # 加载YOLOv5模型
        self.model = YOLO('yolov5nu.pt')
        self.conf_threshold = 0.25  # 置信度阈值
        self.frame_count = 0
        self.detection_interval = 30  # 每30帧检测一次
        self.last_results = None  # 存储上一次的检测结果
        self.last_save_time = 0

    def __del__(self):
        self.video.release()

    def detect_objects(self, frame):
        self.frame_count += 1
        # 每30帧进行一次检测
        if self.frame_count % self.detection_interval == 0:
            results = self.model(frame)
            self.last_results = results
        elif self.last_results is None:
            # 如果还没有检测结果，就进行一次检测
            results = self.model(frame)
            self.last_results = results
        else:
            # 使用上一次的检测结果
            results = self.last_results

        # 处理检测结果
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                if conf > self.conf_threshold:
                    if self.model.names[cls] == 'person':
                        current_time = time.time()
                        if current_time - self.last_save_time >= 5 * 60:
                            file_name = str(uuid.uuid4()) + '.jpg'
                            cv2.imwrite(file_name, frame)
                            print('Person detected, image saved: ', file_name)
                            Event.create('有人进入', '禁区', file_name)
                            self.last_save_time = current_time
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    label = f'{self.model.names[cls]} {conf:.2f}'
                    # 为不同的类别选择不同的颜色
                    color = (int(255 * (cls % 3) / 3), int(255 * (cls % 2) / 2), int(255 * (1 - cls % 3) / 3))
                    # 绘制边界框
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    # 添加标签
                    t_size = cv2.getTextSize(label, 0, fontScale=0.6, thickness=1)[0]
                    c2 = x1 + t_size[0], y1 - t_size[1] - 3
                    cv2.rectangle(frame, (x1, y1), c2, color, -1, cv2.LINE_AA)  # filled
                    cv2.putText(frame, label, (x1, y1 - 2), 0, 0.6, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)
        return frame

    def get_object_frame(self):
        success, frame = self.video.read()
        if not success:
            return None
        # 物体检测
        frame = self.detect_objects(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
