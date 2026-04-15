from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import random


def generate_quantum_chunk(n=8):   # keep VERY small (safe)
    backend = Aer.get_backend("aer_simulator")

    qc = QuantumCircuit(n, n)

    for i in range(n):
        if random.choice([0, 1]):
            qc.x(i)
        if random.choice([0, 1]):
            qc.h(i)

    qc.measure(range(n), range(n))

    compiled = transpile(qc, backend)
    result = backend.run(compiled, shots=1).result()

    return list(result.get_counts().keys())[0]


def generate_quantum_key(n=128):
    key = ""

    while len(key) < n:
        key += generate_quantum_chunk(8)   # NOT 128, NOT 32

    return key[:n]