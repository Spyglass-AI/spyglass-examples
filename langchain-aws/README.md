# LangChain AWS Bedrock Example

An example demonstrating LangChain AWS Bedrock integration with Spyglass tracing and MCP (Model Context Protocol) tools.

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
   - AWS credentials (see `.env.example` for options)

3. **Run the example:**
   ```bash
   uv run langchain-aws.py
   ```

## What This Example Demonstrates

- LangChain AWS Bedrock integration with `spyglass_chatbedrockconverse()`
- MCP tools integration with `spyglass_mcp_tools_async()`
- Async LLM calls with tool usage
- OpenTelemetry GenAI semantic conventions

## Prerequisites

- Node.js (for MCP server)
- AWS credentials with Bedrock access
- An MCP server (optional, example uses a test server)

## Files

- `langchain-aws.py`: Main example script
- `.env.example`: Environment variables template

