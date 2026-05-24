import streamlit as st
import requests
import time

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DocuChat AI",
    page_icon="📄💬",
    layout="centered"
)

if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "messages" not in st.session_state:
    st.session_state.messages = []


st.markdown("""
<style>


.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #F9FAFB;
}


section[data-testid="stSidebar"] {
    animation: slideIn 0.6s ease-out;
    background: #0B1220;
    border-right: 1px solid rgba(255,255,255,0.05);
}


section[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

/* Headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #F9FAFB !important;
}


section[data-testid="stSidebar"] button {
    background-color: #1F2937 !important;
    color: #F9FAFB !important;
    border-radius: 8px;
}


section[data-testid="stSidebar"] label {
    color: #D1D5DB !important;
}


@keyframes slideIn {
    from { transform: translateX(-30px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}


.chat-user {
    background-color: #3B82F6;
    color: white;
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 8px;
    max-width: 80%;
}

.chat-assistant {
    background-color: #0F172A;
    color: #E5E7EB;
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 12px;
    max-width: 80%;
    border: 1px solid rgba(255,255,255,0.05);
}


footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ---------------- AUTH SCREEN ----------------
if not st.session_state.token:

    st.markdown("<h1 style='text-align:center;'>📄💬 DocuChat AI</h1>", unsafe_allow_html=True)
    st.caption("Secure Document Intelligence Assistant")

    tab1, tab2 = st.tabs(["Login", "Create Account"])

    # ---------- LOGIN ----------
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.form_submit_button("Login"):
                if not username or not password:
                    st.warning("Enter username & password")
                else:
                    try:
                        res = requests.post(
                            f"{BACKEND_URL}/login",
                            params={"username": username, "password": password}
                        )

                        if res.status_code == 200:
                            st.session_state.token = res.json()["access_token"]
                            st.session_state.username = username
                            st.success("Login successful")
                            st.rerun()
                        else:
                            st.error("Invalid credentials")

                    except Exception as e:
                        st.error(f"Backend error: {e}")

    # ---------- SIGNUP ----------
    with tab2:
        with st.form("signup_form"):
            new_user = st.text_input("New Username")
            new_pass = st.text_input("New Password", type="password")

            if st.form_submit_button("Create Account"):
                if not new_user or not new_pass:
                    st.warning("Enter username & password")
                else:
                    try:
                        res = requests.post(
                            f"{BACKEND_URL}/signup",
                            params={"username": new_user, "password": new_pass}
                        )

                        if res.status_code == 200:
                            st.success("Account created successfully 🎉")
                        else:
                            st.error(res.text)

                    except Exception as e:
                        st.error(f"Backend error: {e}")

    st.stop()

# ---------------- AUTH HEADER ----------------
headers = {"Authorization": f"Bearer {st.session_state.token}"}


st.markdown(
    "<h1 style='text-align:center;'>📄💬 DocuChat AI</h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<p style='text-align:center;'>Logged in as <b>{st.session_state.username}</b></p>",
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.success(f"👤 {st.session_state.username}")

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.username = None
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload document",
        type=["pdf", "docx", "txt", "csv"]
    )

    if uploaded_file:
        with st.spinner("Indexing document..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/upload",
                    files={"file": uploaded_file},
                    headers=headers
                )

                if res.status_code == 200:
                    st.success("Document indexed successfully")
                else:
                    st.error(res.text)

            except Exception as e:
                st.error(e)

    st.markdown("---")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- CHAT ----------------
st.subheader("💬 Chat")

for msg in st.session_state.messages:
    css = "chat-user" if msg["role"] == "user" else "chat-assistant"
    icon = "🧑" if msg["role"] == "user" else "🤖"

    st.markdown(
        f"<div class='{css}'>{icon} {msg['content']}</div>",
        unsafe_allow_html=True
    )

prompt = st.chat_input("Ask a question about your document...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    thinking = st.empty()
    thinking.markdown("<i>🤖 Thinking...</i>", unsafe_allow_html=True)

    try:
        res = requests.post(
            f"{BACKEND_URL}/chat",
            params={"query": prompt},
            headers=headers
        )

        answer = res.json().get("answer", "") if res.status_code == 200 else res.text

    except Exception as e:
        answer = str(e)

    thinking.empty()

    animated = ""
    output = st.empty()

    for char in answer:
        animated += char
        output.markdown(
            f"<div class='chat-assistant'>🤖 {animated}</div>",
            unsafe_allow_html=True
        )
        time.sleep(0.01)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()