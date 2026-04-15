import streamlit as st
import hashlib
import os
import time

from kms.qkd_kms import fetch_qkd_key
from crypto.hybrid_kdf import derive_final_key
from crypto.aes_secure import decrypt_message, decrypt_file

st.title("🖥️ Server – Decryption")

# -------------------------------
# KEY EXPIRY
# -------------------------------
if "key_time" in st.session_state:
    remaining = 300 - int(time.time() - st.session_state["key_time"])
    if remaining > 0:
        st.info(f"⏳ Key expires in {remaining} sec")
    else:
        st.error("Key expired")
        st.stop()

# -------------------------------
# VALIDATION
# -------------------------------
required = ["key_id", "ecdh_key", "kyber_key"]

if any(k not in st.session_state for k in required):
    st.error("Client not ready")
    st.stop()

data_type = st.session_state.get("data_type")

if data_type is None:
    st.warning("⚠ No data received from client")
    st.stop()

# -------------------------------
# FETCH KEY
# -------------------------------
qkd_key = fetch_qkd_key(st.session_state["key_id"])

if qkd_key is None:
    st.error("Key expired in KMS")
    st.stop()

# -------------------------------
# DERIVE KEY
# -------------------------------
final_key = derive_final_key(
    st.session_state["ecdh_key"],
    st.session_state["kyber_key"],
    qkd_key
)[:32]

fingerprint = hashlib.sha256(final_key).hexdigest()[:16]

st.success("Shared Key Ready")
st.write(f"🔑 Fingerprint: {fingerprint}")

st.divider()

# =========================================================
# TEXT DECRYPT
# =========================================================
if data_type in ["text", "both"]:

    st.subheader("📝 Text Decryption")

    if "ciphertext" in st.session_state:

        if st.button("Decrypt Text"):

            decrypted = decrypt_message(
                final_key,
                st.session_state["nonce"],
                st.session_state["ciphertext"],
                st.session_state["tag"]
            )

            st.session_state["text_decrypted"] = True

            st.code(decrypted)

# =========================================================
# FILE DECRYPT
# =========================================================
if data_type in ["file", "both"]:

    st.subheader("📁 File Decryption")

    if "encrypted_file" in st.session_state:

        if st.button("Decrypt File"):

            output_name = "decrypted_" + st.session_state["original_name"]

            decrypt_file(
                st.session_state["encrypted_file"],
                output_name,
                final_key
            )

            st.session_state["decrypted_file"] = output_name

            st.success("File Decrypted")

            # preview if image
            if output_name.lower().endswith((".png", ".jpg", ".jpeg")):
                st.image(output_name, use_container_width=True)

            with open(output_name, "rb") as f:
                st.download_button("Download Decrypted File", f, output_name)