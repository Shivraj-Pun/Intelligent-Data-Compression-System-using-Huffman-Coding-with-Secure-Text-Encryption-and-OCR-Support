# compression_grayscale.py

import heapq
import pickle
from PIL import Image
import numpy as np
from collections import Counter, namedtuple

class Node(namedtuple("Node", ["value", "freq", "left", "right"])):
    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(data):
    return Counter(data)

def build_huffman_tree(freq_table):
    heap = [Node(value=k, freq=f, left=None, right=None) for k, f in freq_table.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(value=None, freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    return heap[0] if heap else None

def generate_codes(node, prefix="", code_map={}):
    if node is None:
        return
    if node.value is not None:
        code_map[node.value] = prefix
    generate_codes(node.left, prefix + "0", code_map)
    generate_codes(node.right, prefix + "1", code_map)
    return code_map

def encode_data(data, code_map):
    return ''.join(code_map[pixel] for pixel in data)

def pad_encoded_data(encoded_data):
    extra_padding = 8 - len(encoded_data) % 8
    encoded_data += "0" * extra_padding
    padded_info = "{0:08b}".format(extra_padding)
    return padded_info + encoded_data

def get_byte_array(padded_encoded_data):
    b = bytearray()
    for i in range(0, len(padded_encoded_data), 8):
        byte = padded_encoded_data[i:i+8]
        b.append(int(byte, 2))
    return b

def compress_image(image_path, output_path):
    image = Image.open(image_path).convert('L')
    pixel_data = np.array(image).flatten()
    shape = image.size[::-1]  # (height, width)

    freq_table = build_frequency_table(pixel_data)
    huffman_tree = build_huffman_tree(freq_table)
    code_map = generate_codes(huffman_tree)

    encoded_data = encode_data(pixel_data, code_map)
    padded_data = pad_encoded_data(encoded_data)
    byte_array = get_byte_array(padded_data)

    with open(output_path, 'wb') as out:
        pickle.dump((huffman_tree, shape), out)
        out.write(bytes(byte_array))

if __name__ == "__main__":
    compress_image('input_image.png', 'compressed_gray.huff')
