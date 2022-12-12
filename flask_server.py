import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from manual_run import check_in_uploaded_files
import constant

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = constant.MAX_CONTENT_LENGTH


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in constant.ALLOWED_EXTENSIONS

@app.route("/")
def hello():
    return render_template('home.html')


@app.route('/file-upload', methods=['GET', 'POST'])
def upload_file():

    if request.method == "GET":
        return render_template('upload.html')
    if request.method == "POST":
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

        comments_ignore = not request.form.get('comments')
        table_ignore = not request.form.get('table')
        lim = float(request.form.get('lim') or constant.DEFAULT_LIM)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            data, df = check_in_uploaded_files(filename, lim, comments_ignore)

            temp = df.to_dict('records')
            columnNames = df.columns.values
            if table_ignore:
                return render_template('record.html', output=data, lim=lim)
            return render_template('record.html', records=temp, colnames=columnNames, output=data, lim=lim)
        else:
            resp = jsonify({'message' : 'Allowed only zip files'})
            resp.status_code = 400
            return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0')