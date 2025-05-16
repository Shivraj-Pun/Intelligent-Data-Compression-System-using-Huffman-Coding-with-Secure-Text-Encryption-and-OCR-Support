# app.py
from flask import Flask, render_template, request, redirect, url_for, send_file
from encryption_and_image_protection import AESEncryption, ImageProtector, Authenticator
import os

app = Flask(__name__)

# Hardcoded login for encryption
USERNAME = "root"
PASSWORD = "securepassword"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compression')
def compression():
    return render_template('compression.html')

@app.route('/encryption')
def encryption():
    return render_template('encryption.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('encryption'))
        else:
            return "Login Failed"
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
