from fastapi import FastAPI
from fastapi.responses import JSONResponse
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from pydantic_settings import BaseSettings
from pydantic import Field
from spyglass_ai import spyglass_trace, configure_spyglass, spyglass_chatopenai


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Spyglass configuration
    spyglass_api_key: str = Field(..., env="SPYGLASS_API_KEY")
    spyglass_deployment_id: str = Field(..., env="SPYGLASS_DEPLOYMENT_ID")

    # OpenAI configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-3.5-turbo", env="OPENAI_MODEL")

    class Config:
        env_file = ".env"
        case_sensitive = False


# Load settings
settings = Settings()

# Configure Spyglass SDK programmatically
configure_spyglass(
    api_key=settings.spyglass_api_key,
    deployment_id=settings.spyglass_deployment_id,
)

# Initialize FastAPI app
app = FastAPI(title="Spyglass FastAPI LangChain Example")

# Initialize LangChain ChatOpenAI
llm = ChatOpenAI(
    model=settings.openai_model,
    temperature=0.7,
    api_key=settings.openai_api_key,
)

# Instrument with Spyglass
llm = spyglass_chatopenai(llm)


@app.get("/")
async def root():
    return {
        "message": "FastAPI LangChain Example - Use POST /chat to chat with the LLM"
    }


@app.post("/chat")
@spyglass_trace()
async def chat(message: dict):
    """Chat endpoint that uses LangChain ChatOpenAI to generate a response."""
    try:
        user_message = message.get("message", "")
        if not user_message:
            return JSONResponse(
                status_code=400, content={"error": "Message is required"}
            )

        # Call LangChain ChatOpenAI
        response = await llm.ainvoke([HumanMessage(content=user_message)])

        return {"response": response.content}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
