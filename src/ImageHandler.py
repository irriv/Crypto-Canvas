from tkinter import filedialog, simpledialog, messagebox
from secrets import token_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from os import startfile
from os import remove
from os.path import splitext
from stegano import lsb
from stegano.lsb import generators
from argon2 import PasswordHasher
import base64
from PIL import UnidentifiedImageError

class ImageHandler:
    """Handles image encryption, decryption, hiding, and revealing operations."""

    def __init__(self):
        """Initialize the Authenticator."""
        self.password_hasher = PasswordHasher(time_cost=1, memory_cost=47104, parallelism=1, hash_len=32, salt_len=16)

    def derive_key(self, password, salt):
        """Derives a cryptographic key from the given password and salt.

        Args:
            password (str): The password to derive the key from.
            salt (bytes): The salt used in key derivation.

        Returns:
            bytes: The derived cryptographic key.

        """
        output = self.password_hasher.hash(password, salt=salt) # Get output of hasher
        encoded_hash = output.split('$')[-1] # Unpadded b64 encoded hash
        return base64.b64decode(encoded_hash + "=") # Add padding and decode hash

    def encrypt_image(self, image_data):
        """Encrypts image data using AES-256-GCM.

        Args:
            image_data (bytes): The image data to be encrypted.

        """
        password = simpledialog.askstring('Password', 'Enter password for resulting file:')
        if password is None:
            self.show_error('Operation canceled.')
            return
        try:
            password = password.encode('utf-8')
        except UnicodeEncodeError as e:
            self.show_error('Invalid password.')
            return
        nonce = token_bytes(12) # Initialization Vector (IV)
        salt = token_bytes(16) # Generate random salt
        key = self.derive_key(password, salt)
        ciphertext = nonce + AESGCM(key).encrypt(nonce, image_data, password) + salt
        filepath = self.get_save_image_filepath()
        if not filepath:
            self.show_error('Operation canceled.')
            return
        with open(filepath, 'wb') as encrypted_file:
            encrypted_file.write(ciphertext)
        self.show_success(f'Encryption successful. Encrypted image saved to {filepath}')
        startfile(filepath)

    def decrypt_image(self, image_data):
        """Decrypts image data.

        Args:
            image_data (bytes): The image data to be decrypted.

        """
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
            nonce = image_data[:12]
            salt = image_data[-16:]
            key = self.derive_key(password, salt)
            ciphertext = image_data[12:-16]
            decrypted_data = AESGCM(key).decrypt(nonce, ciphertext, password)
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
        try:
            hex_string = secret_image_data.hex()
            carrier_image = lsb.hide(carrier_image_path, hex_string, generators.eratosthenes())
        except UnidentifiedImageError as e:
            self.show_error('The carrier image could not be identified.')
            return
        except Exception as e:
            self.show_error('The message you want to hide is too long for the carrier OR the secret image could not be identified.')
            return
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
        try:
            hex_string = lsb.reveal(filepath, generators.eratosthenes())
        except UnidentifiedImageError as e:
            self.show_error('The image could not be identified.')
            return
        except IndexError as e:
            self.show_error('No hidden image found.')
            return
        if not hex_string:
            self.show_error('No hidden image found.')
            return
        filepath = self.get_save_image_filepath()
        if not filepath:
            self.show_error('Operation canceled.')
            return
        with open(filepath, 'wb') as f:
            try:
                f.write(bytes.fromhex(hex_string))
            except ValueError as e:
                f.close()
                remove(filepath)
                self.show_error('The message contained invalid characters and could not be saved. The secret message could be text instead.')
                return
        self.show_success(f'Image revealed successfully. Revealed image saved to {filepath}')
        startfile(filepath)

    def hide_text(self, carrier_image_path, secret_text):
        """Hides text within an image.

        Args:
            carrier_image_path (str): The path to the carrier image.
            secret_text (str): The text to be hidden.

        """
        try:
            carrier_image = lsb.hide(carrier_image_path, secret_text, generators.eratosthenes())
        except UnidentifiedImageError as e:
            self.show_error('The image could not be identified.')
            return
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
        try:
            revealed_text = lsb.reveal(filepath, generators.eratosthenes())
        except UnidentifiedImageError as e:
            self.show_error('The image could not be identified.')
            return
        except IndexError as e:
            self.show_error('No hidden text found.')
            return
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
