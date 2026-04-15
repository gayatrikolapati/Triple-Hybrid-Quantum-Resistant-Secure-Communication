from Crypto.Cipher import ChaCha20_Poly1305


# -------------------------------
# TEXT ENCRYPTION
# -------------------------------
def encrypt_message(key, message):
    cipher = ChaCha20_Poly1305.new(key=key)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return cipher.nonce, ciphertext, tag


# -------------------------------
# TEXT DECRYPTION
# -------------------------------
def decrypt_message(key, nonce, ciphertext, tag):
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode()


# -------------------------------
# FILE ENCRYPTION
# -------------------------------
def encrypt_file(input_path, output_path, key):
    cipher = ChaCha20_Poly1305.new(key=key)

    with open(input_path, "rb") as f:
        data = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(data)

    with open(output_path, "wb") as f:
        f.write(cipher.nonce + tag + ciphertext)


# -------------------------------
# FILE DECRYPTION
# -------------------------------
def decrypt_file(input_path, output_path, key):
    with open(input_path, "rb") as f:
        nonce = f.read(12)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    with open(output_path, "wb") as f:
        f.write(data)