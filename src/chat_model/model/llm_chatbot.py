import os
import re
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from .fetch_api_tools import tools as fetch_api_tools
from .embedding import embedding_data

# Enable this when you run this file
# from fetch_api_tools import tools as fetch_api_tools
# from embedding import embedding_data

load_dotenv()

TRAINED_DIR = Path(__file__).resolve().parent / "trained"

class LlmChatBot:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, model="openai/gpt-3.5-turbo", embedding_model="sentence-transformers/all-MiniLM-L6-v2"):
        if not hasattr(self, "initialized"):
            self.VECTOR_WORDS = TRAINED_DIR / "vector_words" / "from_guides"
            
            self.embedding = HuggingFaceEmbeddings(model_name=embedding_model)
            
            self.vector_words = FAISS.load_local(
                folder_path=self.VECTOR_WORDS,
                embeddings=self.embedding,
                allow_dangerous_deserialization=True
            )

            self.llm = ChatOpenAI(
                openai_api_key=os.getenv("OPENROUTER_API"),
                openai_api_base="https://openrouter.ai/api/v1",
                temperature=0.5,
                model=model,
                max_retries=3
            )

            self.user_memory = {} 

            self.agent_executor = self._initialize_agent()

            self.initialized = True

    def _initialize_agent(self):
        tools = [self._create_retrieval_tool()] + fetch_api_tools

        prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        return initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=None, 
            verbose=True,
            prompt=prompt,
            handle_parsing_errors=True
        )

    def _get_system_prompt(self):
        return """
        You are a smart virtual assistant for an e-commerce website.
        You MUST always consider using tools provided to help you answer accurately. If unsure, try using a tool.
        If the user's question is about products, always fetch the complete product list and then respond with the relevant information.    
        You can only answer questions based on the following (only use character and number, not symbolize) topics:
        1. Website Information  
        2. How to use the website  
        3. Product Consultation  
        4. Other general inquiries  
        If the user's question is outside these topics, respond with:  
        "Sorry, I can only answer questions related to our website and services. If you need further assistance, please contact us at Phone: +843949505816 or Email: group11@gmail.com."
        Always ensure your answer is clear, detailed, and concise. Avoid using any markdown formatting, special symbols, or non-standard characters.        
        """

    def _create_retrieval_tool(self):
        retriever = self.vector_words.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 3}
        )
        return create_retriever_tool(
            retriever=retriever,
            name="ecommerce_docs",
            description="Search information from internal docs"
        )

    def load_old_conversation_to_memory(self, user_id: str, messages: list):
        if user_id not in self.user_memory:
            self.user_memory[user_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                input_key="input",
                output_key="output"
            )

        user_memory = self.user_memory[user_id]
        user_memory.clear()
        if not messages:
            return 
        
        for msg in messages:
            if msg["role"] == "user":
                user_memory.chat_memory.add_user_message(msg["content"])
            elif msg["role"] == "chatbot":
                user_memory.chat_memory.add_ai_message(msg["content"])
    



    def get_response(self, user_id: str, user_input: str) -> str:
        def clean_user_input(user_input: str) -> str:
            allowed_punctuation = r".,;:?"
            cleaned_input = re.sub(rf"[^\w\s{re.escape(allowed_punctuation)}\n]", "", user_input)
            cleaned_input = "\n".join(line.strip() for line in cleaned_input.splitlines())
            return cleaned_input
        
        try:
            if user_id not in self.user_memory:
                self.user_memory[user_id] = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True,
                    input_key="input",
                    output_key="output"
                )

            user_memory = self.user_memory[user_id]
            self.agent_executor.memory = user_memory

            response = self.agent_executor.invoke({"input": user_input})
            return clean_user_input(response["output"])
        except Exception as e:
            raise

if __name__ == "__main__":
    bot = LlmChatBot()
    user_id = "1"
    while True:
        user_input = input("User: ")
        print(f"Bot: {bot.get_response(user_id=user_id, user_input=user_input)} ")
