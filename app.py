# app.py
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from encryption_and_image_protection import ImageProtector
from huffman_wav_compress import compress as compress_audio
from huffman_wav_decompress import decompress as decompress_audio
from image_compression import compress_image
from image_decompression import decompress_image
from text_compression import compress_text
from text_decompression import decompress_text
import os

app = Flask(__name__)
app.secret_key = "secretkey"

# Directories
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'
DECOMPRESSED_FOLDER = 'decompressed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)
os.makedirs(DECOMPRESSED_FOLDER, exist_ok=True)

# --------------------
# ROUTES
# --------------------

@app.route('/')
def index():
    return render_template('index.html')

# --------------------
# Text Compression & Decompression
# --------------------
@app.route('/compress_text', methods=['GET', 'POST'])
def compress_text_route():
    if request.method == 'POST':
        text_file = request.files['file']
        if text_file:
            input_path = os.path.join(UPLOAD_FOLDER, text_file.filename)
            output_path = os.path.join(COMPRESSED_FOLDER, f"{text_file.filename}.huff")
            text_file.save(input_path)
            compress_text(input_path, output_path)
            return send_file(output_path, as_attachment=True)
    return render_template('compress/text_compress.html')

@app.route('/decompress_text', methods=['GET', 'POST'])
def decompress_text_route():
    if request.method == 'POST':
        compressed_file = request.files['file']
        if compressed_file:
            input_path = os.path.join(COMPRESSED_FOLDER, compressed_file.filename)
            output_path = os.path.join(DECOMPRESSED_FOLDER, f"{compressed_file.filename}.txt")
            compressed_file.save(input_path)
            decompress_text(input_path, output_path)
            return send_file(output_path, as_attachment=True)
    return render_template('decompress/text_decompress.html')

# --------------------
# Image Compression & Decompression
# --------------------
@app.route('/compress_image', methods=['GET', 'POST'])
def compress_image_route():
    if request.method == 'POST':
        image_file = request.files.get('file')
        if image_file:
            input_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
            output_path = os.path.join(COMPRESSED_FOLDER, f"{image_file.filename}.huff")
            image_file.save(input_path)

            # Call the compression logic
            compress_image(input_path, output_path)
            
            if os.path.exists(output_path):
                flash("Image compression successful!")
                return send_file(output_path, as_attachment=True)
            else:
                flash("Compression failed. No file found.")
    return render_template('compress/image_compress.html')
# --------------------
# Image Blur (Encryption) & Unblur (Decryption)
# --------------------
@app.route('/image-blur')
def image_blur():
    return render_template('image-blur.html')

@app.route('/image-unblur')
def image_unblur():
    return render_template('image-unblur.html')
