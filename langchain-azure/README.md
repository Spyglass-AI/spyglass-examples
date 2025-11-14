# LangChain Azure OpenAI Example

A simple example demonstrating LangChain AzureChatOpenAI integration with Spyglass tracing.

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up environment variables:**
   
   Create a `.env` file or set the following environment variables:
   
   **Required:**
   - `SPYGLASS_API_KEY`: Your Spyglass API key
   - `SPYGLASS_DEPLOYMENT_ID`: Your Spyglass deployment ID
   - `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
   - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL (e.g., `https://your-resource.openai.azure.com/`)

   **Optional:**
   - `AZURE_OPENAI_DEPLOYMENT_NAME`: Azure deployment name (defaults to `gpt-4`)
   - `OPENAI_API_VERSION`: Azure OpenAI API version (defaults to `2024-05-01-preview`)
   - `AZURE_OPENAI_MODEL`: Model name for tracing (defaults to `gpt-4`)

3. **Run the example:**
   ```bash
   uv run langchain-azure.py
   ```

## What This Example Demonstrates

- LangChain AzureChatOpenAI integration
- Spyglass tracing with `spyglass_azure_chatopenai()` wrapper
- Function tracing with `@spyglass_trace()` decorator
- Sync LLM calls using `invoke()`
- Usage metadata extraction
- Environment variable configuration

## Example Output

```
Required configuration:
  - SPYGLASS_API_KEY: abc12345...
  - SPYGLASS_DEPLOYMENT_ID: dep-123
  - AZURE_OPENAI_API_KEY: xyz67890...
  - AZURE_OPENAI_ENDPOINT: https://example.openai.azure.com/

Optional configuration:
  - AZURE_OPENAI_DEPLOYMENT_NAME: ✓ gpt-4
  - OPENAI_API_VERSION: ✓ 2024-05-01-preview
  - AZURE_OPENAI_MODEL: ✓ gpt-4

Using Azure deployment: gpt-4
Model name: gpt-4
API version: 2024-05-01-preview

Calling Azure OpenAI with message: 'Tell me a short joke about programming.'
Azure OpenAI Response: Why do programmers prefer dark mode? Because light attracts bugs!
Token usage: 25 input, 15 output, 40 total
```

## Files

- `langchain-azure.py`: Main example script
- `pyproject.toml`: Project dependencies and configuration

