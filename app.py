import os
import uuid
import sys
from flask import Flask, request, redirect, url_for, send_from_directory, Response, jsonify
from werkzeug import secure_filename
import contour, mask
import cv2

UPLOAD_FOLDER = '/vagrant/web/static/img/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/score')
def get_score():
    std = mask.mask_for_yellow("static/img/original.jpg")
    if std == None:
        return ""

    obj = contour.contour("static/img/edge.jpg", std)
    if obj == None:
        return ""

    return jsonify({"area": cv2.contourArea(obj)/1000, "std": cv2.contourArea(std), "corrected": cv2.contourArea(obj)/cv2.contourArea(std) *10})

@app.route('/original', methods=['POST'])
def original():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            #filename = str(uuid.uuid4()) + secure_filename(file.filename)
            output_file = os.path.join(app.config['UPLOAD_FOLDER'], "original.jpg")
            file.save(output_file)
            return ""
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/edge', methods=['GET', 'POST'])
def edge():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            #filename = str(uuid.uuid4()) + secure_filename(file.filename)
            output_file = os.path.join(app.config['UPLOAD_FOLDER'], "edge.jpg")
            file.save(output_file)
            return ""
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/html/<path:path>')
def send_html(path):
    return send_from_directory('static/html', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=7011)


