import cv2
import face_recognition
import os
import pickle

import numpy as np


class FaceRecognizer:
    def __init__(self, encodings_file='face_encodings.pkl'):
        self.known_face_encodings = []
        self.known_face_names = []
        self.encodings_file = encodings_file
        self.load_encodings()

    def load_image(self, image_path):
        """加载图片并返回numpy数组"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        return face_recognition.load_image_file(image_path)

    def register_face(self, name, image_path):
        """注册新的人脸并保存编码"""
        image = self.load_image(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if not face_encodings:
            print(f"No face found in the image: {image_path}")
            return False

        face_encoding = face_encodings[0]
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(name)
        print(f"Face registered for {name}")

        # 保存编码
        self.save_encodings()
        return True

    def save_encodings(self):
        """保存人脸编码到文件"""
        data = {
            "encodings": self.known_face_encodings,
            "names": self.known_face_names
        }
        with open(self.encodings_file, 'wb') as f:
            pickle.dump(data, f)
        print(f"Encodings saved to {self.encodings_file}")

    def load_encodings(self):
        """从文件加载人脸编码"""
        if os.path.exists(self.encodings_file):
            with open(self.encodings_file, 'rb') as f:
                data = pickle.load(f)
            self.known_face_encodings = data["encodings"]
            self.known_face_names = data["names"]
            print(f"Loaded {len(self.known_face_names)} face encodings from {self.encodings_file}")
        else:
            print("No existing encodings file found. Starting with an empty database.")

    def detect_and_recognize_face(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        if not face_locations:
            return [], []
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        names = []
        face_locations_list = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            else:
                name = "Unknown"
            names.append(name)
            face_locations_list.append((top, right, bottom, left))
        return names, face_locations_list

    def list_registered_faces(self):
        """列出所有已注册的人脸"""
        return self.known_face_names


# 使用示例
if __name__ == "__main__":
    recognizer = FaceRecognizer()

    # # 注册人脸
    # recognizer.register_face("Biden", "static/biden.jpg")
    # recognizer.register_face("Obama", "static/obama.jpg")

    # 列出已注册的人脸
    print("Registered faces:", recognizer.list_registered_faces())

    # 识别人脸
    result = recognizer.recognize_face("static/obama2.jpg")
    print("Recognition result:", result)
