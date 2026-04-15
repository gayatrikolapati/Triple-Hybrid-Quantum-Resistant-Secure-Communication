import streamlit as st
import os

from crypto.hybrid_kdf import derive_final_key
from crypto.aes_secure import encrypt_message, encrypt_file
from kms.qkd_kms import fetch_qkd_key

st.title("👤 Client – Encrypt & Send Data")

# -------------------------------
# SESSION INIT
# -------------------------------
for key in ["ecdh_key", "kyber_key"]:
    if key not in st.session_state:
        st.session_state[key] = None

# -------------------------------
# GENERATE KEYS
# -------------------------------
if st.button("Generate Client Keys"):
    st.session_state["ecdh_key"] = os.urandom(32)
    st.session_state["kyber_key"] = os.urandom(32)
    st.success("Client Keys Generated")

# -------------------------------
# INPUTS (BOTH OPTIONAL)
# -------------------------------
st.markdown("### 📩 Provide Data (Text / File / Both)")

msg = st.text_input("Enter Message (optional)")
uploaded = st.file_uploader("Upload File (optional)")

# -------------------------------
# SEND BUTTON
# -------------------------------
if st.button("Encrypt & Send"):

    # ❗ MAIN CONDITION (IMPORTANT)
    if (not msg.strip()) and (uploaded is None):
        st.error("❌ No data provided (send text or file)")
        st.stop()

    # Validate keys
    if not st.session_state["ecdh_key"] or not st.session_state["kyber_key"]:
        st.error("Generate client keys first")
        st.stop()

    # Fetch QKD key
    qkd_key = fetch_qkd_key(st.session_state.get("key_id"))

    if qkd_key is None:
        st.error("❌ QKD key expired or missing")
        st.stop()

    # Derive hybrid key
    final_key = derive_final_key(
        st.session_state["ecdh_key"],
        st.session_state["kyber_key"],
        qkd_key
    )[:32]

    # -------------------------------
    # TEXT HANDLING
    # -------------------------------
    if msg.strip():

        nonce, ciphertext, tag = encrypt_message(final_key, msg)

        st.session_state["ciphertext"] = ciphertext
        st.session_state["nonce"] = nonce
        st.session_state["tag"] = tag

        st.success("✔ Text Encrypted")
        st.code(ciphertext.hex())

    # -------------------------------
    # FILE HANDLING
    # -------------------------------
    if uploaded is not None:

        file_path = uploaded.name

        with open(file_path, "wb") as f:
            f.write(uploaded.read())

        encrypt_file(file_path, "encrypted.bin", final_key)

        st.session_state["encrypted_file"] = "encrypted.bin"
        st.session_state["original_name"] = file_path

        st.success("✔ File Encrypted")

        with open("encrypted.bin", "rb") as f:
            st.download_button("⬇ Download Encrypted File", f, "encrypted.bin")

    # -------------------------------
    # MARK DATA TYPE
    # -------------------------------
    if msg.strip() and uploaded:
        st.session_state["data_type"] = "both"
    elif msg.strip():
        st.session_state["data_type"] = "text"
    else:
        st.session_state["data_type"] = "file"

    st.success("🚀 Data Sent to Server")