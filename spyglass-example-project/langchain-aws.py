import os
import time
import yaml
import asyncio
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.sessions import create_session, Connection

# Spyglass imports - can now be imported before loading environment variables
from spyglass_ai import (
    spyglass_chatbedrockconverse,
    spyglass_mcp_tools_async,
    spyglass_trace,
)

# Load environment variables from .env file
load_dotenv()

# Note: ChatBedrockConverse supports both synchronous operations (invoke, stream)
# and async operations (ainvoke, astream) through inheritance from BaseChatModel.
# This example demonstrates both patterns with proper Spyglass tracing.


def load_model_config():
    """Load model configuration from model.yaml file."""
    try:
        with open("model.yaml", "r") as file:
            config = yaml.safe_load(file)
            # Adapt model name for Bedrock if needed
            model = config.get("model")
            if model and "gpt" in model.lower():
                # Convert OpenAI model to equivalent Bedrock model
                model = "anthropic.claude-3-sonnet-20240229-v1:0"
                print(f"Adapted model for Bedrock: {model}")
            return model, config.get("prompt")
    except Exception as e:
        print(f"An unexpected error occurred loading config: {e}")
        # Return default Bedrock model
        return (
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "You are a helpful AI assistant.",
        )


@spyglass_trace()
def call_bedrock_chat_api(llm, system_prompt):
    """Call Bedrock chat API with tracing."""
    try:
        print("Attempting to call Bedrock Chat API...")

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content="Tell me a joke with only two sentences."),
        ]

        response = llm.invoke(messages)

        if response.content:
            print("Bedrock Response:", response.content)
        else:
            print("Bedrock Response: No content returned")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


@spyglass_trace()
def call_bedrock_streaming_api(llm, system_prompt):
    """Call Bedrock streaming API with tracing."""
    try:
        print("Attempting to call Bedrock Streaming API...")

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content="Write a very short story about AI helping humans."),
        ]

        print("Bedrock Streaming Response:")
        for chunk in llm.stream(messages):
            if chunk.content:
                print(chunk.content, end="", flush=True)
        print()  # New line after streaming

    except Exception as e:
        print(f"An unexpected error occurred during streaming: {e}")


@spyglass_trace()
async def call_bedrock_async_api(llm, system_prompt):
    """Call Bedrock async API with tracing using ainvoke."""
    try:
        print("Attempting to call Bedrock Async API...")

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(
                content="Explain the benefits of async programming in one sentence."
            ),
        ]

        response = await llm.ainvoke(messages)

        if response.content:
            print("Bedrock Async Response:", response.content)
        else:
            print("Bedrock Async Response: No content returned")

    except Exception as e:
        print(f"An unexpected error occurred during async call: {e}")


@spyglass_trace()
async def call_bedrock_with_mcp_tools(llm, system_prompt):
    """Call Bedrock with MCP tools integration using async methods.

    This function demonstrates full async integration with both MCP tools
    and ChatBedrockConverse async methods (ainvoke).
    """
    try:
        print("Attempting to integrate MCP tools with Bedrock...")

        # Example MCP server connection (adjust for your setup)
        # This is a placeholder - replace with your actual MCP server configuration
        connection = Connection(
            command="python",
            args=["-m", "mcp_simple_math"],  # Example MCP server
        )

        try:
            async with create_session(connection) as session:
                await session.initialize()

                # Load and trace MCP tools
                traced_tools = await spyglass_mcp_tools_async(session=session)

                if traced_tools:
                    print(f"Loaded {len(traced_tools)} MCP tools:")
                    for tool in traced_tools:
                        print(f"  - {tool.name}: {tool.description}")

                    # Bind tools to LLM
                    llm_with_tools = llm.bind_tools(traced_tools)

                    messages = [
                        SystemMessage(content=system_prompt),
                        HumanMessage(
                            content="Help me calculate 15 * 42 using available tools."
                        ),
                    ]

                    # Use async invoke method for proper async integration
                    response = await llm_with_tools.ainvoke(messages)
                    print("Bedrock + MCP Tools Response:", response.content)

                else:
                    print("No MCP tools available from the server")

        except Exception as mcp_error:
            print(
                f"MCP integration error (this is expected if no MCP server is running): {mcp_error}"
            )
            print("To use MCP tools, set up an MCP server first.")

    except Exception as e:
        print(f"An unexpected error occurred with MCP tools: {e}")


def check_environment():
    """Check for required environment variables."""
    required_vars = {
        "SPYGLASS_API_KEY": "Spyglass API key for tracing",
        "SPYGLASS_DEPLOYMENT_ID": "Spyglass deployment ID",
    }

    optional_vars = {
        "AWS_REGION": "AWS region (defaults to us-west-2)",
        "AWS_PROFILE": "AWS profile for credentials",
        "AWS_ACCESS_KEY_ID": "AWS access key",
        "AWS_SECRET_ACCESS_KEY": "AWS secret key",
    }

    missing_required = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_required.append(f"{var} - {description}")

    if missing_required:
        print("Error: Required environment variables not set:")
        for var in missing_required:
            print(f"  - {var}")
        print("Please copy .env.example to .env and set your API keys.")
        return False

    print("Optional AWS configuration:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        status = "✓ Set" if value else "Not set"
        print(f"  - {var}: {status}")

    return True


async def main():
    """Main execution function."""
    if not check_environment():
        return

    # Load configuration from model.yaml
    model, system_prompt = load_model_config()

    print(f"Using Bedrock model: {model}")
    print(f"System prompt: {system_prompt[:100]}...")

    # Create ChatBedrockConverse instance
    try:
        llm = ChatBedrockConverse(
            model=model,
            region_name=os.getenv("AWS_REGION", "us-west-2"),
            temperature=0.7,
            max_tokens=1000,
        )

        # Wrap with Spyglass tracing
        # This wraps both sync (_generate, _stream) and async (_agenerate, _astream) methods
        traced_llm = spyglass_chatbedrockconverse(llm)

        print("Starting Bedrock API call loop (every 5 seconds)...")
        print("Press Ctrl+C to stop")

        call_count = 0
        while True:
            call_count += 1
            print(f"\n--- Call #{call_count} ---")

            # Alternate between different types of calls
            if call_count % 4 == 1:
                call_bedrock_chat_api(traced_llm, system_prompt)
            elif call_count % 4 == 2:
                call_bedrock_streaming_api(traced_llm, system_prompt)
            elif call_count % 4 == 3:
                await call_bedrock_async_api(traced_llm, system_prompt)
            else:
                await call_bedrock_with_mcp_tools(traced_llm, system_prompt)

            print("Waiting 5 seconds before next call...")
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nStopping the loop. Goodbye!")
    except Exception as e:
        print(f"Error initializing Bedrock client: {e}")
        print("Please check your AWS credentials and permissions.")
        print("Make sure you have access to Amazon Bedrock and the specified model.")


if __name__ == "__main__":
    # Check for required environment variables
    asyncio.run(main())
