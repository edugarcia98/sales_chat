import os

from decouple import config
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain_openai import ChatOpenAI

from .constants import PLACEHOLDER, SYSTEM_TEMPLATE

os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")


class Chat:
    @staticmethod
    def _create_prompt() -> ChatPromptTemplate:
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE),
                MessagesPlaceholder(variable_name=PLACEHOLDER),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )

        return prompt

    def create_chat(self) -> ConversationChain:
        prompt = self._create_prompt()

        llm = ChatOpenAI(temperature=1)
        memory = ConversationBufferMemory(return_messages=True)
        conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)       

        return conversation


chat = Chat().create_chat()
