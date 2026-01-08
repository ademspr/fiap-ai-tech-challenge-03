import os
import re

import psycopg2
import streamlit as st
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from psycopg2.extras import RealDictCursor

from chatbot.chatbot import ChatBot
from model import IdentifiedPatient
from repositories import MedicationRepository, PatientRepository

load_dotenv()

MODEL_BASE = "llama3.2:3b"
MODEL_TUNED = "fiap-3"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "medical"),
    "password": os.getenv("DB_PASSWORD", "password123"),
    "dbname": os.getenv("DB_NAME", "medical_assistant"),
}

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")


def get_db_connection():
    if "db_connection" not in st.session_state:
        st.session_state.db_connection = psycopg2.connect(
            **DB_CONFIG, cursor_factory=RealDictCursor
        )
    return st.session_state.db_connection


def normalize_cpf(cpf: str) -> str:
    return re.sub(r"\D", "", cpf)


def get_identified_patient(cpf: str) -> IdentifiedPatient | None:
    connection = get_db_connection()
    patient_repo = PatientRepository(connection)
    medication_repo = MedicationRepository(connection)

    patient = patient_repo.get_by_cpf(cpf)

    if patient is None:
        return None

    medications = medication_repo.get_active_by_patient_id(patient.id)

    return IdentifiedPatient(patient=patient, medications=medications)


def identify_patient(cpf: str) -> bool:
    normalized_cpf = normalize_cpf(cpf)

    if len(normalized_cpf) != 11:
        return False

    identified = get_identified_patient(normalized_cpf)

    if identified is None:
        return False

    st.session_state.identified_patient = identified
    st.session_state.chatbot_base.set_patient_context(identified.context)
    st.session_state.chatbot_base.clear_history()
    st.session_state.chatbot_tuned.set_patient_context(identified.context)
    st.session_state.chatbot_tuned.clear_history()

    return True


def clear_patient():
    st.session_state.identified_patient = None
    st.session_state.chatbot_base.set_patient_context("")
    st.session_state.chatbot_base.clear_history()
    st.session_state.chatbot_tuned.set_patient_context("")
    st.session_state.chatbot_tuned.clear_history()
    st.session_state.messages = []


if __name__ == "__main__":  # noqa: C901
    st.set_page_config(
        page_title="FIAP Fase 03 - Medical Assistant", page_icon="🏥", layout="wide"
    )

    st.title("🏥 Medical Assistant")
    st.caption("Comparison: Llama 3.2 3B (Base) vs Fine-tuned")

    if "chatbot_base" not in st.session_state:
        model_base = ChatOllama(
            model=MODEL_BASE,
            temperature=0.3,
            base_url=f"http://{OLLAMA_HOST}:11434",
        )
        model_tuned = ChatOllama(
            model=MODEL_TUNED,
            temperature=0.3,
            base_url=f"http://{OLLAMA_HOST}:11434",
        )
        st.session_state.chatbot_base = ChatBot(llm=model_base, use_rag=False)
        st.session_state.chatbot_tuned = ChatBot(llm=model_tuned, use_rag=True)
        st.session_state.identified_patient = None

    with st.sidebar:
        st.header("Patient Identification")

        identified = st.session_state.identified_patient

        if identified:
            st.success(f"Identified: {identified.name}")
            if st.button("Change Patient"):
                clear_patient()
                st.rerun()
        else:
            cpf_input = st.text_input(
                "Enter your CPF",
                placeholder="000.000.000-00",
                help="Enter your CPF to access your medical records",
            )

            if st.button("Identify"):
                if cpf_input:
                    if identify_patient(cpf_input):
                        st.session_state.messages = []
                        st.rerun()
                    else:
                        st.error("Patient not found. Please check your CPF.")
                else:
                    st.warning("Please enter your CPF.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        identified = st.session_state.identified_patient

        if identified:
            welcome_message = (
                f"Hello, {identified.name}! I'm your medical assistant. "
                "I can help you with questions about your medications "
                "and provide general health information. "
                "How can I help you today?"
            )
        else:
            welcome_message = (
                "Hello! I'm your medical assistant. "
                "Please identify yourself using your CPF in the sidebar "
                "so I can access your medical records and provide personalized assistance."  # noqa: E501
            )

        st.session_state.messages.append(
            {"role": "assistant", "content": welcome_message}
        )

    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        elif "base" in message and "tuned" in message:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**🔵 Base Model (Llama 3.2 3B)**")
                with st.chat_message("assistant"):
                    st.markdown(message["base"])

            with col2:
                st.markdown("**🟢 Fine-tuned Model**")
                with st.chat_message("assistant"):
                    st.markdown(message["tuned"])

                if message.get("sources"):
                    sources = message["sources"]
                    total_sources = len(sources)

                    with st.expander("📚 Sources (PubMedQA Dataset)"):
                        for i, source in enumerate(sources):
                            st.markdown(f"**PMID {source['pmid']}** ({source['year']})")
                            st.markdown(f"*Related question:* {source['question']}")
                            if source["meshes"]:
                                st.markdown(
                                    f"*Topics:* {', '.join(source['meshes'][:5])}"
                                )

                            if i < total_sources - 1:
                                st.divider()
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask a medical question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        col1, col2 = st.columns(2)

        with st.spinner("Querying models..."):
            response_base = st.session_state.chatbot_base.ask(prompt)
            response_tuned = st.session_state.chatbot_tuned.ask(prompt)

        with col1:
            st.markdown("**🔵 Base Model (Llama 3.2 3B)**")
            with st.chat_message("assistant"):
                st.markdown(response_base.content)
        with col2:
            st.markdown("**🟢 Fine-tuned Model**")
            with st.chat_message("assistant"):
                st.markdown(response_tuned.content)

            if response_tuned.sources:
                with st.expander("📚 Sources (PubMedQA Dataset)"):
                    sources = response_tuned.sources
                    total_sources = len(sources)

                    for i, source in enumerate(sources):
                        st.markdown(f"**PMID {source.pmid}** ({source.year})")
                        st.markdown(f"*Related question:* {source.question}")
                        if source.meshes:
                            st.markdown(f"*Topics:* {', '.join(source.meshes[:5])}")

                        if i < total_sources - 1:
                            st.divider()

        st.session_state.messages.append(
            {
                "role": "assistant",
                "base": response_base.content,
                "tuned": response_tuned.content,
                "sources": [
                    {
                        "pmid": s.pmid,
                        "year": s.year,
                        "question": s.question,
                        "meshes": s.meshes,
                    }
                    for s in response_tuned.sources
                ],
            }
        )
