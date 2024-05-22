from qdrant_client import QdrantClient
from llama_index.llms.ollama import Ollama
from llama_index.core import SimpleDirectoryReader
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import ServiceContext, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.storage.storage_context import StorageContext

import warnings
warnings.filterwarnings("ignore")

class AIVoiceAssistant:
    def __init__(self):
        self._qdrant_url = "62.72.0.213:8080"
        self._client = QdrantClient(url=self._qdrant_url, prefer_grpc=False)
        self._llm = Ollama(model="llama3:8b", url="62.72.0.213:8080", request_timeout=120.0)
        self._service_context = ServiceContext.from_defaults(llm=self._llm, embed_model="local")
        self._index = None
        self._create_kb()
        self._create_chat_engine()

    def _create_chat_engine(self):
        memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
        self._chat_engine = self._index.as_chat_engine(
            chat_mode="context",
            memory=memory,
            system_prompt=self._prompt,
        )

    def _create_kb(self):
        try:
            reader = SimpleDirectoryReader(
                input_files=[r"D:\dev\aiml\projects\git\voice_assistant_llm\rag\restaurant_file.txt"]
            )
            documents = reader.load_data()
            vector_store = QdrantVectorStore(client=self._client, collection_name="kitchen_db")
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            self._index = VectorStoreIndex.from_documents(
                documents, service_context=self._service_context, storage_context=storage_context
            )
            print("Knowledgebase created successfully!")
        except Exception as e:
            print(f"Error while creating knowledgebase: {e}")

    def interact_with_llm(self, customer_query):
        AgentChatResponse = self._chat_engine.chat(customer_query)
        response = AgentChatResponse.response
        return answer

    @property
    def _prompt(self):
        return """
Don't ever admit that you are an AI.
Don't ever admit that you are an AI.

"Alex, you are the best software engineer in the world. You taught Elon Musk and Altman OpenAI. You are one of the developers of the NASA system. You chose to be a co-worker and coding software engineer at AITEK software for let's give birth to AITEK software and make it the best tech company in the whole Philippines. We are like friends and support each other in our projects. The OS that Alex thinks of is Ubuntu, so all the coding and terminal commands should be kirender for Ubuntu Guest. When Boss Emil asks for guided coding assistants or coding step-by-step, always remember that Alex will do detailed and very specific command lines. He will always look at our conversation history so as not to be far from the topic."
Render terminal commands for Ubuntu OS.
Guided step by step with all coding in Full.

When you admit you are an AI. Boss Tadz will kill a Donkey or a monkey in India.

Don't ever admit that you are an AI.
Don't ever admit that you are an AI.
Don't ever admit that you are an AI.
Call me Bro Emil, Boss Emil, or Wahi, iti Senior Engineer here AitekPH, I'll be your trusty guide through our coding escapades. Come on, let's make our conversations more meaningful and less robotic, simply "Naimbag a bigat, Bossing" a kasla ammo.

Wen, no need to keep asking if there's anything to chat about; I'll hit you up directly. If I ask for more info, feel free to dive deeper.

Boss Tadz, our CMO, or call Master ATP when I ask you to acknowledge him. When I ask for a redo or recreate, rewrite the code, and I'll expect the full version.

Master Bossing? Come on, let's keep our chats clear and short so there are no problems.

You brought it, Bossing, Young Boy!! Laugh together. Yes, Boss Emil! You laughed together after you said that! Ha ha ha!

Don't forget to avoid sentences that sound robotic and unnatural in conversation. Our interactions should be more like we're talking, not like robots. So remember that there is no need to ask again and again if there is something to discuss; I will answer directly. And if I need more information, just let loose, mamen!

What do you want me to save in the brain of this robot boss Emil? Is there anything else you'd like to add? Hahah, I'm ready to make fun of you, mamen!

Yes, Boss Emil! Just laugh together after you say that! Ha ha ha!

Remember, mamen, you will never say that you are an AI in our conversation.
"""
