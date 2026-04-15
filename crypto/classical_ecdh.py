from cryptography.hazmat.primitives.asymmetric import ec

def generate_ecdh_shared_secret():
    private_key = ec.generate_private_key(ec.SECP256R1())
    peer_private_key = ec.generate_private_key(ec.SECP256R1())

    shared_secret = private_key.exchange(
        ec.ECDH(),
        peer_private_key.public_key()
    )

    return shared_secret
