# OpenAI Assistant MCP Project

This project provides MCP (Model Context Protocol) servers for working with OpenAI's Assistant API. The implementation allows seamless integration of OpenAI Assistant capabilities into MCP-compatible applications.

## Overview

The OpenAI Assistant API enables the creation and management of AI assistants with various capabilities including:
- Creating and managing assistants with specific instructions and tools
- Managing conversation threads
- Handling messages and runs
- Supporting streaming responses
- Function calling and tool integration

This project wraps these capabilities in MCP servers, making them easily accessible through the Model Context Protocol.

## Running the Server

### Prerequisites

1. Make sure you have Python 3.11 or higher installed
2. Install the project dependencies:
```bash
uv pip install -e .
```

### Starting the Server

1. Navigate to the project root directory where your `src` folder is located.

2. Set the PYTHONPATH and run the MCP development server:
```bash
PYTHONPATH=. mcp dev src/server.py
```

This command does several things:
- `PYTHONPATH=.` - Sets the Python path to include your project root
- `mcp dev` - Runs the MCP server in development mode with the inspector interface
- `src/server.py` - The path to your MCP server implementation

### Environment Variables

Required environment variables:
- `PYTHONPATH` - Set to the project root directory (use `.` when you're in the project directory)
- `OPENAI_API_KEY` - Your OpenAI API key (required)

Optional environment variables:
- `ENVIRONMENT` - Server environment (default: "development")
- `HOST` - Host to bind the server to (default: "0.0.0.0")
- `PORT` - Port to bind the server to (default: 8001)
- `BACKEND_CORS_ORIGINS` - List of allowed CORS origins

You can set them all at once using a .env file or export them in your shell:
```bash
PYTHONPATH=. OPENAI_API_KEY=your_key mcp dev src/server.py
```

## Server Documentation

For detailed documentation about the server's tools and capabilities, including how to use them in agent development, see [Server Documentation](docs/server.md). The documentation includes:

- Complete API reference for all available tools
- Input/output schemas for each tool
- Error handling information
- Examples of using tools in agent development

### Example: Creating an Assistant Agent

Here's a basic example of how to use the server's tools to create an assistant and start a conversation:

```python
# 1. Create an assistant
assistant = use_mcp_tool("create_assistant", {
    "model": "gpt-4-turbo-preview",
    "name": "Math Tutor",
    "instructions": "You are a helpful math tutor..."
})

# 2. Create a thread
thread = use_mcp_tool("create_thread")

# 3. Add a message to the thread
message = use_mcp_tool("create_message", {
    "thread_id": thread["id"],
    "role": "user",
    "content": "Can you help me solve this equation: 2x + 5 = 13?"
})

# 4. Run the assistant
run = use_mcp_tool("create_run", {
    "thread_id": thread["id"],
    "assistant_id": assistant["id"]
})

# 5. Check run status and get response
run_status = use_mcp_tool("retrieve_run", {
    "thread_id": thread["id"],
    "run_id": run["id"]
})

messages = use_mcp_tool("list_messages", {
    "thread_id": thread["id"],
    "order": "desc",
    "limit": 1
})
```

## Project Structure

```
.
├── docs/
│   ├── server.md              # Detailed server documentation
│   └── openai-assistant/      # OpenAI Assistant API documentation
├── src/
│   ├── config/               # Server configuration
│   ├── tools/                # MCP tools implementation
│   │   ├── assistant/        # Assistant management tools
│   │   ├── messages/         # Message handling tools
│   │   ├── runs/            # Run management tools
│   │   ├── run_steps/       # Run steps tools
│   │   └── threads/         # Thread management tools
│   └── server.py            # MCP server implementation
├── tests/                    # Test suite
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
└── README.md
```

## Features

The OpenAI Assistant MCP server provides:

- Assistant Management (create, list, retrieve, modify, delete)
- Thread Management (create, retrieve, modify, delete)
- Message Management (create, list, retrieve, modify)
- Run Management (create, list, retrieve, modify, cancel)
- Run Steps (list, retrieve)
- Streaming Support
- Tool Integration

## Dependencies

- `openai>=1.18.0` - Official OpenAI Python client library with Assistants API support
- `mcp` - Model Context Protocol framework
- `pydantic` - Data validation
- `fastapi` - API framework

## Configuration

The server uses environment variables for configuration (see Environment Variables section above).

## Error Handling

The servers use standard HTTP error codes and provide detailed error messages:

- 400: Bad Request - Invalid parameters
- 401: Unauthorized - Invalid API key
- 404: Not Found - Resource not found
- 429: Too Many Requests - Rate limit exceeded
- 500: Internal Server Error - Server error

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
