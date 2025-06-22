# OpenAI Assistant MCP Server

MCP server for OpenAI Assistant API. Provides tools for managing assistants, threads, messages, and runs.

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd openai-assistant-mcp

# Install dependencies
uv pip install -e .
```

## Configuration

Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

Or create a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

### Transport Configuration

The server supports multiple transport mechanisms via the `TRANSPORT` environment variable:

```bash
# stdio (default) - for CLI tools and Claude Desktop
export TRANSPORT=stdio

# HTTP - modern streamable HTTP transport (recommended for web)
export TRANSPORT=http
# or
export TRANSPORT=streamable-http

# SSE - Server-Sent Events (legacy, for backward compatibility)
export TRANSPORT=sse
```

Or in your `.env` file:
```
TRANSPORT=stdio
HOST=0.0.0.0
PORT=8001
```

## Running the Server

### Transport-Specific Examples

#### STDIO Transport (Default)
Best for CLI tools and Claude Desktop integration:
```bash
# Set transport to stdio
export TRANSPORT=stdio
uv run python run_server.py
```

#### HTTP Transport (Recommended for Web)
Modern streamable HTTP transport for web services:
```bash
# Set transport to HTTP
export TRANSPORT=http
export HOST=0.0.0.0
export PORT=8001
uv run python run_server.py
```

Server will be available at: `http://localhost:8001`

#### SSE Transport (Legacy)
Server-Sent Events for backward compatibility:
```bash
# Set transport to SSE
export TRANSPORT=sse
export HOST=0.0.0.0
export PORT=8001
uv run python run_server.py
```

### Development Options

#### Option 1: Direct Python execution
```bash
uv run mcp run run_server.py
```

#### Option 2: MCP Dev Mode (for development)
```bash
uv run mcp dev run_server.py
```

#### Option 3: MCPO with FastAPI UI (recommended for HTTP transport)
Due to a bug in the official mcpo release, use the fixed fork:
```bash
uvx --from git+https://github.com/bmen25124/mcpo.git@fix_schema_defs_not_found mcpo --port 8602 -- uv run mcp run run_server.py
```

After starting, access the FastAPI UI at: http://localhost:8602/docs

## Available Tools

### Assistant Management
- `create_assistant` - Create a new assistant
- `get_assistant` - Retrieve assistant by ID
- `list_assistants` - List all assistants
- `modify_assistant` - Update assistant configuration
- `delete_assistant` - Delete an assistant

### Thread Management
- `create_thread` - Create a conversation thread
- `get_thread` - Retrieve thread by ID
- `modify_thread` - Update thread metadata
- `delete_thread` - Delete a thread

### Message Management
- `create_message` - Add message to thread
- `get_message` - Retrieve message by ID
- `list_messages` - List thread messages
- `modify_message` - Update message metadata
- `delete_message` - Delete a message

### Run Management
- `create_run` - Start assistant execution
- `create_thread_and_run` - Create thread and run in one call
- `list_runs` - List thread runs
- `get_run` - Retrieve run by ID
- `modify_run` - Update run metadata
- `submit_tool_outputs` - Submit tool call results
- `cancel_run` - Cancel active run

### Run Steps
- `list_run_steps` - List steps for a run
- `get_run_step` - Retrieve specific step

## Example Usage

```python
# Create an assistant
assistant = await create_assistant({
    "model": "gpt-4-turbo-preview",
    "name": "Code Helper",
    "instructions": "You are a helpful coding assistant."
})

# Create a thread
thread = await create_thread()

# Add a message
message = await create_message({
    "thread_id": thread["id"],
    "role": "user",
    "content": "Help me write a Python function"
})

# Run the assistant
run = await create_run({
    "thread_id": thread["id"],
    "assistant_id": assistant["id"]
})
```

## Project Structure

```
├── src/
│   ├── server.py              # MCP server entry point
│   ├── config/                # Configuration
│   └── tools/                 # Tool implementations
│       ├── assistant/         # Assistant tools
│       ├── threads/           # Thread tools
│       ├── messages/          # Message tools
│       ├── runs/              # Run tools
│       └── run_steps/         # Run step tools
├── tests/                     # Test suite
├── docs/                      # Documentation
└── pyproject.toml            # Project configuration
```

## Troubleshooting

### MCPO Schema Error
If you encounter `TypeError: argument of type 'NoneType' is not iterable`, you're using the broken official mcpo release. Use the fixed fork command shown above.

### API Key Issues
Ensure your OpenAI API key has access to the Assistants API beta.

## License

MIT
