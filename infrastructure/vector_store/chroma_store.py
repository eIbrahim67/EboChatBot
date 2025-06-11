from langchain_chroma import Chroma
from chatbot.EboChatBotV1.config import AppConfig
from chatbot.EboChatBotV1.infrastructure.embeddings.local_nomic_embedder import LocalNomicEmbedder

config = AppConfig()

local_embedder = LocalNomicEmbedder()

chroma_vectorstore = Chroma(
    embedding_function=local_embedder,
    collection_name=config.CHROMA_COLLECTION_NAME,
    persist_directory=config.CHROMA_PERSIST_DIR
)
