import wave
import struct
import heapq
import os

# Node class for Huffman Tree
class Node:
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Function to calculate frequencies
def calculate_frequencies(samples):
    freq_dict = {}
    for sample in samples:
        if sample in freq_dict:
            freq_dict[sample] += 1
        else:
            freq_dict[sample] = 1
    return freq_dict

# Build Huffman Tree
def build_huffman_tree(freq_dict):
    priority_queue = [Node(symbol, freq) for symbol, freq in freq_dict.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

# Generate Huffman Codes
def generate_huffman_codes(node, prefix='', codebook={}):
    if node is not None:
        if node.symbol is not None:
            codebook[node.symbol] = prefix
        generate_huffman_codes(node.left, prefix + '0', codebook)
        generate_huffman_codes(node.right, prefix + '1', codebook)
    return codebook

# Read WAV samples
def read_wav_samples(path):
    with wave.open(path, 'rb') as wav:
        n_channels, sampwidth, framerate, n_frames, _, _ = wav.getparams()
        raw_data = wav.readframes(n_frames)
        samples = struct.unpack('<' + 'h' * n_frames * n_channels, raw_data)
        
        # Split stereo channels (if stereo)
        if n_channels == 2:
            left_channel = samples[0::2]
            right_channel = samples[1::2]
            samples = list(zip(left_channel, right_channel))  # Pair left and right channels
    return samples

# Write WAV file
def write_wav(path, samples, framerate=44100):
    with wave.open(path, 'wb') as wav:
        wav.setnchannels(2)  # Stereo
        wav.setsampwidth(2)  # 2 bytes per sample
        wav.setframerate(framerate)
        flattened_samples = [sample for pair in samples for sample in pair]
        raw = struct.pack('<' + 'h' * len(flattened_samples), *flattened_samples)
        wav.writeframes(raw)

# Write codebook to file
def save_codebook(codebook, filename="codebook.txt"):
    with open(filename, "w") as f:
        for code, symbol in codebook.items():
            f.write(f"{code}:{symbol}\n")

# Write compressed data to file
def save_compressed_data(compressed_data, filename="compressed_data.bin"):
    with open(filename, "wb") as f:
        f.write(compressed_data)

# Main function for compression
def compress(path):
    samples = read_wav_samples(path)
    freq_dict = calculate_frequencies(samples)
    root = build_huffman_tree(freq_dict)
    codebook = generate_huffman_codes(root)

    # Save the codebook for decompression
    save_codebook(codebook)

    # Convert samples to binary using the codebook
    compressed_data = ''.join([codebook[sample] for sample in samples])
    
    # Ensure it's byte-aligned
    compressed_data = compressed_data + '0' * (8 - len(compressed_data) % 8) if len(compressed_data) % 8 != 0 else compressed_data
    compressed_data_bytes = bytes(int(compressed_data[i:i+8], 2) for i in range(0, len(compressed_data), 8))
    
    save_compressed_data(compressed_data_bytes)
    print("Compression successful!")

# Run compression
if __name__ == "__main__":
    input_path = "C:\\Users\\bhatt\\Desktop\\Travis Scott - sdp interlude (Extended).wav"
    compress(input_path)
