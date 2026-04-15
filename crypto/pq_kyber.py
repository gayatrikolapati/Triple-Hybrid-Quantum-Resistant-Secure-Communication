import os
import hashlib

def generate_kyber_shared_secret():
    """
    Simulated Post-Quantum shared secret (Kyber)
    Used due to lack of stable KEM bindings on Windows
    """
    return hashlib.sha256(os.urandom(32)).digest()
