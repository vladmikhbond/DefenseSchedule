from flask import Flask, render_template, flash, request, send_file
from werkzeug import Request
# from werkzeug.utils import secure_filename
from Model import Model

PATH_TO_ORDER = "uploads/order.xlsx"
PATH_TO_RESULT = r"..\uploads\result.xlsx"


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
    model = Model(PATH_TO_ORDER)
    model.excell_result()


if __name__ == '__main__':
    app.run(debug=True)