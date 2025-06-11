from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_TEMPERATURE: float = 0.7
    CHROMA_COLLECTION_NAME: str = "chat_history"
    CHROMA_PERSIST_DIR: str = "chroma_db"
    SECRET_API_KEY: str = "your-secret-key"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"