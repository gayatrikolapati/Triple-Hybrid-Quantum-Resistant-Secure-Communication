import uuid
import time
from crypto.quantum_qkd import generate_quantum_key

# In-memory store
qkd_store = {}

# Expiry time (seconds)
KEY_EXPIRY_SECONDS = 300  # 5 minutes


def generate_qkd_key():
    key_id = str(uuid.uuid4())

    key_str = generate_quantum_key(128)
    key_bytes = int(key_str, 2).to_bytes(16, 'big')

    qkd_store[key_id] = {
        "key": key_bytes,
        "timestamp": time.time()
    }

    return key_id, key_bytes


def fetch_qkd_key(key_id):
    record = qkd_store.get(key_id)

    if not record:
        return None

    current_time = time.time()

    # Expiry check
    if current_time - record["timestamp"] > KEY_EXPIRY_SECONDS:
        del qkd_store[key_id]
        return None

    return record["key"]