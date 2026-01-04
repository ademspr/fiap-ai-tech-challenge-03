import os

import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

from chatbot.chatbot import ChatBot

load_dotenv()

MODEL_NAME = "fiap-3"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "medical"),
    "password": os.getenv("DB_PASSWORD", "password123"),
    "dbname": os.getenv("DB_NAME", "medical_assistant"),
}

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


if __name__ == "__main__":
    st.set_page_config(
        page_title="FIAP Fase 03 - Medical Assistant",
        page_icon="🏥",
        layout="wide"
    )

    st.title("🏥 Medical Assistant")
    st.caption("Fine-tuned Llama 3.2 3B")

    with st.spinner("Starting..."):
        if "db_connection" not in st.session_state:
            st.session_state.db_connection = get_db_connection()

        if "chatbot" not in st.session_state:
            model = ChatOllama(
                model=MODEL_NAME,
                temperature=0.3,
                base_url=f"http://{OLLAMA_HOST}:11434",
            )
            st.session_state.chatbot = ChatBot(llm=model)

        # Initialize UI messages
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
