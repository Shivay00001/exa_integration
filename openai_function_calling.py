import json
import os
from openai import OpenAI
from exa_py import Exa
from dotenv import load_dotenv

load_dotenv()

# Setup API Keys
openai_api_key = os.environ.get("OPENAI_API_KEY")
exa_api_key = os.environ.get("EXA_API_KEY")

if not openai_api_key or not exa_api_key:
    print("Please set OPENAI_API_KEY and EXA_API_KEY environment variables to run this script.")
    # We continue just to show the structure, but execution will fail without keys
    if not openai_api_key: openai_api_key = "placeholder"
    if not exa_api_key: exa_api_key = "placeholder"

openai = OpenAI(api_key=openai_api_key)
exa = Exa(api_key=exa_api_key)

tools = [{
    "type": "function",
    "function": {
        "name": "exa_search",
        "description": "Search the web for current information.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Search query"}},
            "required": ["query"]
        }
    }
}]

def exa_search(query: str) -> str:
    print(f"Executing search for: {query}")
    results = exa.search(query=query, type="auto", num_results=10, contents={"text": {"max_characters": 20000}})
    return "\n".join([f"{r.title}: {r.url}" for r in results.results])

messages = [{"role": "user", "content": "What's the latest in AI safety?"}]

try:
    print("Sending request to OpenAI...")
    response = openai.chat.completions.create(model="gpt-4o", messages=messages, tools=tools)

    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        if tool_call.function.name == "exa_search":
            search_query = json.loads(tool_call.function.arguments)["query"]
            search_results = exa_search(search_query)
            
            messages.append(response.choices[0].message)
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": search_results})
            
            print("Received search results, generating final answer...")
            final = openai.chat.completions.create(model="gpt-4o", messages=messages)
            print("\nFinal Answer:")
            print(final.choices[0].message.content)
    else:
        print("Model did not call the search tool.")
        print(response.choices[0].message.content)

except Exception as e:
    print(f"\nError occurred: {e}")
