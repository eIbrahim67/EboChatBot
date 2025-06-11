import logging
from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields
from functools import wraps
from marshmallow import ValidationError

from chatbot.EboChatBotV1.domain.schemas import ChatInputSchema
from chatbot.EboChatBotV1.domain.chat import get_session_id, get_conversation_chain
from chatbot.EboChatBotV1.infrastructure.vector_store.chroma_store import chroma_vectorstore
from chatbot.EboChatBotV1.config import AppConfig

config = AppConfig()

# Initialize Marshmallow schema for input validation
chat_input_schema = ChatInputSchema()

# Create a Flask Blueprint and initialize Flask-RESTX API
api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint, version="1.0", title="Chat API", description="A conversational chat API")
ns = api.namespace('api', description='Chat operations')


# Decorator for API key protection
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if not api_key or api_key != config.SECRET_API_KEY:
            return jsonify({"error": "Unauthorized access"}), 401
        return f(*args, **kwargs)

    return decorated_function


# Swagger models for documentation
chat_model = ns.model('Chat', {
    'session_id': fields.String(required=False, description='Session identifier'),
    'input': fields.String(required=True, description='User input text')
})

response_model = ns.model('ChatResponse', {
    'session_id': fields.String(description='Session identifier'),
    'response': fields.String(description='Assistant response text')
})


def sanitize_input(user_input: any) -> str:
    """Ensure the user input is a non-empty string."""
    if not isinstance(user_input, str):
        user_input = str(user_input)
    return user_input.strip()


@ns.route('/chat')
class ChatResource(Resource):
    @ns.expect(chat_model)
    @ns.marshal_with(response_model)
    def post(self):
        """Chat with the assistant."""
        try:
            json_data = request.get_json(force=True)
            data = chat_input_schema.load(json_data)
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            return {"error": err.messages}, 400
        except Exception as e:
            logging.exception("Invalid JSON:")
            return {"error": f"Invalid JSON input, {e}"}, 400

        session_id = get_session_id(data)
        user_input = sanitize_input(data.get('input', ''))
        if not user_input:
            return {"error": "Input text is required"}, 400

        conversation_chain = get_conversation_chain(session_id)
        try:
            response_text = conversation_chain.predict(input=user_input)
        except Exception as e:
            logging.exception("Error during conversation chain prediction:")
            return {"error": f"Error processing your request, {e}"}, 500

        # Save conversation history with metadata
        metadata = {"session_id": session_id}
        texts_to_add = [
            {"text": f"User: {user_input}", "metadata": metadata},
            {"text": f"Assistant: {response_text}", "metadata": metadata}
        ]
        try:
            chroma_vectorstore.add_texts(
                [doc["text"] for doc in texts_to_add],
                metadatas=[doc["metadata"] for doc in texts_to_add]
            )
        except Exception as e:
            logging.exception(f"Error adding texts to Chroma: {e}")

        return {"session_id": session_id, "response": response_text}, 200


@ns.route('/data')
class DataResource(Resource):
    @require_api_key
    def get(self):
        """Retrieve all data from the vector store."""
        try:
            # chroma_vectorstore._client
            collection = chroma_vectorstore.client.get_collection(config.CHROMA_COLLECTION_NAME)
            data = collection.get()
            return data, 200
        except Exception as e:
            logging.exception(f"Error retrieving data: {e}")
            return {"error": "Unable to retrieve data"}, 500


@ns.route('/drop')
class DropDataResource(Resource):
    @require_api_key
    def post(self):
        """Delete all data from the vector store (protected endpoint)."""
        try:
            result = chroma_vectorstore.collection.delete(where={"session_id": {"$ne": ""}})
            return {"status": "success", "result": result}, 200
        except Exception as e:
            logging.exception("Error dropping data:")
            return {"status": "error", "message": str(e)}, 500
