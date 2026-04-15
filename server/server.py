from crypto.aes_secure import decrypt_message

def server_process(final_key, nonce, ciphertext, tag):
    print("[SERVER] Receiving encrypted message")

    plaintext = decrypt_message(final_key, nonce, ciphertext, tag)
    print("[SERVER] Decrypted message:", plaintext)
