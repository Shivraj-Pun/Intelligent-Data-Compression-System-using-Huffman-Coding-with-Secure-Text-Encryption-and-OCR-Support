# app.py
from image_compression import compress_image, decompress_image
from audio_compression import compress_audio, decompress_audio
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

# Image Compression
@app.route('/compress_image', methods=['GET', 'POST'])
def compress_image_route():
    if request.method == 'POST':
        image_file = request.files.get('image')
        if image_file:
            input_path = f'uploads/{image_file.filename}'
            image_file.save(input_path)

            output_path = f'compressed/{image_file.filename}.bin'
            compress_image(input_path, output_path)

            return send_file(output_path, as_attachment=True)

    return render_template('compress_image.html')

# Image Decompression
@app.route('/decompress_image', methods=['GET', 'POST'])
def decompress_image_route():
    if request.method == 'POST':
        compressed_file = request.files.get('compressed_image')
        if compressed_file:
            input_path = f'compressed/{compressed_file.filename}'
            compressed_file.save(input_path)

            output_path = f'decompressed/{compressed_file.filename}.png'
            decompress_image(input_path, output_path)

            return send_file(output_path, as_attachment=True)

    return render_template('decompress_image.html')

# Audio Compression
@app.route('/compress_audio', methods=['GET', 'POST'])
def compress_audio_route():
    if request.method == 'POST':
        audio_file = request.files.get('audio')
        if audio_file:
            input_path = f'uploads/{audio_file.filename}'
            audio_file.save(input_path)

            output_path = f'compressed/{audio_file.filename}.bin'
            compress_audio(input_path, output_path)

            return send_file(output_path, as_attachment=True)

    return render_template('compress_audio.html')

# Audio Decompression
@app.route('/decompress_audio', methods=['GET', 'POST'])
def decompress_audio_route():
    if request.method == 'POST':
        compressed_file = request.files.get('compressed_audio')
        if compressed_file:
            input_path = f'compressed/{compressed_file.filename}'
            compressed_file.save(input_path)

            output_path = f'decompressed/{compressed_file.filename}.wav'
            decompress_audio(input_path, output_path)

            return send_file(output_path, as_attachment=True)

    return render_template('decompress_audio.html')

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
