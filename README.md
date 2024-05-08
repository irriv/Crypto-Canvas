# Crypto-Canvas
Image encryption/decryption, image and text-based steganography tool with a local SQLite database and custom authentication system.

![GUI](https://github.com/irriv/Crypto-Canvas/assets/105553132/ccd82381-d553-4c46-9315-0c94b3adbd78)
## Security features
- Encryption with AES-256-GCM
- Password storing and authentication with Argon2id
- Obscurity through LSB steganography
## How to install
The program requires Python 3.9 at minimum.
Libraries used:
- cryptography `pip install cryptography`
- stegano `pip install stegano`
- argon2 `pip install argon2-cffi`

Other libraries are included in Python's standard library.
## How to use
To run the program, run `python main.py` or `py main.py`.

Signing in grants access to the **database feature**. The user can store images in the database and use them for the operations in the program. The database can be navigated with **mouse and arrow keys**.

For the image operations, simply choose an image file from the database or the device for the given operation. The **Hide image** -operation requires two images to be chosen; the first image will hide the second image within itself.

All files created by the program are saved on the **user's device** and can later be added to the database manually.
