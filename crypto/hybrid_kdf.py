import hashlib


def derive_final_key(ecdh_key, kyber_key, qkd_key):
    """
    Hybrid key derivation using:
    1. SHA3 normalization
    2. Weighted XOR mixing
    3. SHA3 final derivation
    """

    # ----------------------------
    # Step 1: SHA3 normalization
    # ----------------------------

    k1 = hashlib.sha3_256(ecdh_key).digest()
    k2 = hashlib.sha3_256(kyber_key).digest()
    k3 = hashlib.sha3_256(qkd_key).digest()


    # ----------------------------
    # Step 2: Weighted XOR mixing
    # ----------------------------

    mixed = bytearray(32)

    for i in range(32):

        a = k1[i]
        b = k2[i]
        c = k3[i]

        # weighted mixing
        mixed[i] = (a ^ ((b << 1) & 0xFF) ^ (c >> 1)) & 0xFF


    # ----------------------------
    # Step 3: SHA3 final derivation
    # ----------------------------

    final_key = hashlib.sha3_256(bytes(mixed)).digest()

    return final_key