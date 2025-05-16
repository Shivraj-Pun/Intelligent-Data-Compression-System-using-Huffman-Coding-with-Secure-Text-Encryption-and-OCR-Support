# Encryption Logic (AES)
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from PIL import Image, ImageDraw, ImageFilter

class AESEncryption:
    def __init__(self, key=None):
        self.key = key if key else get_random_bytes(16)
    
    def encrypt(self, plain_text):
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode('utf-8'))
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')
    
    def decrypt(self, encrypted_text):
        raw_data = base64.b64decode(encrypted_text)
        nonce, tag, ciphertext = raw_data[:16], raw_data[16:32], raw_data[32:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    
    def get_key(self):
        return base64.b64encode(self.key).decode('utf-8')
    
    def set_key(self, key_str):
        self.key = base64.b64decode(key_str)


# Image Blurring Logic
class ImageProtector:
    @staticmethod
    def blur_text_in_image(image_path, output_path, coordinates, blur_radius=5):
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        for coord in coordinates:
            region = image.crop(coord)
            blurred_region = region.filter(ImageFilter.GaussianBlur(blur_radius))
            image.paste(blurred_region, coord)
        image.save(output_path)

    @staticmethod
    def authenticate_root(user_key, root_key):
        return user_key == root_key
