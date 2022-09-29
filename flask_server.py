import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from manual_run import check_in_uploaded_files
import json

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 # 4*1024*1024 bytes == 4 Mbytes

ALLOWED_EXTENSIONS = set(['zip'])

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

        dir_name = filename.split('.')[0]
        suspect_filename = f"uploads/suspects_{dir_name}.json"

        check_in_uploaded_files(filename, suspect_filename)

        with open(suspect_filename) as json_file:
            data = json.load(json_file)
        resp = jsonify(data)
        json_file.close()
        os.remove(suspect_filename)

        resp.status_code = 201
        return resp 

    else:
        resp = jsonify({'message' : 'Allowed only zip files'})
        resp.status_code = 400
        return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0')