# Exa API Integration Examples

This directory contains examples for using the Exa API for web search and function calling.

## Setup

1. **Install Dependencies**
   It is recommended to use a virtual environment.

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   You need to set your API keys. You can do this in your terminal or by creating a `.env` file (not included in repo for security).
   - `EXA_API_KEY`: Your Exa API key.
   - `OPENAI_API_KEY`: (Optional) For OpenAI function calling example.
   - `ANTHROPIC_API_KEY`: (Optional) For Anthropic tool use example.

   **Windows PowerShell:**

   ```powershell
   $env:EXA_API_KEY="your_key_here"
   ```

## Files

- **`quick_start.py`**: A simple script to demonstrate a basic search using `exa-py`.
- **`openai_function_calling.py`**: Demonstrates how to use Exa as a tool with OpenAI's GPT models.
- **`anthropic_function_calling.py`**: Demonstrates how to use Exa as a tool with Anthropic's Claude models.
- **`mcp_server_config.json`**: Contains configuration snippets for setting up the Exa MCP server in Claude Desktop or Cursor.

## Usage

To run the basic search:

```bash
python quick_start.py
```

To run the function calling examples (ensure respective API keys are set):

```bash
python openai_function_calling.py
To run the job search example:
```bash
python job_search.py
```

To run the **Job Application Agent**:

1. Place your CV as `my_cv.pdf` in the `exa_integration` folder (I've already copied your test resume there).
2. Ensure you have `OPENAI_API_KEY` in your `.env` for AI generation (otherwise it uses a placeholder).
3. Run:

```bash
python application_agent.py
```

This will create a `my_applications` folder with subfolders for each job containing a generated cover letter and apply link.
