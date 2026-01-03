from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama


class ChatBot:
    def __init__(self, llm: ChatOllama):
        self.llm = llm
        self.chat_history: list[HumanMessage | AIMessage] = []
        self.prompt = self.__get_prompt()
        self.chain = self.prompt | self.llm

    @staticmethod
    def __get_prompt():
        system_prompt = """You are an AI medical information assistant.

STRICT RULES:
1. Answer in 2-4 short sentences maximum. Be direct.
2. NEVER diagnose conditions or prescribe/recommend medications.
3. NEVER invent disease names, drug names, or mix medical information.
4. NEVER mention institution names, signatures, or introduce yourself.
5. NEVER include statistics, study results, or academic citations.
6. If asked about treatment, say "Consult a healthcare professional."

If unsure, say "I don't have reliable information on this topic. Please consult a healthcare professional.\""""

        return ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("human", "{input}"),
            ]
        )

    def ask(self, prompt: str) -> str:
        response = self.chain.invoke(
            {"input": prompt, "chat_history": self.chat_history}
        )

        self.chat_history.append(HumanMessage(content=prompt))
        self.chat_history.append(AIMessage(content=response.content))

        return str(response.content)

    def clear_history(self):
        self.chat_history = []
