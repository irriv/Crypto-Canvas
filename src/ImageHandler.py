from tkinter import filedialog, simpledialog, messagebox
from secrets import token_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from os import startfile
from os.path import splitext
from stegano import lsb

class ImageHandler:
    """Handles image encryption, decryption, hiding, and revealing operations."""

    def encrypt_image(self, image_data):
        """Encrypts image data using AES-256-GCM.

        Args:
            image_data (bytes): The image data to be encrypted.

        """
        nonce = token_bytes(12)
        key = token_bytes(32)
        password = simpledialog.askstring('Password', 'Enter password for resulting file:')
        if password is None:
            self.show_error('Operation canceled.')
            return
        try:
            password = password.encode('utf-8')
        except UnicodeEncodeError as e:
            self.show_error('Invalid password.')
            return
        ciphertext = AESGCM(key).encrypt(nonce, image_data, password)
        filepath = self.get_save_image_filepath()
        if not filepath:
            self.show_error('Operation canceled.')
            return
        with open(filepath, 'wb') as encrypted_file:
            encrypted_file.write(ciphertext)
        self.show_success(f'Encryption successful. Encrypted image saved to {filepath}')
        root, _ = splitext(filepath)
        info_filepath = f'{root}_encryption_info.txt'
        with open(info_filepath, 'w') as file:
            file.write('Nonce: ' + nonce.hex() + '\n')
            file.write('Key: ' + key.hex() + '\n')
            try:
                file.write('Password: ' + password.decode('utf-8') + '\n')
            except UnicodeEncodeError as e:
                self.show_error('Password could not be written.')
        self.show_success(f'Encryption info written to {info_filepath}')
        startfile(filepath)
        startfile(info_filepath)

    def decrypt_image(self, image_data):
        """Decrypts image data.

        Args:
            image_data (bytes): The image data to be decrypted.

        """
        nonce = simpledialog.askstring('Nonce', 'Enter nonce:')
        if not nonce:
            self.show_error('Operation canceled.')
            return
        try:
            nonce = bytes.fromhex(nonce)
        except ValueError as e:
            self.show_error('Invalid nonce.')
            return
        key = simpledialog.askstring('Key', 'Enter key:')
        if not key:
            self.show_error('Operation canceled.')
            return
        try:
            key = bytes.fromhex(key)
        except ValueError as e:
            self.show_error('Invalid key.')
            return
        password = simpledialog.askstring('Password', 'Enter password:')
        if password is None:
            self.show_error('Operation canceled.')
            return
        try:
            password = password.encode('utf-8')
        except UnicodeEncodeError as e:
            self.show_error('Invalid password.')
            return
        try:
            decrypted_data = AESGCM(key).decrypt(nonce, image_data, password)
        except InvalidTag as e:
            self.show_error('Decryption failed.')
            return
        filepath = self.get_save_image_filepath()
        if not filepath:
            self.show_error('Operation canceled.')
            return
        with open(filepath, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
        self.show_success(f'Decryption successful. Decrypted image saved to {filepath}')
        startfile(filepath)

    def hide_image(self, carrier_image_path, secret_image_data):
        """Hides an image within another image.

        Args:
            carrier_image_path (str): The path to the carrier image.
            secret_image_data (bytes): The image data to be hidden.

        """
        hex_string = secret_image_data.hex()
        try:
            carrier_image = lsb.hide(carrier_image_path, hex_string)
        except Exception as e:
            self.show_error('The message you want to hide is too long for the carrier.')
            return
        root, _ = splitext(carrier_image_path)
        filepath = self.get_save_image_filepath()
        if not filepath:
            self.show_error('Operation canceled.')
            return
        carrier_image.save(filepath)
        self.show_success(f'Image hidden successfully. Stego image saved to {filepath}')
        carrier_image.show()

    def reveal_image(self, filepath):
        """Reveals a hidden image from a steganographic image.

        Args:
            filepath (str): The path to the stego image.

        """
        hex_string = lsb.reveal(filepath)
        if not hex_string:
            self.show_error('No hidden image found.')
            return
        filepath = self.get_save_image_filepath()
        if not filepath:
            self.show_error('Operation canceled.')
            return
        with open(filepath, 'wb') as f:
            f.write(bytes.fromhex(hex_string))
        self.show_success(f'Image revealed successfully. Revealed image saved to {filepath}')
        startfile(filepath)

    def hide_text(self, carrier_image_path, secret_text):
        """Hides text within an image.

        Args:
            carrier_image_path (str): The path to the carrier image.
            secret_text (str): The text to be hidden.

        """
        try:
            carrier_image = lsb.hide(carrier_image_path, secret_text)
        except Exception as e:
            self.show_error('The message you want to hide is too long for the carrier.')
            return
        filepath = self.get_save_image_filepath()
        if not filepath:
            self.show_error('Operation canceled.')
            return
        carrier_image.save(filepath)
        self.show_success(f'Text hidden successfully. Stego image saved to {filepath}')
        carrier_image.show()

    def reveal_text(self, filepath):
        """Reveals text hidden within an image.

        Args:
            filepath (str): The path to the stego image.

        """
        revealed_text = lsb.reveal(filepath)
        if not revealed_text:
            self.show_error('No hidden text found.')
            return
        filepath = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('TXT files','*.txt')])
        if not filepath:
            self.show_error('Operation canceled.')
            return
        with open(filepath, 'w') as f:
            f.write(revealed_text)
        self.show_success(f'Text revealed successfully. Revealed text saved to {filepath}')
        startfile(filepath)

    def show_success(self, msg):
        """Displays a success message.

        Args:
            msg (str): The message to display.

        """
        messagebox.showinfo('Success', msg)

    def show_error(self, msg):
        """Displays an error message.

        Args:
            msg (str): The error message to display.

        """
        messagebox.showerror('Error', msg)

    def get_save_image_filepath(self):
        """Opens a dialog to get the filepath to save an image.

        Returns:
            str: The filepath selected by the user or an empty string if canceled.

        """
        return filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files','*.png')])
