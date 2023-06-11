import os
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, jsonify

from models.m7.model import M7FaceAntiSpoofing
import os
# from m6 import predict_one_img
import warnings
from detector.cv_face_detector.model import CVFaceDetector
face_detector = CVFaceDetector()
spoof_detectors = [M7FaceAntiSpoofing()]
import urllib.request
import cv2

def predict_one_img(img_path,  spoof_detector):
    bgr = cv2.imread(img_path)
    face_bboxes = face_detector.get_face_bboxes(bgr)
    for bbox in face_bboxes:
        crop = bgr[bbox[1]:bbox[3], bbox[0]:bbox[2], :]
        real_score = spoof_detector.get_real_score(bgr, bbox)
        print("Real score for image name " + img_path + " is: ",
              real_score)
        if real_score < 0.5:
            return False
        else:
            return True

import warnings
import urllib.request
#from app import app
app = Flask(__name__)
from models.m7.model import M7FaceAntiSpoofing
from models.m6.model import M6FaceAntiSpoofing
import os
app.config['UPLOAD_FOLDER'] = 'static/uploads'

from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
        # check if the post request has the file part
        if 'file' not in request.files:
                resp = jsonify({'message' : 'No file part in the request'})
                resp.status_code = 400
                return resp
        file = request.files['file']
        if file.filename == '':
                resp = jsonify({'message' : 'No file selected for uploading'})
                resp.status_code = 400
                return resp
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                resp = jsonify({'message' : 'File successfully uploaded'})
                resp.status_code = 201
                return resp
        else:
                resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
                resp.status_code = 400
                return resp

@app.route('/m7', methods=['POST'])
def m1():
        if 'file' not in request.files:
                resp = jsonify({'message' : 'No file part in the request'})
                resp.status_code = 400
                return resp
        file = request.files['file']
        if file.filename == '':
                resp = jsonify({'message' : 'No file selected for uploading'})
                resp.status_code = 400
                return resp
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # call predict_one_img here
                x  = predict_one_img(os.path.join(app.config['UPLOAD_FOLDER'], filename),M7FaceAntiSpoofing())
                resp = jsonify({'message' : 'File successfully uploaded','result':x})

if __name__ == "__main__":
        warnings.filterwarnings('ignore')
        app.run(host='0.0.0.0')