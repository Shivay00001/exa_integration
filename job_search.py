import os
from exa_py import Exa
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# Setup API Key
api_key = os.environ.get("EXA_API_KEY")
if not api_key:
    print("Error: EXA_API_KEY not found in environment variables.")
    exit(1)

exa = Exa(api_key=api_key)

def find_jobs(role: str, location: str = "Remote"):
    print(f"Searching for '{role}' jobs in '{location}'...")
    
    # Calculate date for "past week" filter (approximate via prompt or Exa filters if available)
    # Exa's search is semantic, so we can ask for "recent" in the query
    
    query = f"Hiring {role} in {location} posted recently"
    
    try:
        results = exa.search(
            query=query,
            type="auto", # 'auto' is good for general queries
            category="tweet", # searching tweets can sometimes find fresh job threads, but let's stick to general web for now
            # Better to use no category for general job boards
            num_results=15,
            start_published_date=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"), # Last 7 days
        )

        output_text = f"Found {len(results.results)} potential job listings from the last 7 days:\n\n"
        
        for i, result in enumerate(results.results, 1):
            output_text += f"{i}. {result.title}\n"
            output_text += f"   URL: {result.url}\n"
            output_text += f"   Published: {result.published_date}\n"
            output_text += "-" * 40 + "\n"
            
        print(output_text)
        with open("results.txt", "w", encoding="utf-8") as f:
            f.write(output_text)
        print("Results saved to results.txt")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # You can change these variables
    TARGET_ROLE = "Python Developer"
    TARGET_LOCATION = "Remote"
    
    find_jobs(TARGET_ROLE, TARGET_LOCATION)
