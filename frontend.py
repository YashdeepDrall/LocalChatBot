import streamlit as st
import requests
import os

def run_frontend():
    st.set_page_config(page_title="Cybersecurity Consultant", layout="centered")
    st.title("🔐 Cybersecurity Consultancy Bot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.header("Settings")
        api_base = st.text_input("API Base URL", value="http://127.0.0.1:8000")
        
        if st.button("Check Backend Status"):
            try:
                requests.get(f"{api_base.rstrip('/')}/docs", timeout=2)
                st.success("Backend Connected")
            except Exception:
                st.error("Connection Failed")

        k = st.slider("Context documents (k)", min_value=1, max_value=10, value=3)
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "context" in message:
                with st.expander("View Context"):
                    st.text(message["context"])

    if prompt := st.chat_input("What is your question?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Consulting..."):
                try:
                    api_url = f"{api_base.rstrip('/')}/ask"
                    payload = {"question": prompt, "k": k}
                    response = requests.post(api_url, json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data["answer"]
                        context = data["context"]
                        
                        st.markdown(answer)
                        with st.expander("View Context"):
                            st.text(context)
                        
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": answer, 
                            "context": context
                        })
                    else:
                        st.error(f"Error from backend: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error(f"Could not connect to {api_url}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    run_frontend()