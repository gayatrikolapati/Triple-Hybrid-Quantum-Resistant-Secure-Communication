import streamlit as st
import hashlib
import os

from kms.qkd_kms import generate_qkd_key, fetch_qkd_key
from crypto.classical_ecdh import generate_ecdh_shared_secret
from crypto.pq_kyber import generate_kyber_shared_secret
from crypto.hybrid_kdf import derive_final_key
from crypto.aes_secure import encrypt_message, decrypt_message


st.set_page_config(page_title="Triple-Hybrid Quantum-Resistant Security", layout="centered")

st.title("🔐 Triple-Hybrid Quantum-Resistant Secure Communication")
st.write("Classical (ECDH) + Post-Quantum (Kyber) + QKD (Simulated)")

st.divider()

# =========================
# STEP 1: QKD via KMS
# =========================
st.subheader("1️⃣ QKD Key Generation (KMS)")

key_id, qkd_key = generate_qkd_key()

st.code(f"""
[KMS] QKD Key Generated
Key ID : {key_id}
Key Length : {len(qkd_key)*8} bits
""")

st.success("QKD key securely stored in KMS (key not transmitted)")

# retrieve from KMS
retrieved_qkd = fetch_qkd_key(key_id)


# =========================
# STEP 2: Classical ECDH
# =========================
st.subheader("2️⃣ Classical ECDH Key Exchange")

ecdh_key = generate_ecdh_shared_secret()

st.code("""
[Client] ECDH keypair generated
[Server] ECDH shared secret computed
""")

st.success("ECDH shared secret established")


# =========================
# STEP 3: Post-Quantum Kyber
# =========================
st.subheader("3️⃣ Post-Quantum Kyber Key Exchange")

kyber_key = generate_kyber_shared_secret()

st.code("""
[Client] Kyber public key generated
[Server] Kyber shared secret derived
""")

st.success("Post-Quantum shared secret established")


# =========================
# STEP 4: Hybrid Key Derivation
# =========================
st.subheader("4️⃣ Hybrid Key Derivation (HKDF-style)")

salt = os.urandom(16)
context = b"TripleHybridSession"
session_id = os.urandom(8)

final_key = derive_final_key(ecdh_key, kyber_key, retrieved_qkd, salt, context, session_id)

key_hash = hashlib.sha256(final_key).hexdigest()[:16]

st.code(f"""
Hybrid Session Key (SHA-256 Fingerprint)

ECDH Key Length : {len(ecdh_key)*8} bits
Kyber Key Length : {len(kyber_key)*8} bits
QKD Key Length : {len(retrieved_qkd)*8} bits
Final Hybrid Key : {len(final_key)*8} bits

Key Hash : {key_hash}
""")

st.success("Hybrid session key derived successfully")


# =========================
# STEP 5: Secure Communication
# =========================
st.subheader("5️⃣ Secure Communication (AES-GCM)")

message = st.text_input("Enter message", "Hello Quantum-Secure World")

nonce, ciphertext, tag = encrypt_message(final_key, message)
decrypted = decrypt_message(final_key, nonce, ciphertext, tag)

st.write("🔹 AES Nonce")
st.code(nonce.hex())

st.write("🔹 Encrypted Message")
st.code(ciphertext.hex())

st.write("🔹 Authentication Tag")
st.code(tag.hex())

st.write("🔹 Decrypted Message")
st.code(decrypted)

st.success("Secure communication successful")

st.divider()

st.caption("Prototype demonstrating triple-hybrid quantum-resistant TLS-like workflow.")