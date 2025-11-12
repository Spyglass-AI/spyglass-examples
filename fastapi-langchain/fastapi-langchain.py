from fastapi import FastAPI
from fastapi.responses import JSONResponse
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field
from spyglass_ai import spyglass_trace, configure_spyglass, spyglass_chatopenai


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Spyglass configuration
    spyglass_api_key: str = Field(..., validation_alias="SPYGLASS_API_KEY")
    spyglass_deployment_id: str = Field(..., validation_alias="SPYGLASS_DEPLOYMENT_ID")

    # OpenAI configuration
    openai_api_key: str = Field(..., validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-nano", validation_alias="OPENAI_MODEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


# Load settings
settings = Settings()

# Configure Spyglass SDK programmatically
configure_spyglass(
    api_key=settings.spyglass_api_key,
    deployment_id=settings.spyglass_deployment_id,
    endpoint="http://localhost:4318/v1/traces" # TODO: Only for local testing, do not commit
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


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(..., description="The user message to send to the LLM")


@app.get("/")
@spyglass_trace()
async def root():
    return {
        "message": "FastAPI LangChain Example - Use POST /chat to chat with the LLM"
    }

@app.post("/chat")
@spyglass_trace()
async def chat(request: ChatRequest):
    """Chat endpoint that uses LangChain ChatOpenAI to generate a response."""
    try:
        # Call LangChain ChatOpenAI
        response = await llm.ainvoke([HumanMessage(content=request.message)])

        return {"response": response.content}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8088)
