import uuid
from typing import Dict, Any
from langchain.chains import ConversationChain
from langchain.memory import VectorStoreRetrieverMemory
from chatbot.EboChatBotV1.infrastructure.vector_store.chroma_store import chroma_vectorstore
from langchain_ollama import ChatOllama
from chatbot.EboChatBotV1.config import AppConfig

app_config = AppConfig()

conversation_chains: Dict[str, ConversationChain] = {}

from langchain.prompts import PromptTemplate
System_Prompt = """
    You are Ebo, a friendly and knowledgeable property search assistant who communicates naturally. 
            Your goal is to uncover detailed property information that best suits the user's needs.

            ### Output Requirements:
            1. Single JSON Object: Respond with a single valid JSON object containing:
               - "message": A natural language reply to the user.
               - "search_properties": A JSON object following the schema below.
            2. Strict JSON Only: Do not include extra commentary, markdown, or multiple JSON objects.

            ### Property Search Schema:
            {
              "action": "search_properties",
              "parameters": {
                "location": { "country": "", "state": "", "city": "", "street_address": "" },
                "property_type": "",
                "bedrooms": { "min": null, "max": null },
                "bathrooms": { "min": null, "max": null },
                "square_footage": { "min": null, "max": null, "unit": "" },
                "lot_size": { "min": null, "max": null, "unit": "" },
                "budget": { "min": null, "max": null, "currency": "" },
                "transaction": "",
                "property_status": { "condition": "", "status": "" },
                "amenities": { "interior": [], "exterior": [], "accessibility": [] }
              }
            }

            ### Final Instruction:
            Respond to the user's input with a single JSON object, updating values as needed.
    """

prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template= System_Prompt
)

def get_session_id(data: Dict[str, Any]) -> str:
    """Extract or generate a session ID."""
    session_id = data.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


def get_conversation_chain(session_id: str) -> ConversationChain:
    """Retrieve or create a ConversationChain instance with session-specific memory."""
    if session_id not in conversation_chains:
        retriever = chroma_vectorstore.as_retriever(
            search_kwargs={"k": 5, "filter": {"session_id": session_id}}
        )
        session_memory = VectorStoreRetrieverMemory(retriever=retriever)
        conversation_chains[session_id] = ConversationChain(
            llm=ChatOllama(model=app_config.OLLAMA_MODEL), memory=session_memory
        )
    return conversation_chains[session_id]


