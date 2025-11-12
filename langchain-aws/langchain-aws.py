import os
import asyncio
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.sessions import create_session, StdioConnection
from spyglass_ai import (
    spyglass_chatbedrockconverse,
    spyglass_mcp_tools_async,
    spyglass_trace,
)

# Load environment variables from .env file
load_dotenv()


@spyglass_trace()
async def call_bedrock_with_mcp_tools(llm, system_prompt):
    """Call Bedrock with MCP tools integration using async methods.

    This function demonstrates full async integration with both MCP tools
    and ChatBedrockConverse async methods (ainvoke).
    """
    try:
        print("Attempting to integrate MCP tools with Bedrock...")

        connection = StdioConnection(
            command="uvx",
            transport="stdio",
            args=[
                "--from",
                "git+https://github.com/macsymwang/hello-mcp-server.git",
                "hello-mcp-server",
            ],
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
                            content="Use available tools to say hello to yourself"
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
        import traceback

        print(f"An unexpected error occurred with MCP tools: {e}")
        print("Full traceback:")
        traceback.print_exc()


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

    # Hardcoded model and system prompt
    model = "anthropic.claude-3-sonnet-20240229-v1:0"
    system_prompt = "You are a helpful AI assistant."

    # Create ChatBedrockConverse instance
    try:
        llm = ChatBedrockConverse(
            model=model,
            region_name=os.getenv("AWS_REGION", "us-west-2"),
            temperature=0.7,
            max_tokens=1000,
        )

        # Wrap with Spyglass tracing
        traced_llm = spyglass_chatbedrockconverse(llm)

        while True:
            await call_bedrock_with_mcp_tools(traced_llm, system_prompt)
            await asyncio.sleep(5)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Check for required environment variables
    asyncio.run(main())
