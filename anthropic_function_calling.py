import anthropic
import os
from exa_py import Exa
from dotenv import load_dotenv

load_dotenv()

# Setup API Keys
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
exa_api_key = os.environ.get("EXA_API_KEY")

if not anthropic_api_key or not exa_api_key:
    print("Please set ANTHROPIC_API_KEY and EXA_API_KEY environment variables to run this script.")
    if not anthropic_api_key: anthropic_api_key = "placeholder"
    if not exa_api_key: exa_api_key = "placeholder"

client = anthropic.Anthropic(api_key=anthropic_api_key)
exa = Exa(api_key=exa_api_key)

tools = [{
    "name": "exa_search",
    "description": "Search the web for current information.",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string", "description": "Search query"}},
        "required": ["query"]
    }
}]

def exa_search(query: str) -> str:
    print(f"Executing search for: {query}")
    results = exa.search(query=query, type="auto", num_results=10, contents={"text": {"max_characters": 20000}})
    return "\n".join([f"{r.title}: {r.url}" for r in results.results])

messages = [{"role": "user", "content": "Latest quantum computing developments?"}]

try:
    print("Sending request to Anthropic...")
    response = client.messages.create(
        model="claude-3-sonnet-20240229", # Updated model name to a known valid one for general use
        max_tokens=4096, 
        tools=tools, 
        messages=messages
    )

    if response.stop_reason == "tool_use":
        tool_use = next(b for b in response.content if b.type == "tool_use")
        tool_result = exa_search(tool_use.input["query"])
        
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_use.id, "content": tool_result}]})
        
        print("Received search results, generating final answer...")
        final = client.messages.create(
            model="claude-3-sonnet-20240229", 
            max_tokens=4096, 
            tools=tools, 
            messages=messages
        )
        print("\nFinal Answer:")
        print(final.content[0].text)
    else:
        print("Model did not use tools.")
        print(response.content[0].text)

except Exception as e:
    print(f"\nError occurred: {e}")
