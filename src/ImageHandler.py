
from tkinter import filedialog, simpledialog, messagebox
from secrets import token_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import startfile
from os.path import splitext
from stegano import lsb

class ImageHandler:
    def encrypt_image(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[('Image to encrypt', '*.jpg;*.jpeg;*.png;')])
            with open(filepath, 'rb') as file:
                image_data = file.read()
            nonce = token_bytes(12)
            key = token_bytes(32)
            password = simpledialog.askstring('Password', 'Enter password for resulting file:').encode('utf-8')
            ciphertext = AESGCM(key).encrypt(nonce, image_data, password)
            root, extension = splitext(filepath)
            filepath = f'{root}_encrypted_image{extension}'
            with open(filepath, 'wb') as encrypted_file:
                encrypted_file.write(ciphertext)
            messagebox.showinfo('Success', f'Encryption successful. Encrypted image saved to {filepath}')
            startfile(filepath)
            root, extension = splitext(filepath)
            filepath = f'{root}_encryption_info.txt'
            with open(filepath, 'w') as file:
                file.write('Nonce: ' + nonce.hex() + '\n')
                file.write('Key: ' + key.hex() + '\n')
                file.write('Password: ' + password.decode('utf-8') + '\n')
            messagebox.showinfo('Success', f'Encryption info written to {filepath}')
            startfile(filepath)
        except Exception as e:
            messagebox.showerror('Error', f'Encrypting image failed: {e}')

    def decrypt_image(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[('Encrypted image', '*.jpg;*.jpeg;*.png;')])
            with open(filepath, 'rb') as file:
                encrypted_data = file.read()
            nonce = bytes.fromhex(simpledialog.askstring('Nonce', 'Enter nonce:'))
            key = bytes.fromhex(simpledialog.askstring('Key', 'Enter key:'))
            password = simpledialog.askstring('Password', 'Enter password:').encode('utf-8')
            image_data = AESGCM(key).decrypt(nonce, encrypted_data, password)
            root, extension = splitext(filepath)
            filepath = f'{root}_decrypted_image{extension}'
            with open(filepath, 'wb') as decrypted_file:
                decrypted_file.write(image_data)
            messagebox.showinfo('Success', f'Decryption successful. Decrypted image saved to {filepath}')
            startfile(filepath)
        except Exception as e:
            messagebox.showerror('Error', f'Decrypting image failed: {e}')

    def hide_image(self):
        try:
            carrier_filepath = filedialog.askopenfilename(filetypes=[('Carrier image', '*.png;')])
            secret_filepath = filedialog.askopenfilename(filetypes=[('Image to hide', '*.png;')])
            with open(secret_filepath, 'rb') as f:
                image_bytes = f.read()
            hex_string = image_bytes.hex()
            carrier_image = lsb.hide(carrier_filepath, hex_string)
            root, extension = splitext(carrier_filepath)
            filepath = f'{root}_hidden_image{extension}'
            carrier_image.save(filepath)
            messagebox.showinfo('Success', f'Image hidden successfully. Stego image saved to {filepath}')
            carrier_image.show()
        except Exception as e:
            messagebox.showerror('Error', f'Hiding image failed: {e}')

    def reveal_image(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[('Stego image', '*.png;')])
            hex_string = lsb.reveal(filepath)
            root, extension = splitext(filepath)
            filepath = f'{root}_revealed_image{extension}'
            with open(filepath, 'wb') as f:
                f.write(bytes.fromhex(hex_string))
            messagebox.showinfo('Success', f'Image revealed successfully. Revealed image saved to {filepath}')
            startfile(filepath)
        except Exception as e:
            messagebox.showerror('Error', f'Revealing image failed: {e}')

    def hide_text(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[('Carrier image', '*.png;')])
            choice = messagebox.askquestion('Text input', 'Select a file or enter text')
            if choice == 'yes':
                text_filepath = filedialog.askopenfilename(filetypes=[('Text to hide', '*.txt;')])
                with open(text_filepath, 'r') as f:
                    text = f.read()
            else:
                text = simpledialog.askstring('Text', 'Enter text to hide:')
            carrier_image = lsb.hide(filepath, text)
            root, extension = splitext(filepath)
            filepath = f'{root}_hidden_text{extension}'
            carrier_image.save(filepath)
            messagebox.showinfo('Success', f'Text hidden successfully. Stego image saved to {filepath}')
            carrier_image.show()
        except Exception as e:
            messagebox.showerror('Error', f'Hiding text failed: {e}')

    def reveal_text(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[('Stego image', '*.png;')])
            revealed_text = lsb.reveal(filepath)
            root, extension = splitext(filepath)
            filepath = f'{root}_revealed_text.txt'
            with open(filepath, 'wb') as f:
                f.write(revealed_text.encode('utf-8'))
            messagebox.showinfo('Success', f'Text revealed successfully. Revealed text saved to {filepath}')
            startfile(filepath)
        except Exception as e:
            messagebox.showerror('Error', f'Revealing text failed: {e}')
