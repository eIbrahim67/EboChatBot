# EboChatBotV1

EboChatBotV1 is a Flask-based conversational AI application designed as a property search assistant. It leverages the Ollama language model and Chroma vector store for session-based conversational memory, enabling natural and context-aware interactions. The application is built with modularity, security, and scalability in mind, using modern Python practices and libraries like Pydantic, LangChain, and Flask-Talisman.

## Table of Contents
1. [Features](#features)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running the Application](#running-the-application)
7. [Usage](#usage)
8. [File Structure](#file-structure)
9. [Dependencies](#dependencies)
10. [Logging](#logging)
11. [Security](#security)
12. [Contributing](#contributing)
13. [License](#license)

## Features
- **Conversational AI**: Powered by the Ollama language model (default: `llama3.2`) for natural language processing.
- **Session-Based Memory**: Utilizes Chroma vector store with a custom local embedding model to maintain conversation context per session.
- **Property Search Assistant**: Structured JSON responses tailored for property search queries, following a predefined schema.
- **Secure Flask Application**: Enforces HTTPS and adds security headers using Flask-Talisman.
- **Configurable Settings**: Managed via Pydantic's `BaseSettings` with `.env` file support for environment-specific configurations.
- **Input Validation**: Uses Marshmallow schemas to validate incoming API requests.
- **Logging**: Comprehensive logging setup for debugging and monitoring.

## Architecture
The application follows a modular architecture, separating concerns across configuration, infrastructure, and presentation layers:

- **Configuration**: Managed by `config.py` using Pydantic for type-safe environment variable handling.
- **Infrastructure**: Includes the Chroma vector store (`chroma_store.py`) for conversation memory and a custom embedding model (`local_nomic_embedder.py`).
- **Conversational Logic**: Handled by `chat.py`, which manages session-based conversation chains using LangChain.
- **LLM Integration**: `ollama_llm.py` provides a custom interface to the Ollama language model.
- **API Layer**: `app.py` sets up the Flask application with security headers and routes defined in `presentation/api_routes.py`.
- **Input Validation**: `schemas.py` defines Marshmallow schemas for validating API inputs.
- **Logging**: Configured in `logging_config.py` for consistent logging across the application.

## Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Virtualenv (recommended for isolated environments)
- Ollama server (for running the language model locally or remotely)
- Access to a terminal or command-line interface

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/EboChatBotV1.git
   cd EboChatBotV1
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Ollama**:
   - Install and run the Ollama server locally or ensure access to a remote Ollama instance.
   - Pull the desired model (default: `llama3.2`):
     ```bash
     ollama pull llama3.2
     ```

5. **Create a `.env` File**:
   Copy the example environment file and customize it:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to set configuration values (e.g., `SECRET_API_KEY`, `OLLAMA_MODEL`, etc.).

## Configuration
The application uses a `.env` file to manage configuration settings. Below are the available configuration options defined in `config.py`:

| Variable                  | Description                                      | Default Value         |
|---------------------------|--------------------------------------------------|-----------------------|
| `OLLAMA_MODEL`            | Name of the Ollama model to use                 | `llama3.2`            |
| `OLLAMA_TEMPERATURE`      | Sampling temperature for the model               | `0.7`                 |
| `CHROMA_COLLECTION_NAME`  | Name of the Chroma collection for memory         | `chat_history`        |
| `CHROMA_PERSIST_DIR`      | Directory for persisting Chroma data             | `chroma_db`           |
| `SECRET_API_KEY`          | API key for authentication (replace with secure key) | `your-secret-key` |
| `ENVIRONMENT`             | Application environment (`development`, `production`) | `development`    |

Example `.env` file:
```env
OLLAMA_MODEL=llama3.2
OLLAMA_TEMPERATURE=0.7
CHROMA_COLLECTION_NAME=chat_history
CHROMA_PERSIST_DIR=chroma_db
SECRET_API_KEY=your-secure-api-key
ENVIRONMENT=development
```

## Running the Application
1. **Ensure the Ollama Server is Running**:
   Start the Ollama server if it’s running locally:
   ```bash
   ollama serve
   ```

2. **Run the Flask Application**:
   ```bash
   python app.py
   ```
   The application will start on `http://0.0.0.0:5000` in development mode. In production, configure a WSGI server (e.g., Gunicorn) and a reverse proxy (e.g., Nginx).

3. **Access the API**:
   Use tools like `curl`, Postman, or a browser to interact with the API endpoints (e.g., `/chat` for conversational queries).

## Usage
The application exposes a REST API for interacting with the Ebo property search assistant. The primary endpoint is `/chat`, which accepts JSON payloads containing user input and an optional session ID.

### Example Request
```bash
curl -X POST http://localhost:5000/chat \
-H "Content-Type: application/json" \
-d '{
  "input": "I’m looking for a 3-bedroom house in Austin, TX under $500,000",
  "session_id": "123e4567-e89b-12d3-a456-426614174000"
}'
```

### Example Response
```json
{
  "message": "I found some great options for a 3-bedroom house in Austin, TX within your budget. Here are the search parameters I’ve set for you.",
  "search_properties": {
    "action": "search_properties",
    "parameters": {
      "location": { "country": "USA", "state": "TX", "city": "Austin", "street_address": "" },
      "property_type": "house",
      "bedrooms": { "min": 3, "max": 3 },
      "bathrooms": { "min": null, "max": null },
      "square_footage": { "min": null, "max": null, "unit": "" },
      "lot_size": { "min": null, "max": null, "unit": "" },
      "budget": { "min": null, "max": 500000, "currency": "USD" },
      "transaction": "",
      "property_status": { "condition": "", "status": "" },
      "amenities": { "interior": [], "exterior": [], "accessibility": [] }
    }
  }
}
```

### Session Management
- If no `session_id` is provided, a new UUID is generated.
- The session ID is used to maintain conversation context via the Chroma vector store.

## File Structure
```
EboChatBotV1/
├── chatbot/
│   ├── EboChatBotV1/
│   │   ├── config.py                  # Configuration management with Pydantic
│   │   ├── infrastructure/
│   │   │   ├── embeddings/
│   │   │   │   └── local_nomic_embedder.py  # Custom embedding model
│   │   │   └── vector_store/
│   │   │       └── chroma_store.py    # Chroma vector store setup
│   │   └── presentation/
│   │       ├── api_routes.py          # Flask API routes
│   │       └── error_handlers.py      # Custom error handling
├── app.py                            # Flask application entry point
├── chat.py                           # Conversation logic and session management
├── logging_config.py                 # Logging setup
├── ollama_llm.py                     # Ollama LLM integration
├── schemas.py                        # Input validation schemas
├── requirements.txt                  # Python dependencies
├── .env.example                      # Example environment file
└── README.md                         # Project documentation
```

## Dependencies
The application relies on the following key Python packages (listed in `requirements.txt`):
- `flask`: Web framework for the API.
- `flask-talisman`: Security headers and HTTPS enforcement.
- `pydantic-settings`: Type-safe configuration management.
- `langchain`: Framework for conversational AI and memory.
- `langchain-chroma`: Chroma vector store integration.
- `langchain-ollama`: Ollama model integration.
- `marshmallow`: Schema validation for API inputs.
- `ollama`: Python client for the Ollama API.
- `uuid`: For generating session IDs.

Install dependencies using:
```bash
pip install flask flask-talisman pydantic-settings langchain langchain-chroma langchain-ollama marshmallow ollama
```

## Logging
Logging is configured in `logging_config.py` with the following format:
```
%(asctime)s [%(levelname)s] %(name)s: %(message)s
```
Logs are output at the `INFO` level by default. Errors from the Ollama model or other components are logged for debugging purposes.

## Security
- **HTTPS Enforcement**: Flask-Talisman ensures all requests are served over HTTPS in production.
- **API Key**: A `SECRET_API_KEY` is required for authentication (configured in `.env`).
- **Input Validation**: Marshmallow schemas prevent invalid or malicious inputs.
- **Session Isolation**: Conversation memory is scoped to individual sessions using UUIDs.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code adheres to PEP 8 and includes appropriate tests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.