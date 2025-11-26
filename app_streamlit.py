import streamlit as st
import requests

st.set_page_config(page_title="Chat With Transformer Paper", layout="wide")
st.title("Chat With the Paper")

question = st.text_input("Ask a question about the Transformer paper:")

if st.button("Submit"):
    if question.strip():
        try:
            res = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": question}
            ).json()

            st.subheader("💡 Answer")
            st.write(res["answer"])

        except Exception as e:
            st.error(f"Error contacting the backend: {e}")
