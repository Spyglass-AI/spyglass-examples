import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from spyglass_ai import (
    spyglass_azure_chatopenai,
    spyglass_trace,
    configure_spyglass,
)

# Load environment variables from .env file
load_dotenv()


def check_environment():
    """Check for required environment variables."""
    required_vars = {
        "SPYGLASS_API_KEY": "Spyglass API key for tracing",
        "SPYGLASS_DEPLOYMENT_ID": "Spyglass deployment ID",
        "AZURE_OPENAI_API_KEY": "Azure OpenAI API key",
        "AZURE_OPENAI_ENDPOINT": "Azure OpenAI endpoint URL",
    }

    optional_vars = {
        "AZURE_OPENAI_DEPLOYMENT_NAME": "Azure deployment name (defaults to 'gpt-4')",
        "OPENAI_API_VERSION": "Azure OpenAI API version (defaults to '2024-05-01-preview')",
        "AZURE_OPENAI_MODEL": "Model name for tracing (defaults to 'gpt-4')",
    }

    missing_required = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_required.append(f"{var} - {description}")

    if missing_required:
        print("Error: Required environment variables not set:")
        for var in missing_required:
            print(f"  - {var}")
        print("Please set these environment variables before running.")
        return False

    print("Required configuration:")
    for var in required_vars.keys():
        value = os.getenv(var)
        # Mask sensitive values
        if "KEY" in var:
            masked_value = value[:8] + "..." if value else "Not set"
            print(f"  - {var}: {masked_value}")
        else:
            print(f"  - {var}: {value}")

    print("\nOptional configuration:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        status = f"✓ {value}" if value else "Not set (using default)"
        print(f"  - {var}: {status}")

    return True


@spyglass_trace()
def call_azure_openai(llm, system_prompt, user_message):
    """Call Azure OpenAI with LangChain using sync methods.

    This function demonstrates sync integration with AzureChatOpenAI
    and Spyglass tracing.
    """
    try:
        print(f"\nCalling Azure OpenAI with message: '{user_message}'")
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]

        # Use sync invoke method
        response = llm.invoke(messages)
        
        print(f"Azure OpenAI Response: {response.content}")
        
        # Display usage metadata if available
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            usage = response.usage_metadata
            print(f"Token usage: {usage.get('input_tokens', 0)} input, "
                  f"{usage.get('output_tokens', 0)} output, "
                  f"{usage.get('total_tokens', 0)} total")
        
        return response
    except Exception as e:
        print(f"Error calling Azure OpenAI: {e}")
        raise


def main():
    """Main execution function."""
    if not check_environment():
        return

    # Configure Spyglass
    configure_spyglass(
        api_key=os.getenv("SPYGLASS_API_KEY"),
        deployment_id=os.getenv("SPYGLASS_DEPLOYMENT_ID"),
    )

    # Get configuration from environment
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    api_version = os.getenv("OPENAI_API_VERSION", "2024-05-01-preview")
    model_name = os.getenv("AZURE_OPENAI_MODEL", "gpt-4")
    
    system_prompt = "You are a helpful AI assistant."
    user_message = "Tell me a short joke about programming."

    # Create AzureChatOpenAI instance
    try:
        llm = AzureChatOpenAI(
            azure_deployment=deployment_name,
            model=model_name,
            api_version=api_version,
            temperature=0.7,
            max_tokens=500,
        )

        # Wrap with Spyglass tracing
        traced_llm = spyglass_azure_chatopenai(llm)

        print(f"\nUsing Azure deployment: {deployment_name}")
        print(f"Model name: {model_name}")
        print(f"API version: {api_version}")

        # Make the call
        call_azure_openai(traced_llm, system_prompt, user_message)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
