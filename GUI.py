from flask import Flask, render_template, request, send_file
from encryption_and_image_protection import AESEncryption, ImageProtector
import os

app = Flask(__name__)
aes = AESEncryption()
ROOT_KEY = "my-secret-root-key"  # Change this to something more secure


@app.route('/', methods=['GET', 'POST'])
def index():
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


@app.route('/image-blur', methods=['GET', 'POST'])
def image_blur():
    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            coordinates = [(50, 50, 200, 100)]  # Can be dynamic as per UI input
            image.save('uploaded_image.png')
            ImageProtector.blur_text_in_image('uploaded_image.png', 'blurred_image.png', coordinates)
            return send_file('blurred_image.png', as_attachment=True)
    return render_template('image_blur.html')


if __name__ == '__main__':
    app.run(debug=True)
