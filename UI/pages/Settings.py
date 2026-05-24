import streamlit as st

st.title("⚙️ Settings")

if st.button("🧹 Clear Chat History"):
    st.session_state.messages = []
    st.success("Chat cleared!")