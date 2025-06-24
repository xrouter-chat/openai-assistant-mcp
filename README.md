# OpenAI Assistant MCP Server

MCP server for OpenAI Assistant API. Provides tools for managing assistants, threads, messages, and runs.

## Deployment

This section outlines the primary methods to deploy and run the OpenAI Assistant MCP server.

### Docker Deployment (Recommended)

Docker is the primary and recommended method for deploying the MCP server, offering consistent environments and easy scaling. It supports both single-user and multi-user configurations.

#### Single-User Docker Deployment
```bash
# Start the container with a static OpenAI API key
docker run --rm -p 8662:8662 \
  -e OPENAI_API_KEY=your_api_key_here \
  ghcr.io/olegische/openai-assistant-mcp:latest
```

#### Multi-User Docker Deployment (with Credential Passthrough)

For multi-user scenarios where different API keys are required per request, enable credential passthrough. The API key will then be provided via the `X-OpenAI-API-Key` header in each request.

```bash
# Start the container with credential passthrough enabled
docker run --rm -p 8662:8662 \
  -e MCP_CREDENTIALS_PASSTHROUGH=true \
  ghcr.io/olegische/openai-assistant-mcp:latest
```

### Other Deployment Options

For development or specific scenarios, you can also run the server directly.

#### Direct Python Execution
```bash
uv run python src/server.py
```

#### MCP Dev Mode (for development)
```bash
uv run mcp dev src/server.py
```

## Configuration

This section details how to configure the MCP server for various operational modes.

### Local Mode (Default)
Set your OpenAI API key in the `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

### Passthrough Mode (Multi-User)
Enable credential passthrough to allow different API keys per request:

Create a `.env` file:
```
MCP_CREDENTIALS_PASSTHROUGH=true
```

For testing with MCPO or other clients that pass headers, export the API key as environment variable:
```bash
export HTTP_HEADER_X_OPENAI_API_KEY="your_api_key_here"
```

In passthrough mode, the OpenAI API key is provided via the `X-OpenAI-API-Key` header in each request.

### Transport Configuration

The server supports multiple transport mechanisms via the `TRANSPORT` environment variable:

```bash
# stdio (default) - for CLI tools
export TRANSPORT=stdio

# Streamable HTTP - modern streamable HTTP transport (recommended for web, Cursor, Claude Desktop)
export TRANSPORT=streamable-http

# SSE - Server-Sent Events (legacy, for backward compatibility)
export TRANSPORT=sse
```

Or in your `.env` file:
```
TRANSPORT=streamable-http
HOST=0.0.0.0
PORT=8001
```

## IDE Integration

> [!NOTE]
> As of now, Claude Desktop does **not** support custom headers in URLs and does **not** support multi-user MCP configurations directly. For multi-user scenarios or custom header requirements, consider using MCPO Proxy for integration.

This section details how to integrate the running OpenAI Assistant MCP server with your IDEs and other AI frontends for seamless interaction.

### Direct Integration (e.g., Claude Desktop, Cursor)

When configuring the MCP server in clients like Claude Desktop or Cursor, the key variable is the transport mechanism through which the client will communicate with the server. MCP servers support at least two transports:
*   `stdio` — standard input/output, where the server process runs directly in the client's stream.
*   `streamable-http` — a standard HTTP server to which the client sends requests.

The configuration difference lies in the command used to start the server and the transport it listens on.

#### Config for `stdio` (Recommended for Docker, if image supports it)

```json
{
  "mcpServers": {
    "openai-assistant-mcp-stdio": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "OPENAI_API_KEY=your_api_key_here",
        "-e", "TRANSPORT=stdio",
        "ghcr.io/olegische/openai-assistant-mcp:latest"
      ]
    }
  }
}
```
Here:
*   `-i` is mandatory because `stdio` only works with a live interactive stdin.
*   `-e TRANSPORT=stdio` tells the MCP server to use the `stdio` transport.

#### Config for `streamable-http`

```json
{
  "mcpServers": {
    "openai-assistant-mcp-http": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-p", "127.0.0.1:8001:8001",  // Map port
        "-e", "OPENAI_API_KEY=your_api_key_here",
        "-e", "TRANSPORT=streamable-http",
        "-e", "HOST=0.0.0.0",
        "-e", "PORT=8001",
        "ghcr.io/olegische/openai-assistant-mcp:latest"
      ],
      "url": "http://localhost:8001/mcp"
    }
  }
}
```
Here:
*   In Docker, we map the port `-p 127.0.0.1:8001:8001`.
*   In the launch arguments, we pass environment variables `-e TRANSPORT=streamable-http`, `-e HOST=0.0.0.0`, and `-e PORT=8001`.
*   In the config, `"url": "http://localhost:8001/mcp"` is mandatory so the client knows where to send HTTP requests.

#### Important Considerations:
*   `stdio` does not require a `url` in the config. The process and client communicate directly via stdin/stdout.
*   `streamable-http` absolutely requires a `url`, otherwise the client will not know where to send HTTP requests.
*   Not all MCP servers equally support `stdio` and `streamable-http`. If the official image does not have a transport switch, you might need a custom build or check the default transport.

#### Quick Choice:
*   If the server is lightweight and does not require a separate port — use `stdio`.
*   If the server is needed as a separate HTTP service — use `streamable-http`.

### Integration via MCPO Proxy (e.g., OpenWebUI, Multi-User Clients)

MCPO (MCP Proxy) is useful for integrating with frontends like OpenWebUI or for multi-user scenarios where credentials need to be passed dynamically via headers.

**Step 1: Ensure MCP server is running with credential passthrough enabled**
(Refer to "Multi-User Docker Deployment" in the Deployment section)

**Step 2: Set up environment variables for MCPO headers (if needed)**
```bash
export HTTP_HEADER_X_OPENAI_API_KEY="your_openai_api_key_here"
```

**Step 3: Run MCPO proxy**
Use the fixed Docker image to avoid schema bugs. This command exposes the MCP server via MCPO at `http://localhost:8602`.
```bash
docker run -p 8602:8000 ghcr.io/olegische/mcpo-fixed-schema:0.0.15 \
    --server-type "sse" \
    --header "{\"X-OpenAI-API-Key\": \"$HTTP_HEADER_X_OPENAI_API_KEY\"}" \
    -- http://host.docker.internal:8662/sse
```
After starting, access the FastAPI UI at: http://localhost:8602/docs

Configure your IDE/client to connect to `http://localhost:8602/sse` (or `/mcp` if using streamable-http transport for the underlying server).

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
