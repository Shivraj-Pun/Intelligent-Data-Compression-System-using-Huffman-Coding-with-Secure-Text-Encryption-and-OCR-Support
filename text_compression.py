# text_compression.py
from collections import Counter
import pickle

class ExtendedBinaryTreeNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

class ExtendedBinaryTree:
    def __init__(self):
        self.root = None
        self.codes = {}

    def build_tree(self, frequencies):
        nodes = [ExtendedBinaryTreeNode(char, freq) for char, freq in frequencies.items()]
        while len(nodes) > 1:
            nodes = sorted(nodes, key=lambda x: x.freq)
            left = nodes.pop(0)
            right = nodes.pop(0)
            merged = ExtendedBinaryTreeNode(freq=left.freq + right.freq)
            merged.left = left
            merged.right = right
            nodes.append(merged)

        self.root = nodes[0]
        self.generate_codes(self.root)

    def generate_codes(self, node, current_code=""):
        if node is not None:
            if node.char is not None:
                self.codes[node.char] = current_code
            self.generate_codes(node.left, current_code + "0")
            self.generate_codes(node.right, current_code + "1")

    def get_codes(self):
        return self.codes

def compress_text(input_path, output_path):
    with open(input_path, 'r') as file:
        text = file.read()

    # Frequency analysis
    frequencies = Counter(text)

    # Build the extended binary tree
    ebt = ExtendedBinaryTree()
    ebt.build_tree(frequencies)
    codes = ebt.get_codes()

    # Encode the text
    encoded_data = ''.join([codes[char] for char in text])

    # Padding to make it byte-aligned
    extra_padding = 8 - len(encoded_data) % 8
    encoded_data += "0" * extra_padding

    # Save the extra padding count
    padding_info = f"{extra_padding:08b}"

    # Convert the bit string to bytes
    b = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i + 8]
        b.append(int(byte, 2))

    # Write to file in the correct order:
    with open(output_path, 'wb') as file:
        pickle.dump(codes, file)                       # 1️⃣ Save the Huffman codes
        file.write(padding_info.encode('utf-8'))       # 2️⃣ Save the padding information
        file.write(b)                                  # 3️⃣ Save the compressed data
