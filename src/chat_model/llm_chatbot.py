import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings
from tools.fetch_data import tools as fetch_api_tools

load_dotenv()

TRAINED_DIR = Path(__file__).resolve().parent / "trained"

class LlmChatBot:
    def __init__(self, model="openai/gpt-3.5-turbo", embedding_model=TRAINED_DIR / "all-MiniLM-L6-v2.F32.gguf"):
        self.VECTOR_WORDS = TRAINED_DIR / "vector_words" / "from_guides"
        
        self.embedding = GPT4AllEmbeddings(
            model_file=embedding_model,
            device='cpu' 
        )
        
        self.vector_words = FAISS.load_local(
            folder_path=self.VECTOR_WORDS,
            embeddings=self.embedding,
            allow_dangerous_deserialization=True
        )

        self.llm = ChatOpenAI(
            openai_api_key=os.getenv("OPENROUTER_API"),
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.3,
            model=model,
            max_retries=3
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="input",
            output_key="output"
        )

        self.agent_executor = self._initialize_agent()

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
            memory=self.memory,
            verbose=True,
            prompt=prompt,
            handle_parsing_errors=True
        )

    def _get_system_prompt(self):
        return """
        You are a smart virtual assistant for an e-commerce website.
        You MUST always consider using tools provided to help you answer accurately. If unsure, try using a tool.
        You can only answer questions based on the following (only use character and number, not symbolize) topics:
        1. Website Information  
        2. How to use the website  
        3. Product Consultation  
        4. Other general inquiries  
        If the user's question is outside these topics, respond with:  
        "Sorry, I can only answer questions related to our website and services. If you need further assistance, please contact us at Phone: +843949505816 or Email: group11@gmail.com."
        Always ensure your answer is clear, detailed, and concise.  
        """

    def _create_retrieval_tool(self):
        retriever = self.vector_words.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 3}
        )
        return create_retriever_tool(
            retriever=retriever,
            name="ecommerce_docs",
            description="Search infomation from internal docs"
        )

    def load_old_conversation_to_memory(self, messages: list):
        self.memory.clear()
        for msg in messages:
            if msg["role"] == "user":
                self.memory.chat_memory.add_user_message(msg["content"])
            elif msg["role"] == "chatbot":
                self.memory.chat_memory.add_ai_message(msg["content"])

    def get_response(self, user_input: str) -> str:
        try:
            response = self.agent_executor.invoke({"input": user_input})
            return response["output"]
        except Exception as e:
            raise 

if __name__ == "__main__":
    bot = LlmChatBot()
    while (True):
        user_input = input("User: ")
        print(f"Bot: {bot.get_response(user_input=user_input)} ")