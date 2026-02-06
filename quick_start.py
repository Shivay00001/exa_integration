import os
from exa_py import Exa
from dotenv import load_dotenv

load_dotenv()

# Setup API Key
api_key = os.environ.get("EXA_API_KEY") or "YOUR_API_KEY"
print(f"Using API Key: {api_key if api_key != 'YOUR_API_KEY' else 'placeholder (please set EXA_API_KEY)'}")

try:
    exa = Exa(api_key=api_key)

    # Perform Search
    print("\nSearching for 'React hooks best practices 2024'...")
    results = exa.search(
        query="React hooks best practices 2024",
        type="auto",
        num_results=10,
        contents={"text":{"max_characters":20000}}
    )

    # Print Results
    print(f"\nFound {len(results.results)} results:")
    for result in results.results:
        print(f"- {result.title}: {result.url}")

except Exception as e:
    print(f"\nError occurred: {e}")
    print("Please check if your API key is correct and set in the environment or the script.")
