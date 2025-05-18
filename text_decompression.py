# text_decompression.py
import pickle
import time

def decompress_text(input_path, output_path):
    print("[INFO] Starting decompression...")

    start_time = time.time()  # Timer to detect long loops

    with open(input_path, 'rb') as file:
        # 1️⃣ Load the Huffman codes first
        try:
            codes = pickle.load(file)
            print("[INFO] Huffman Codes loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Unable to load Huffman codes: {e}")
            return

        # 2️⃣ Read padding information
        padding_info = file.read(1).decode('utf-8')
        extra_padding = int(padding_info, 2)
        print(f"[INFO] Extra Padding: {extra_padding} bits")

        # 3️⃣ Read the compressed bit string
        bit_string = ""
        byte = file.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)

        # Remove the extra padding
        if extra_padding > 0:
            bit_string = bit_string[:-extra_padding]

        print(f"[INFO] Total bits to process: {len(bit_string)}")

        # 4️⃣ Reverse the codes dictionary for decoding
        reverse_codes = {v: k for k, v in codes.items()}
        print("[INFO] Huffman Codes reversed for decoding.")

        # 5️⃣ Decode the string
        current_code = ""
        decoded_text = ""
        
        print("[INFO] Starting bit-by-bit decoding...")
        max_code_length = max(map(len, reverse_codes.keys()))
        
        for index, bit in enumerate(bit_string):
            current_code += bit

            # 🔄 Debugging every 1000 bits processed
            if index % 1000 == 0:
                print(f"[DEBUG] Processed {index} bits, current_code length: {len(current_code)}")

            # 🛡️ Protection: If the code is too long, break (prevents infinite loops)
            if len(current_code) > max_code_length + 10:
                print(f"[ERROR] Current code is too long: {current_code}. Breaking to prevent loop.")
                break
            
            if current_code in reverse_codes:
                decoded_text += reverse_codes[current_code]
                current_code = ""

        # Write to output file
        if decoded_text:
            with open(output_path, 'w') as file:
                file.write(decoded_text)
            print("[INFO] Decompression complete. File saved.")
        else:
            print("[ERROR] Decompression failed. No valid data decoded.")
