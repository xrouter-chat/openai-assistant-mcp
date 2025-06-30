# OpenAI Assistant MCP Installation Guide for LLMs

This guide will help you install and configure the OpenAI Assistant MCP server for managing OpenAI Assistants API operations through Claude Desktop, Cursor, and other AI assistants.

## Requirements

- Docker installed on your system
- Valid OpenAI API key with access to Assistants API
- Web browser for testing (optional)

## Installation Methods

### Method 1: Docker with Environment Variables (Single User) - **RECOMMENDED**

**Best for**: Single user, production deployment, isolated environment

**Step 1**: Pull Docker image
```bash
docker pull ghcr.io/olegische/openai-assistant-mcp:latest
```

**Step 2**: Configure Claude Desktop
```json
{
  "mcpServers": {
    "openai-assistant-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "OPENAI_API_KEY",
        "-e", "TRANSPORT=stdio",
        "ghcr.io/olegische/openai-assistant-mcp:latest"
      ],
      "env": {
        "OPENAI_API_KEY": "sk-your-openai-api-key-here"
      }
    }
  }
}
```

---

### Method 2: Docker with Custom Headers (Multi-User)

**Best for**: Multi-user environments, enterprise deployments, dynamic credentials

**Step 1**: Start Docker container with custom headers support
```bash
docker run --rm -p 8662:8662 \
  -e MCP_CREDENTIALS_PASSTHROUGH=true \
  -e TRANSPORT=sse \
  -e HOST=0.0.0.0 \
  -e PORT=8662 \
  ghcr.io/olegische/openai-assistant-mcp:latest
```

**Step 2**: Configure Claude Desktop with HTTP transport
```json
{
  "mcpServers": {
    "openai-assistant-mcp": {
      "url": "http://localhost:8662/sse",
      "headers": {
        "X-OpenAI-API-Key": "sk-your-openai-api-key-here"
      }
    }
  }
}
```

---

### Method 3: MCPO Proxy for OpenWebUI Integration

**Best for**: OpenWebUI integration, REST API access, web-based AI interfaces

MCPO (MCP-to-OpenAPI proxy) converts MCP servers into standard REST APIs, making them compatible with OpenWebUI and other web-based AI platforms.

**Step 1**: Start MCP server with custom headers
```bash
docker run --rm -p 8662:8662 \
  -e MCP_CREDENTIALS_PASSTHROUGH=true \
  -e TRANSPORT=sse \
  -e HOST=0.0.0.0 \
  -e PORT=8662 \
  ghcr.io/olegische/openai-assistant-mcp:latest
```

**Step 2**: Set up environment variables for MCPO
```bash
export HTTP_HEADER_X_OPENAI_API_KEY="sk-your-openai-api-key-here"
```

**Step 3**: Run MCPO proxy to convert MCP to REST API
```bash
docker run -p 8602:8000 ghcr.io/olegische/mcpo-fixed-schema:0.0.15 \
    --server-type "sse" \
    --header "{\"X-OpenAI-API-Key\": \"$HTTP_HEADER_X_OPENAI_API_KEY\"}" \
    -- http://host.docker.internal:8662/sse
```

**Step 4**: Access the FastAPI UI
Open http://localhost:8602/docs to test the REST API endpoints.

---

## Authentication Setup

### OpenAI API Key - **Recommended**

1. Go to https://platform.openai.com/api-keys
2. Click **Create new secret key**, name it (e.g., "MCP Assistant Server")
3. Copy the key immediately and store it securely
4. Ensure your account has access to the Assistants API (currently in beta)

> [!IMPORTANT]
> Your OpenAI API key must have access to the Assistants API. If you don't have access, request it from OpenAI.

---

## IDE Configuration

### Claude Desktop Configuration Files

**For Claude Desktop**, edit the configuration file:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**For Cursor**: Open Settings → MCP → + Add new global MCP server

### Transport Options

#### Option 1: stdio Transport (Recommended for Docker)

```json
{
  "mcpServers": {
    "openai-assistant-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "OPENAI_API_KEY",
        "-e", "TRANSPORT=stdio",
        "ghcr.io/olegische/openai-assistant-mcp:latest"
      ],
      "env": {
        "OPENAI_API_KEY": "sk-your-openai-api-key-here"
      }
    }
  }
}
```

#### Option 2: Streamable HTTP Transport

```json
{
  "mcpServers": {
    "openai-assistant-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-p", "127.0.0.1:8001:8001",
        "-e", "OPENAI_API_KEY",
        "-e", "TRANSPORT=streamable-http",
        "-e", "HOST=0.0.0.0",
        "-e", "PORT=8001",
        "ghcr.io/olegische/openai-assistant-mcp:latest"
      ],
      "env": {
        "OPENAI_API_KEY": "sk-your-openai-api-key-here"
      },
      "url": "http://localhost:8001/mcp"
    }
  }
}
```

#### Option 3: SSE Transport

```json
{
  "mcpServers": {
    "openai-assistant-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-p", "127.0.0.1:8662:8662",
        "-e", "OPENAI_API_KEY",
        "-e", "TRANSPORT=sse",
        "-e", "HOST=0.0.0.0",
        "-e", "PORT=8662",
        "ghcr.io/olegische/openai-assistant-mcp:latest"
      ],
      "env": {
        "OPENAI_API_KEY": "sk-your-openai-api-key-here"
      },
      "url": "http://localhost:8662/sse"
    }
  }
}
```

---

## Configuration Options

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required unless using passthrough mode)
- `MCP_CREDENTIALS_PASSTHROUGH`: Set to "true" to enable multi-user mode with header-based auth
- `TRANSPORT`: Transport mechanism ("stdio", "streamable-http", "sse")
- `HOST`: Host to bind to (default: "localhost")
- `PORT`: Port to listen on (default: 8662)

### Multi-User Configuration

For multi-user scenarios, enable credential passthrough:

```json
{
  "mcpServers": {
    "openai-assistant-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-p", "127.0.0.1:8662:8662",
        "-e", "MCP_CREDENTIALS_PASSTHROUGH=true",
        "-e", "TRANSPORT=sse",
        "-e", "HOST=0.0.0.0",
        "-e", "PORT=8662",
        "ghcr.io/olegische/openai-assistant-mcp:latest"
      ],
      "url": "http://localhost:8662/sse",
      "headers": {
        "X-OpenAI-API-Key": "sk-user-specific-api-key-here"
      }
    }
  }
}
```

---

## Troubleshooting

### Authentication Errors

- **Invalid API Key**: Verify your OpenAI API key is correct and active
- **No Assistants Access**: Ensure your OpenAI account has access to the Assistants API beta
- **Rate Limits**: Check if you've exceeded OpenAI API rate limits

### Connection Issues

- Verify Docker is running and the image is pulled correctly
- Check if the specified ports are available and not blocked by firewall
- Ensure the container starts without errors

### Transport Issues

- **stdio**: Requires `-i` flag in Docker command for interactive mode
- **HTTP transports**: Require port mapping (`-p`) and `url` in configuration
- **Headers not working**: Claude Desktop may not support custom headers; use MCPO proxy instead

### Permission Errors

- Ensure your OpenAI API key has sufficient permissions
- Verify API key has access to Assistants API beta
- Check OpenAI account billing and usage limits

### Debugging Commands

```bash
# Test Docker image
docker run --rm ghcr.io/olegische/openai-assistant-mcp:latest --help

# Check container logs
docker logs <container_id>

# Test with MCP Inspector (development only)
npx @modelcontextprotocol/inspector docker run -i --rm \
  -e OPENAI_API_KEY=sk-your-key \
  ghcr.io/olegische/openai-assistant-mcp:latest

# Check Claude Desktop logs (macOS)
tail -n 20 -f ~/Library/Logs/Claude/mcp*.log

# Check Claude Desktop logs (Windows)
type %APPDATA%\Claude\logs\mcp*.log | more
```

---

## Development and Testing

For development and testing purposes only, you can run directly:

```bash
# Clone the repository
git clone https://github.com/olegische/openai-assistant-mcp.git
cd openai-assistant-mcp

# Install dependencies
uv sync

# Set environment variables
export OPENAI_API_KEY=sk-your-key-here

# Run directly
uv run python src/server.py

# Or with MCP dev mode
uv run mcp dev src/server.py
```

> [!WARNING]
> Direct execution is intended for development and testing only. For production use, always use Docker deployment methods described above.

---

## Security Notes

- Never share your OpenAI API keys
- Keep .env files secure and private
- Store credentials securely and never commit to version control
- Use environment files with proper permissions (600)
- Regularly review and rotate API keys
- Monitor API usage in OpenAI dashboard
- Use multi-user mode with individual API keys for team environments

---

## Usage Examples

After installation, you can perform various operations with OpenAI Assistants:

### Example Usage

Ask your AI assistant to:

- **🤖 Assistant Management** - "Create a coding assistant specialized in Python"
- **💬 Conversation Threads** - "Start a new conversation thread about machine learning"
- **📝 Message Handling** - "Add a message to thread asking about best practices"
- **🏃 Run Execution** - "Run the assistant to get responses and handle tool calls"

### Assistant Operations

```
"Create a new assistant with GPT-4 model for code review"
"List all my assistants"
"Update assistant instructions to focus on security"
"Delete the old assistant that's no longer needed"
```

### Thread Operations

```
"Create a new conversation thread"
"Get thread details for thread-123"
"Update thread metadata with project tags"
"Delete the completed thread"
```

### Message Operations

```
"Add a user message to the thread asking about Python best practices"
"List all messages in the current thread"
"Get the specific message content"
"Update message metadata"
```

### Run Operations

```
"Start a run with the coding assistant on the current thread"
"Create a new thread and run the assistant in one call"
"Check the status of the current run"
"Submit tool outputs for function calls"
"Cancel the long-running assistant execution"
```

### Cross-Service Operations

```
"Create an assistant, start a thread, add a message, and run it all together"
"Handle tool calls from the assistant and submit the results"
"Stream the assistant responses in real-time"
"Manage multiple concurrent conversations"
```

---

## Available Tools

### Assistant Management
- `create_assistant` - Create a new assistant with specific model and instructions
- `get_assistant` - Retrieve assistant details by ID
- `list_assistants` - List all assistants with pagination
- `modify_assistant` - Update assistant configuration and instructions
- `delete_assistant` - Delete an assistant permanently

### Thread Management
- `create_thread` - Create a new conversation thread
- `get_thread` - Retrieve thread details by ID
- `modify_thread` - Update thread metadata
- `delete_thread` - Delete a thread and all its messages

### Message Management
- `create_message` - Add a new message to a thread
- `get_message` - Retrieve specific message by ID
- `list_messages` - List all messages in a thread with pagination
- `modify_message` - Update message metadata
- `delete_message` - Delete a specific message

### Run Management
- `create_run` - Start assistant execution on a thread
- `create_thread_and_run` - Create thread and run assistant in one call
- `list_runs` - List all runs for a thread
- `get_run` - Retrieve run details and status
- `modify_run` - Update run metadata
- `submit_tool_outputs` - Submit results for tool calls
- `cancel_run` - Cancel an active run

### Run Steps
- `list_run_steps` - List all steps in a run execution
- `get_run_step` - Retrieve details of a specific run step

---

## Support

For more detailed information and troubleshooting:

- Check the [GitHub repository](https://github.com/olegische/openai-assistant-mcp)
- Review the [OpenAI Assistants API documentation](https://platform.openai.com/docs/assistants/overview)
- File issues for bugs or feature requests
- Check OpenAI API status page for service issues
