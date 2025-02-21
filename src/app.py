from flask import Flask, render_template, flash, request
# from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Потрібно для використання flash повідомлень


@app.route('/bach', methods=['GET', 'POST'])
def calc():
    # flash('This is a flashed message!')
    # flash('This is another flashed message!')

    if request.method == 'POST':
            f = request.files['file_order']
            f.save(f"uploads/order.xlsx")
            # f.save(f"uploads/{secure_filename(f.filename)}")

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)