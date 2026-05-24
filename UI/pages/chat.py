import streamlit as st
import requests
import time

BACKEND_URL = "http://127.0.0.1:8000"
headers = {"Authorization": f"Bearer {st.session_state.token}"}


st.set_page_config(page_title="DocuChat AI", page_icon="💬")


st.markdown("""
<style>
.chat-container {
    max-width: 750px;
    margin: auto;
}

.user-msg {
    background-color: #2563eb;
    color: white;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
    width: fit-content;
    margin-left: auto;
}

.assistant-msg {
    background-color: #111827;
    color: #e5e7eb;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
    width: fit-content;
}

.typing {
    font-style: italic;
    color: #94a3b8;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

st.title("💬 DocuChat AI")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- RENDER CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-msg'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# ---------------- USER INPUT ----------------
prompt = st.chat_input("Ask something about your document...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='user-msg'>🧑 {prompt}</div>", unsafe_allow_html=True)

    typing_placeholder = st.empty()

    with typing_placeholder:
        st.markdown("<div class='typing'>🤖 Thinking...</div>", unsafe_allow_html=True)

    try:
        res = requests.post(
            f"{BACKEND_URL}/chat",
            params={"query": prompt},
            headers=headers,
            timeout=150
        )

        if res.status_code == 200:
            answer = res.json().get("answer", "No response")
        else:
            answer = res.text

    except Exception as e:
        answer = f"Backend error: {e}"

    typing_placeholder.empty()

    # ---------------- TYPING ANIMATION ----------------
    animated_text = ""
    output_placeholder = st.empty()

    for char in answer:
        animated_text += char
        output_placeholder.markdown(
            f"<div class='assistant-msg'>🤖 {animated_text}</div>",
            unsafe_allow_html=True
        )
        time.sleep(0.01)  # typing speed

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
