from flask import Flask, render_template, request, redirect, url_for, session
import socket

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # Сессийн нууц үг

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Энгийн хэрэглэгчийн шалгалт
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Нууц үг буруу байна'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Порт авах
    port = request.environ.get('SERVER_PORT')
    return render_template('dashboard.html', port=port)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
