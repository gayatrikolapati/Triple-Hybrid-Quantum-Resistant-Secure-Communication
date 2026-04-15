import streamlit as st
import time
from kms.qkd_kms import generate_qkd_key

st.title("🔐 KMS – Quantum Key Generation")

# SESSION INIT
for key in ["key_id", "qkd_key", "key_time"]:
    if key not in st.session_state:
        st.session_state[key] = None

# INIT BUTTON
if st.button("Initialize Session"):
    st.session_state["key_id"] = None
    st.session_state["qkd_key"] = None
    st.session_state["key_time"] = None
    st.success("Session Initialized")

st.divider()

# GENERATE KEY
if st.button("Generate QKD Key"):
    key_id, qkd_key = generate_qkd_key()
    st.session_state["key_id"] = key_id
    st.session_state["qkd_key"] = qkd_key
    st.session_state["key_time"] = time.time()
    st.success("QKD Key Generated")

# DISPLAY
if st.session_state["key_id"]:
    st.code(f"""
Key ID : {st.session_state["key_id"]}
Key Length : {len(st.session_state["qkd_key"])*8} bits
""")

# COUNTDOWN
if st.session_state["key_time"]:
    remaining = 300 - int(time.time() - st.session_state["key_time"])
    if remaining > 0:
        st.metric("⏳ Key Expiry (seconds)", remaining)
    else:
        st.error("❌ Key expired")