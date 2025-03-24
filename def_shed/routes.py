import io
import zipfile
from flask import render_template, flash, request, send_file
from werkzeug import Request
# from werkzeug.utils import secure_filename
from .Model import Model
import re

PATH_TO_INPUT_XLS = "uploads/input.xlsx"
PATH_TO_RESULT_XLS = "uploads/result.xlsx"
DEFAULT_WEIGHTS = (10, 1)

from flask import Blueprint
main = Blueprint("main", __name__)


# main.secret_key = 'your_secret_key'  # Потрібно для використання flash повідомлень


@main.route('/bach', methods=['GET', 'POST'])
def calc():
    # flash('This is a flashed message!')
    # flash('This is another flashed message!')
    
    # GET
    if request.method == 'GET':
        return render_template('form.html')
    # POST
    if valid_login(request.form['username'], request.form['password']):
        path_to_log = do_work(request)
        return download_zip(path_to_log)
    else:
        error = 'Invalid username/password'
        return render_template('form.html', error=error)

   

def valid_login(name:str, password: str): 
    return name == 'admin' and password == 'admin'

def do_work(request: Request):
    
    f = request.files['file_order']
    f.save(PATH_TO_INPUT_XLS)

    # parse weights
    weights_str = request.form['weights'].strip()
    match = re.match(r"(\d+)\s*:\s*(\d+)", weights_str)
    if match:
        weights = (int(match.group(1)), int(match.group(2)))
    else:
        weights = DEFAULT_WEIGHTS

    # distribution
    model = Model(PATH_TO_INPUT_XLS, weights)
    return model.log.path

def download_zip(log_path):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(PATH_TO_RESULT_XLS, 'result.xlsx') 
        zip_file.write(log_path, 'result.log') 
    zip_buffer.seek(0)

    return send_file(zip_buffer, as_attachment=True, download_name="result.zip",
                     mimetype="application/zip")
   


if __name__ == '__main__':
    app.run(debug=True)