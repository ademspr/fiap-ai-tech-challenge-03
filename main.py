import streamlit as st
from langchain_ollama import ChatOllama

from chatbot.chatbot import ChatBot

MODEL_NAME = "fiap-3"


if __name__ == "__main__":
    st.set_page_config(
        page_title="FIAP Fase 03 - Medical Assistant",
        page_icon="🏥",
        layout="wide"
    )

    st.title("🏥 Medical Assistant")
    st.caption("Fine-tuned Llama 3.2 3B")

    with st.spinner("Starting..."):
        if "chatbot" not in st.session_state:
            model = ChatOllama(
                model=MODEL_NAME,
                temperature=0.3,
            )
            st.session_state.chatbot = ChatBot(llm=model)

        if "messages" not in st.session_state:
            st.session_state.messages = []

            welcome_message = (
                "Hello! I'm a medical information assistant. "
                "I can help answer general health questions, but please remember "
                "that I cannot diagnose conditions or recommend treatments. "
                "For medical concerns, always consult a healthcare professional."
            )

            st.session_state.messages.append(
                {"role": "assistant", "content": welcome_message}
            )

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask a medical question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            response = st.session_state.chatbot.ask(prompt)
            with st.chat_message("assistant"):
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
