
from tkinter import filedialog, simpledialog
from secrets import token_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
from stegano import lsb
from PIL import Image

class ImageHandler:

    def encrypt_image(self):
        filepath = select_file_to_encrypt()
        with open(filepath, 'rb') as file:
            image_data = file.read()
        nonce = token_bytes(12)
        key = token_bytes(32)
        password = input_password()
        ciphertext = AESGCM(key).encrypt(nonce, image_data, password)
        with open(filepath + '.enc', 'wb') as encrypted_file:
            encrypted_file.write(ciphertext)
        print("Encryption successful. Encrypted image saved to", filepath + '.enc')
        write_encryption_info(filepath, nonce, key, password)
        os.startfile(filepath + '.enc')
        os.startfile(filepath + '.enc.txt')

    def decrypt_image(self):
        filepath = select_file_to_decrypt()
        with open(filepath, 'rb') as file:
            encrypted_data = file.read()
        nonce, key, password = input_nonce_key_password()
        image_data = AESGCM(key).decrypt(nonce, encrypted_data, password)
        with open(filepath[:-4], 'wb') as decrypted_file:
            decrypted_file.write(image_data)
        print("Decryption successful. Decrypted image saved to", filepath[:-4])
        os.startfile(filepath[:-4])

    def hide_image(self):
        carrier_filepath = filedialog.askopenfilename(filetypes=[("Carrier image", "*.png;")])
        secret_filepath = filedialog.askopenfilename(filetypes=[("Secret image", "*.png;")])
        hex_string = image_to_hex(secret_filepath)
        carrier_image = lsb.hide(carrier_filepath, hex_string)
        filepath_parts = carrier_filepath.rsplit('.', 1)
        filepath = filepath_parts[0] + "_hidden." + filepath_parts[1]
        carrier_image.save(filepath)
        carrier_image.show()

    def find_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;")])
        hex_string = lsb.reveal(filepath)
        hex_to_image(hex_string)
        os.startfile("secret_image.png")

    def hide_text(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;")])
        text = input("Text to hide: ")
        cover_image = lsb.hide(filepath, text)
        filepath_parts = filepath.rsplit('.', 1)
        filepath = filepath_parts[0] + "_hidden." + filepath_parts[1]
        cover_image.save(filepath)
        cover_image.show()

    def find_text(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;")])
        msg = lsb.reveal(filepath)
        print("Hidden text:", msg)


def select_file_to_encrypt():
    filepath = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;")])
    return filepath

def select_file_to_decrypt():
    filepath = filedialog.askopenfilename(
        filetypes=[("Encrypted image files", "*.enc;")])
    return filepath

def write_encryption_info(filepath, nonce, key, password):
    with open(filepath + '.enc.txt', 'w') as file:
        file.write("Nonce: " + nonce.hex() + "\n")
        file.write("Key: " + key.hex() + "\n")
        file.write("Password: " + password.decode("utf-8") + "\n")
    print("Encryption info written to", filepath + '.enc.txt')

def input_password():
    password = simpledialog.askstring("Password", "Enter password for resulting file:").encode('utf-8')
    return password

def input_nonce_key_password():
    nonce = bytes.fromhex(simpledialog.askstring("Nonce", "Enter nonce:"))
    key = bytes.fromhex(simpledialog.askstring("Key", "Enter key:"))
    password = simpledialog.askstring("Password", "Enter password:").encode('utf-8')
    return nonce, key, password

def image_to_hex(image_path):
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    return image_bytes.hex()

def hex_to_image(hex_string):
    with open("secret_image.png", 'wb') as f:
        f.write(bytes.fromhex(hex_string))
