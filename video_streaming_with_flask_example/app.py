import os

from flask import Flask
from flask import jsonify
from flask import render_template, Response, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

from FaceRecognitionSystem import FaceRecognizer
from models import Oldman, Event
from mood_detect import MoodDetect
from object_detect import ObjectDetect
from pose_detect import PoseDetect

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


@app.route("/")
def helloWorld():
    return "Hello, cross-origin-world!"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pose')
def pose():
    return render_template('pose.html')


@app.route('/object')
def object():
    return render_template('object.html')


@app.route('/face')
def face():
    return render_template('face.html')


@app.route('/mood')
def mood():
    return render_template('mood.html')


@app.route('/mood_feed')
def mood_feed():
    def generate(camera):
        while True:
            frame = camera.get_mood_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    return Response(generate(MoodDetect()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/face_feed')
def face_feed():
    def generate(camera):
        while True:
            frame = camera.get_face_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    return Response(generate(MoodDetect()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/pose_feed')
def pose_feed():
    def generate(camera):
        while True:
            frame = camera.get_pose_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    return Response(generate(PoseDetect()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/object_feed')
def object_feed():
    def generate(camera):
        while True:
            frame = camera.get_object_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    return Response(generate(ObjectDetect()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/oldman', methods=['POST'])
def create_oldman():
    name = request.form.get('name')
    room = request.form.get('room')
    age = request.form.get('age')
    gender = request.form.get('gender')
    phone = request.form.get('phone')
    type = request.form.get('type')
    image = request.files.get('image')
    image_filename = secure_filename(image.filename)
    image_suffix = image_filename.split('.')[-1]
    image_name = f'{name}.{image_suffix}'
    image.save(image_name)
    Oldman.create(name, room, age, gender, image_name, phone, type)
    recognizer = FaceRecognizer()
    recognizer.register_face(name, image_name)
    return {'message': 'Oldman created successfully'}, 201


@app.route('/oldmen', methods=['GET'])
def get_oldmen():
    oldmen = Oldman.list_all()
    return jsonify(oldmen)


@app.route('/events', methods=['GET'])
def get_events():
    events = Event.list_all()
    return jsonify(events)


if __name__ == '__main__':
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    app.run(host='0.0.0.0', debug=True)
