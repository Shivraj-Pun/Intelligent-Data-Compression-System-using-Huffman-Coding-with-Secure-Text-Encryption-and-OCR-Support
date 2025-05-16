import wave
import struct

# Node class for Huffman Tree
class Node:
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Function to load the codebook
def load_codebook():
    codebook = {}
    with open("codebook.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    sample_pair, code = line.split(":")
                    sample1, sample2 = map(int, sample_pair.strip("()").split(","))
                    codebook[code] = (sample1, sample2)
                except ValueError:
                    print(f"Skipping invalid line: {line}")
                    continue
    print(f"Codebook loaded with {len(codebook)} entries.")
    return codebook

# Function to reconstruct the Huffman Tree from codebook
def reconstruct_huffman_tree(codebook):
    root = Node(None, None)
    for code, symbol in codebook.items():
        current_node = root
        for bit in code:
            if bit == '0':
                if current_node.left is None:
                    current_node.left = Node(None, None)
                current_node = current_node.left
            else:
                if current_node.right is None:
                    current_node.right = Node(None, None)
                current_node = current_node.right
        current_node.symbol = symbol
    return root

# Function to decode the binary data
def decode_data(compressed_data, root):
    decoded_samples = []
    current_node = root
    for bit in compressed_data:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node is None:
            print("Error: Reached a None node during traversal!")
            break
        
        if current_node.symbol is not None:
            decoded_samples.append(current_node.symbol)
            current_node = root  # Reset to root for the next symbol

    print(f"Decoded {len(decoded_samples)} stereo pairs.")
    return decoded_samples

# Write WAV file
def write_wav(path, samples, framerate=44100):
    with wave.open(path, 'wb') as wav:
        wav.setnchannels(2)  # Stereo
        wav.setsampwidth(2)  # 2 bytes per sample (16-bit samples)
        wav.setframerate(framerate)
        flattened_samples = [sample for pair in samples for sample in pair]  # Flatten the stereo pairs
        raw = struct.pack('<' + 'h' * len(flattened_samples), *flattened_samples)
        wav.writeframes(raw)

# Main function for decompression
def decompress():
    codebook = load_codebook()
    root = reconstruct_huffman_tree(codebook)

    # Load the compressed data
    with open("compressed_data.bin", "rb") as f:
        compressed_data_bytes = f.read()

    # Convert bytes back to binary string
    compressed_data = ''.join(f'{byte:08b}' for byte in compressed_data_bytes)
    print(f"Compressed data length: {len(compressed_data)} bits.")

    # Decode the data using Huffman Tree
    decoded_samples = decode_data(compressed_data, root)

    if decoded_samples:
        # Write the decompressed audio to a WAV file
        output_path = "decompressed_audio.wav"
        write_wav(output_path, decoded_samples)
        print("Decompression successful!")
    else:
        print("Decompression failed. No samples decoded.")

# Run decompression
if __name__ == "__main__":
    decompress()
