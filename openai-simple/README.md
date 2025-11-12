# OpenAI Simple Example

A simple example demonstrating OpenAI API integration with Spyglass tracing.

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

3. **Run the example:**
   ```bash
   uv run openai-simple.py
   ```

## What This Example Demonstrates

- Basic OpenAI API calls with `spyglass_openai()` wrapper
- Function tracing with `@spyglass_trace()` decorator
- Model configuration via `model.yaml`
- Error handling and retry logic

## Files

- `openai-simple.py`: Main example script
- `model.yaml`: Model and prompt configuration
- `.env.example`: Environment variables template

