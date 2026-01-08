from dataclasses import dataclass

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama

from model import PubMedSource
from tools.pubmed_search import search_pubmed


@dataclass
class ChatResponse:
    content: str
    sources: list[PubMedSource]


class ChatBot:
    def __init__(
        self, llm: ChatOllama, patient_context: str = "", use_rag: bool = False
    ):
        self.llm = llm
        self.patient_context = patient_context
        self.use_rag = use_rag
        self.chat_history: list[HumanMessage | AIMessage] = []

    @staticmethod
    def _get_prompt(with_rag: bool = False):
        prompt = """You are an AI medical information assistant.

        CURRENT ACTIVE MEDICATIONS:
        {patient_context}
        """

        if with_rag:
            prompt += """

        REFERENCE KNOWLEDGE BASE (use this to inform your answer):
        {rag_context}"""

        prompt += """

        STRICT RULES:
        1. Answer in 2-4 short sentences maximum. Be direct.
        2. NEVER diagnose conditions or prescribe/recommend medications the patient doesn't takes already.
        3. NEVER invent disease names, drug names, or mix medical information.
        4. NEVER mention institution names, signatures, or introduce yourself.
        5. If asked about treatment, say "Consult a healthcare professional."

        If unsure, say "I don't have reliable information on this topic. Please consult a healthcare professional."
        """  # noqa: E501

        return ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("human", "{input}"),
            ]
        )

    @staticmethod
    def _build_rag_context(sources: list[PubMedSource]) -> str:
        if not sources:
            return "No relevant references found."

        context_parts = []
        for source in sources:
            part = f"[PMID: {source.pmid}, Year: {source.year}]\n"
            part += f"Question: {source.question}\n"

            for context, label in zip(source.contexts, source.labels):
                truncated = context[:450] + "..." if len(context) > 450 else context
                part += f"{label}: {truncated}\n"

            context_parts.append(part)

        return "\n---\n".join(context_parts)

    def set_patient_context(self, patient_context: str) -> None:
        self.patient_context = patient_context

    def ask(self, prompt: str) -> ChatResponse:
        sources = []
        invoke_params = {
            "input": prompt,
            "chat_history": self.chat_history,
            "patient_context": self.patient_context,
        }

        if self.use_rag:
            sources = search_pubmed(prompt, top_k=2)
            invoke_params["rag_context"] = self._build_rag_context(sources)

        prompt_template = self._get_prompt(with_rag=self.use_rag)
        chain = prompt_template | self.llm
        response = chain.invoke(invoke_params)

        self.chat_history.append(HumanMessage(content=prompt))
        self.chat_history.append(AIMessage(content=response.content))

        return ChatResponse(content=str(response.content), sources=sources)

    def clear_history(self) -> None:
        self.chat_history = []
