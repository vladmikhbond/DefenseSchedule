from flask import Flask, render_template, flash, request
from werkzeug import Request
# from werkzeug.utils import secure_filename
from Model import Model

app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Потрібно для використання flash повідомлень


@app.route('/bach', methods=['GET', 'POST'])
def calc():
    # flash('This is a flashed message!')
    # flash('This is another flashed message!')
    if request.method == 'GET':
        return render_template('form.html')

    if valid_login(request.form['username'], request.form['password']):
        answer = do_work(request)
        return render_template('answer.html', answer=answer)
    else:
        error = 'Invalid username/password'
        # the code below is executed if the request method
        # was GET or the credentials were invalid
        return render_template('form.html', error=error)

   

def valid_login(name:str, pass_: str): 
    return True

def do_work(request: Request):
    PATH = f"uploads/order.xlsx"
    f = request.files['file_order']
    f.save(PATH)
    model = Model(PATH)
    model.excell_result()
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True)