import streamlit as st

st.set_page_config(layout="wide")

st.title("🔐 Hybrid Encryption Pipeline")

# -------------------------------
# STATE CHECKS (CORRECTED)
# -------------------------------
kms = "key_id" in st.session_state and st.session_state["key_id"]
client = "ecdh_key" in st.session_state and st.session_state["ecdh_key"]

# CLIENT ENCRYPTED
encrypted = (
    st.session_state.get("ciphertext") is not None
    or st.session_state.get("encrypted_file") is not None
)

# SERVER DECRYPTED (FIXED)
decrypted = (
    st.session_state.get("decrypted_file") is not None
    or st.session_state.get("text_decrypted") is True
)

# -------------------------------
# STEP BOX UI
# -------------------------------
def step_box(title, status):
    color = "#28a745" if status else "#6c757d"
    text = "✔ Completed" if status else "⏳ Pending"

    return f"""
    <div style="
        padding:20px;
        border-radius:15px;
        text-align:center;
        background-color:{color};
        color:white;
        font-weight:bold;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.3);
    ">
        {title}<br><br>
        {text}
    </div>
    """

# -------------------------------
# PIPELINE ROW
# -------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(step_box("🔐 KMS Key", kms), unsafe_allow_html=True)

with col2:
    st.markdown(step_box("👤 Client Keys", client), unsafe_allow_html=True)

with col3:
    st.markdown(step_box("🔒 Client Encrypt", encrypted), unsafe_allow_html=True)

with col4:
    st.markdown(step_box("📡 Data Transfer", encrypted), unsafe_allow_html=True)

with col5:
    st.markdown(step_box("🔓 Server Decrypt", decrypted), unsafe_allow_html=True)

# -------------------------------
# CONNECTOR LINE
# -------------------------------
st.markdown("""
<div style="
    height: 5px;
    background: linear-gradient(to right, #28a745, #00c6ff);
    margin: 25px 0;
    border-radius: 5px;
">
</div>
""", unsafe_allow_html=True)

# -------------------------------
# PROGRESS BAR
# -------------------------------
steps = [kms, client, encrypted, decrypted]
progress = sum(1 for s in steps if s) / len(steps)

st.markdown("### 🚀 Execution Progress")
st.progress(progress)

# -------------------------------
# DETAILS PANEL
# -------------------------------
st.markdown("### 📊 Detailed System Status")

colA, colB = st.columns(2)

with colA:
    st.info("🔐 Key Management")
    st.write("KMS Key:", "✔" if kms else "❌")
    st.write("Client Keys:", "✔" if client else "❌")

with colB:
    st.info("🔄 Data Flow")
    st.write("Encrypted at Client:", "✔" if encrypted else "❌")
    st.write("Decrypted at Server:", "✔" if decrypted else "❌")

# -------------------------------
# SECURITY INFO
# -------------------------------
st.markdown("### 🔐 Security Flow Insight")

st.success("""
✔ Client encrypts data before sending  
✔ Data is transmitted securely  
✔ Server performs only decryption  
✔ Hybrid key ensures quantum resistance  
""")

# -------------------------------
# DEBUG
# -------------------------------
with st.expander("🔍 Internal Session Data"):
    st.json({k: str(v) for k, v in st.session_state.items()})