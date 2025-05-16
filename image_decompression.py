# decompression_grayscale.py

import pickle
from PIL import Image
import numpy as np

from collections import namedtuple

class Node(namedtuple("Node", ["value", "freq", "left", "right"])):
    def __lt__(self, other):
        return self.freq < other.freq


def read_encoded_data(file_path):
    with open(file_path, 'rb') as file:
        huffman_tree, shape = pickle.load(file)
        bit_string = ""
        byte = file.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)
    return huffman_tree, shape, bit_string

def remove_padding(padded_encoded_data):
    padded_info = padded_encoded_data[:8]
    extra_padding = int(padded_info, 2)
    return padded_encoded_data[8:-extra_padding]

def decode_data(encoded_data, huffman_tree):
    decoded_pixels = []
    current_node = huffman_tree
    for bit in encoded_data:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.value is not None:
            decoded_pixels.append(current_node.value)
            current_node = huffman_tree
    return decoded_pixels

def decompress_image(input_path, output_path):
    huffman_tree, shape, padded_data = read_encoded_data(input_path)
    encoded_data = remove_padding(padded_data)
    pixel_values = decode_data(encoded_data, huffman_tree)
    image_array = np.array(pixel_values, dtype=np.uint8).reshape(shape)
    image = Image.fromarray(image_array)
    image.save(output_path)

if __name__ == "__main__":
    decompress_image('compressed_gray.huff', 'decompressed_gray_image.png')
