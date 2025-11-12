# Spyglass Examples

This repository contains example projects demonstrating how to integrate with the Spyglass AI Platform for AI observability and monitoring.

Each example is a self-contained project with its own dependencies, making it easy to run with `uv`.

## Available Examples

### 1. OpenAI Simple (`openai-simple/`)

A simple example demonstrating OpenAI API integration with Spyglass tracing.

**Features:**
- Basic OpenAI API calls with `spyglass_openai()` wrapper
- Function tracing with `@spyglass_trace()` decorator
- Model configuration via `model.yaml`
- Error handling and retry logic

**Quick Start:**
```bash
cd openai-simple
uv sync
cp .env.example .env
# Edit .env with your API keys
uv run openai-simple.py
```

### 2. LangChain AWS Bedrock (`langchain-aws/`)

An advanced example demonstrating LangChain AWS Bedrock integration with Spyglass tracing and MCP (Model Context Protocol) tools.

**Features:**
- LangChain AWS Bedrock integration with `spyglass_chatbedrockconverse()`
- MCP tools integration with `spyglass_mcp_tools_async()`
- Async LLM calls with tool usage
- OpenTelemetry GenAI semantic conventions

**Quick Start:**
```bash
cd langchain-aws
uv sync
cp .env.example .env
# Edit .env with your API keys and AWS credentials
uv run langchain-aws.py
```

### 3. FastAPI LangChain (`fastapi-langchain/`)

A minimal FastAPI server example demonstrating LangChain ChatOpenAI integration with Spyglass tracing.

**Features:**
- FastAPI server with REST API endpoint
- LangChain ChatOpenAI integration
- Function tracing with `@spyglass_trace()` decorator
- Async LLM calls

**Quick Start:**
```bash
cd fastapi-langchain
uv sync
cp .env.example .env
# Edit .env with your API keys
uv run fastapi-langchain.py
# Or: uv run uvicorn fastapi-langchain:app --reload
```

## Prerequisites

1. **uv**: Install from [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Spyglass API Key**: Get one by logging into [spyglass-ai.com](https://spyglass-ai.com), navigating to the Account section in the sidebar, and generating one from the API Keys tab.

3. **Example-specific prerequisites**: See each example's README for additional requirements (e.g., AWS credentials, Node.js for MCP tools).

## Project Structure

```
spyglass-examples/
├── README.md                    # This file
├── use-local-sdk.py            # Helper script for local SDK development
├── openai-simple/              # Simple OpenAI example
│   ├── openai-simple.py
│   ├── model.yaml
│   ├── pyproject.toml
│   ├── README.md
│   └── .env.example
├── langchain-aws/              # LangChain AWS Bedrock example
│   ├── langchain-aws.py
│   ├── pyproject.toml
│   ├── README.md
│   └── .env.example
└── fastapi-langchain/          # FastAPI LangChain example
    ├── fastapi-langchain.py
    ├── pyproject.toml
    ├── README.md
    └── .env.example
```

## Running Examples with uv

Each example is a standalone `uv` project. To run any example:

1. **Navigate to the example directory:**
   ```bash
   cd <example-name>
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Run the example:**
   ```bash
   uv run <script-name>.py
   ```

## What Gets Traced

All examples demonstrate tracing for:
- **Function calls** using `@spyglass_trace()` decorator
- **LLM API calls** using Spyglass wrappers
- **Model usage, token consumption, and response times**
- **Tool usage** (in examples that support it)

View your analytics in the Spyglass AI dashboard after running any example.

## Local Development with spyglass-sdk

If you're developing the `spyglass-sdk` locally and want to test it with these examples, you can conditionally use the local SDK instead of the published version.

### Quick Setup

Use the provided helper script to toggle local SDK usage. The script automatically runs `uv sync` in each updated example directory:

```bash
# Enable local SDK for all examples (automatically runs uv sync)
uv run use-local-sdk.py enable

# Disable local SDK (use published version, automatically runs uv sync)
uv run use-local-sdk.py disable

# Check current status
uv run use-local-sdk.py status
```

### Manual Setup

Alternatively, you can manually edit each example's `pyproject.toml` file. Look for the commented section at the bottom:

```toml
# Uncomment the section below to use the local spyglass-sdk for development
# This assumes spyglass-sdk is located at ../../spyglass-sdk relative to this file
# [tool.uv.sources]
# spyglass-ai = { path = "../../spyglass-sdk", editable = true }
```

Uncomment the `[tool.uv.sources]` section to use the local SDK, or comment it out to use the published version.

**Note:** 
- This assumes `spyglass-sdk` is located at `../../spyglass-sdk` relative to each example directory. Adjust the path if your directory structure differs.
- After manually editing `pyproject.toml`, run `uv sync` in each example directory to apply the changes.

## Adding New Examples

To add a new example:

1. Create a new directory: `mkdir <example-name>`
2. Create a `pyproject.toml` with the example's dependencies
3. Add your example script(s)
4. Create a `README.md` with setup instructions
5. Create a `.env.example` file with required environment variables
6. Update this README to include your new example

## GitHub Actions Integration

Some examples may include GitHub Actions workflows for deployment tracking. These workflows track model and prompt changes over time, helping identify performance issues in production deployments.

To use GitHub Actions:
1. Create a new GitHub repository and push the example code
2. Set the `SPYGLASS_API_KEY` secret in your repository settings
3. Push code to trigger the workflow

## Support

If you run into any issues, feel free to contact us: team@spyglass-ai.com
