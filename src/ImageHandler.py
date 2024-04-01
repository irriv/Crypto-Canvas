from tkinter import filedialog, simpledialog, messagebox
from secrets import token_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import startfile
from os.path import splitext
from stegano import lsb

class ImageHandler:
    def encrypt_image(self, image_data):
        try:
            nonce = token_bytes(12)
            key = token_bytes(32)
            password = simpledialog.askstring('Password', 'Enter password for resulting file:').encode('utf-8')
            ciphertext = AESGCM(key).encrypt(nonce, image_data, password)
            filepath = self.get_save_image_filepath()
            if not filepath:
                return
            with open(filepath, 'wb') as encrypted_file:
                encrypted_file.write(ciphertext)
            self.show_success(f'Encryption successful. Encrypted image saved to {filepath}')
            startfile(filepath)
            root, _ = splitext(filepath)
            info_filepath = f'{root}_encryption_info.txt'
            with open(info_filepath, 'w') as file:
                file.write('Nonce: ' + nonce.hex() + '\n')
                file.write('Key: ' + key.hex() + '\n')
                file.write('Password: ' + password.decode('utf-8') + '\n')
            self.show_success(f'Encryption info written to {info_filepath}')
            startfile(info_filepath)
        except Exception as e:
            self.show_error(f'Encrypting image failed: {e}')

    def decrypt_image(self, image_data):
        try:
            nonce = bytes.fromhex(simpledialog.askstring('Nonce', 'Enter nonce:'))
            key = bytes.fromhex(simpledialog.askstring('Key', 'Enter key:'))
            password = simpledialog.askstring('Password', 'Enter password:').encode('utf-8')
            decrypted_data = AESGCM(key).decrypt(nonce, image_data, password)
            filepath = self.get_save_image_filepath()
            if not filepath:
                return
            with open(filepath, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)
            self.show_success(f'Decryption successful. Decrypted image saved to {filepath}')
            startfile(filepath)
        except Exception as e:
            self.show_error(f'Decrypting image failed: {e}')

    def hide_image(self, carrier_image_path, secret_image_data):
        try:
            hex_string = secret_image_data.hex()
            carrier_image = lsb.hide(carrier_image_path, hex_string)
            root, _ = splitext(carrier_image_path)
            filepath = self.get_save_image_filepath()
            carrier_image.save(filepath)
            self.show_success(f'Image hidden successfully. Stego image saved to {filepath}')
            carrier_image.show()
        except Exception as e:
            self.show_error(f'Hiding image failed: {e}')

    def reveal_image(self, filepath):
        try:
            hex_string = lsb.reveal(filepath)
            filepath = self.get_save_image_filepath()
            with open(filepath, 'wb') as f:
                f.write(bytes.fromhex(hex_string))
            self.show_success(f'Image revealed successfully. Revealed image saved to {filepath}')
            startfile(filepath)
        except Exception as e:
            self.show_error(f'Revealing image failed: {e}')

    def hide_text(self, carrier_image_path, secret_text):
        try:
            carrier_image = lsb.hide(carrier_image_path, secret_text)
            filepath = self.get_save_image_filepath()
            carrier_image.save(filepath)
            self.show_success(f'Text hidden successfully. Stego image saved to {filepath}')
            carrier_image.show()
        except Exception as e:
            self.show_error(f'Hiding text failed: {e}')

    def reveal_text(self, filepath):
        try:
            revealed_text = lsb.reveal(filepath)
            filepath = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('TXT files','*.txt')])
            with open(filepath, 'w') as f:
                f.write(revealed_text)
            self.show_success(f'Text revealed successfully. Revealed text saved to {filepath}')
            startfile(filepath)
        except Exception as e:
            self.show_error(f'Revealing text failed: {e}')

    def show_success(self, msg):
        messagebox.showinfo('Success', msg)

    def show_error(self, msg):
        messagebox.showerror('Error', msg)

    def get_save_image_filepath(self):
        return filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files','*.png')])
