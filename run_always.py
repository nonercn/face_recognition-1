# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join, splitext
import face_recognition
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import numpy as np
import PIL.Image
import multiprocessing

# Create flask app
app = Flask(__name__)
CORS(app)


# distance
def image_distance(known_face_encoding):
    return face_recognition.face_distance([known_face_encoding], unkown_face_encoding)[0]


def back_func_distance(values):
    global result_distance
    result_distance = values


def back_func_err_distance(values):
    print(values)


def process_pool_distance(known_face_encodings):
    pool = multiprocessing.Pool(processes=None)
    pool.map_async(image_distance, (known_face_encoding for known_face_encoding in known_face_encodings), callback=back_func_distance,
                   error_callback=back_func_err_distance)

    pool.close()
    pool.join()
    print(result_distance)
    return result_distance


# encoding
def is_picture(filename):
    image_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pgm'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in image_extensions


def get_all_picture_files(path):
    files_in_dir = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    return [f for f in files_in_dir if is_picture(f)]


def remove_file_ext(filename):
    return splitext(filename.rsplit('/', 1)[-1])[0]


def calc_face_encoding(image):
    loaded_image = face_recognition.load_image_file(image)

    # 缩小图片尺寸，识别更快
    if max(loaded_image.shape) > 1600:
        pil_img = PIL.Image.fromarray(loaded_image)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        loaded_image = np.array(pil_img)

    faces = face_recognition.face_encodings(loaded_image)
    if not faces:
        return []
    return faces[0]


def get_faces_dict(image):
    info = {}
    info["name"] = remove_file_ext(image)
    info["encode"] = list(calc_face_encoding(image))
    return info


def back_func_encode(values):
    global result_encode
    result_encode = values


def back_func_err_encode(values):
    print(values)


def process_pool_encode(path):
    image_files = get_all_picture_files(path)
    pool = multiprocessing.Pool(processes=None)
    pool.map_async(get_faces_dict, (image for image in image_files), callback=back_func_encode,
                   error_callback=back_func_err_encode)
    pool.close()
    pool.join()
    return result_encode


@app.route('/encode', methods=['GET', 'POST'])
def web_encode():
    print("encode")
    if request.method == 'GET':
        return json.dumps(process_pool_encode("/opt/face"))
    if request.method == 'POST':
        file = request.files['file']
        return json.dumps(list(calc_face_encoding(file)))


@app.route('/', methods=['GET'])
def web_run():
    return "running"


@app.route('/distance', methods=['POST'])
def web_distance():
    print("distance")
    global unkown_face_encoding
    unkown_face_encoding = request.form.get('unkown')
    unkown_face_encoding = np.array(json.loads(unkown_face_encoding))
    known_face_encodings = request.form.get('kowns')
    known_face_encodings = np.array(json.loads(known_face_encodings))
    return json.dumps(process_pool_distance(known_face_encodings))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888, debug=False)
