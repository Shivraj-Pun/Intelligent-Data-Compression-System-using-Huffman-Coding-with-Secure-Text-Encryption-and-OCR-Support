from flask import Flask, render_template, request, send_file, session, redirect, url_for, flash
from encryption_and_image_protection import AESEncryption, ImageProtector, Authenticator
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
aes = AESEncryption()
authenticator = Authenticator()
BLUR_COORDINATES = [(50, 50, 200, 100)]  # You can make this dynamic later


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    encrypted_text = ''
    decrypted_text = ''
    if request.method == 'POST':
        if 'encrypt' in request.form:
            plain_text = request.form.get('plain_text')
            encrypted_text = aes.encrypt(plain_text)
        elif 'decrypt' in request.form:
            encrypted_text = request.form.get('encrypted_text')
            decrypted_text = aes.decrypt(encrypted_text)
    return render_template('index.html', encrypted_text=encrypted_text, decrypted_text=decrypted_text)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if authenticator.authenticate(username, password):
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


@app.route('/image-blur', methods=['GET', 'POST'])
def image_blur():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'image' in request.files and 'password' in request.form:
            image = request.files['image']
            password = request.form.get('password')
            if authenticator.authenticate('root', password):
                image.save('uploaded_image.png')
                ImageProtector.blur_text_in_image('uploaded_image.png', 'blurred_image.png', BLUR_COORDINATES)
                return send_file('blurred_image.png', as_attachment=True)
            else:
                flash('Incorrect password!')
    return render_template('image_blur.html')


@app.route('/image-unblur', methods=['GET', 'POST'])
def image_unblur():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        if authenticator.authenticate('root', password):
            ImageProtector.unblur_text_in_image('blurred_image.png', 'unblurred_image.png', BLUR_COORDINATES, 'uploaded_image.png')
            return send_file('unblurred_image.png', as_attachment=True)
        else:
            flash('Incorrect password!')
    return render_template('image_unblur.html')


if __name__ == '__main__':
    app.run(debug=True)
