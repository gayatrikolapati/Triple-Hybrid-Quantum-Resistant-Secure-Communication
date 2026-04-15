import os

def generate_quantum_key(bits=128):
    return ''.join(format(b, '08b') for b in os.urandom(bits // 8))
