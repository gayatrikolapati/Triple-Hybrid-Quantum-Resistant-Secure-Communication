from server.server import server_process
from kms.qkd_kms import generate_qkd_key
from crypto.classical_ecdh import generate_ecdh_shared_secret
from crypto.pq_kyber import generate_kyber_shared_secret
from crypto.hybrid_kdf import derive_final_key
from crypto.aes_secure import encrypt_message

def client_process():
    print("[CLIENT] Preparing secure message")

    # Hybrid key generation (handshake simulated)
    ecdh = generate_ecdh_shared_secret()
    kyber = generate_kyber_shared_secret()
    _, qkd = generate_qkd_key()

    final_key = derive_final_key(ecdh, kyber, qkd)

    nonce, cipher, tag = encrypt_message(
        final_key, "Hello from Client"
    )

    server_process(final_key, nonce, cipher, tag)

client_process()
