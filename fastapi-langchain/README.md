# FastAPI LangChain Example

A minimal FastAPI server example demonstrating LangChain ChatOpenAI integration with Spyglass tracing.

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set:
   - `SPYGLASS_API_KEY`: Your Spyglass API key
   - `SPYGLASS_DEPLOYMENT_ID`: Your deployment ID
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `OPENAI_MODEL`: (Optional) Model to use, defaults to "gpt-3.5-turbo"

3. **Run the server:**
   ```bash
   uv run fastapi-langchain.py
   ```
   
   Or use uvicorn directly:
   ```bash
   uv run uvicorn fastapi-langchain:app --reload
   ```

4. **Test the endpoint:**
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello, how are you?"}'
   ```

## What This Example Demonstrates

- FastAPI server setup with a single chat endpoint
- Pydantic Settings for configuration management
- LangChain ChatOpenAI integration
- Function tracing with `@spyglass_trace()` decorator
- Async LLM calls

## API Endpoints

- `GET /`: Health check endpoint
- `POST /chat`: Chat with the LLM
  - Request body: `{"message": "your message here"}`
  - Response: `{"response": "LLM response"}`

## Files

- `fastapi-langchain.py`: Main FastAPI application
- `.env.example`: Environment variables template

