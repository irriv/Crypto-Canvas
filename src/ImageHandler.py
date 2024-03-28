
from tkinter import filedialog, simpledialog
from secrets import token_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import startfile

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
        startfile(filepath + '.enc')
        startfile(filepath + '.enc.txt')

    def decrypt_image(self):
        filepath = select_file_to_decrypt()
        with open(filepath, 'rb') as file:
            encrypted_data = file.read()
        nonce, key, password = input_nonce_key_password()
        image_data = AESGCM(key).decrypt(nonce, encrypted_data, password)
        with open(filepath[:-4], 'wb') as decrypted_file:
            decrypted_file.write(image_data)
        print("Decryption successful. Decrypted image saved to", filepath[:-4])
        startfile(filepath[:-4])

    def hide_image(self):
        raise Exception("Not implemented")

    def find_image(self):
        raise Exception("Not implemented")

    def hide_text(self):
        raise Exception("Not implemented")

    def find_text(self):
        raise Exception("Not implemented")


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
