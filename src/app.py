from flask import Flask, render_template, flash, request, send_file
from werkzeug import Request
# from werkzeug.utils import secure_filename
from Model import Model
import re

PATH_TO_ORDER = "uploads/order.xlsx"
PATH_TO_RESULT = r"..\uploads\result.xlsx"
DEFAULT_WEIGHTS = (10, 1)


app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Потрібно для використання flash повідомлень


@app.route('/bach', methods=['GET', 'POST'])
def calc():
    # flash('This is a flashed message!')
    # flash('This is another flashed message!')
    
    # GET
    if request.method == 'GET':
        return render_template('form.html')
    # POST
    if valid_login(request.form['username'], request.form['password']):
        do_work(request)

        return send_file(PATH_TO_RESULT, as_attachment=True, download_name="result.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        error = 'Invalid username/password'
        return render_template('form.html', error=error)

   

def valid_login(name:str, password: str): 
    return name == 'admin' and password == 'admin'

def do_work(request: Request):
    
    f = request.files['file_order']
    f.save(PATH_TO_ORDER)

    # parse weights
    weights_str = request.form['weights'].strip()
    match = re.match(r"(\d+)\s*:\s*(\d+)", weights_str)
    if match:
        weights = (int(match.group(1)), int(match.group(2)))
    else:
        weights = DEFAULT_WEIGHTS
 
    model = Model(PATH_TO_ORDER, weights)
    model.excell_result()


if __name__ == '__main__':
    app.run(debug=True)