import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"
headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("📄 Documents")

uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx", "txt", "csv"])

if uploaded_file:
    with st.spinner("Uploading..."):
        try:
            res = requests.post(
                f"{BACKEND_URL}/upload",
                files={"file": uploaded_file},
                headers=headers
            )

            if res.status_code == 200:
                st.success("Document indexed successfully!")
            else:
                st.error(res.text)

        except Exception as e:
            st.error(e)