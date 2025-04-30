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

### Accessing the Server

Once running, you can access:
- MCP Inspector UI: http://localhost:8080
- MCP Server API: http://localhost:8001 (configurable via PORT)

### Development Tips

1. Use the MCP Inspector to:
   - View available tools and resources
   - Test API calls
   - Debug responses

2. Monitor the terminal output for:
   - Server logs
   - Error messages
   - Request/response information

3. Hot reload:
   - The server will automatically reload when you make changes to the code
   - Keep the terminal output visible to catch any errors during reload

### Troubleshooting

If you encounter import errors:
1. Verify you're in the project root directory (where the `src` folder is)
2. Ensure PYTHONPATH is set correctly (should be `.` when in project root)
3. Check that all dependencies are installed with `uv pip install -e .`
4. Verify Python version (3.11+ required)

If you encounter API errors:
1. Verify your OPENAI_API_KEY is set correctly
2. Check the API rate limits in your OpenAI dashboard
3. Monitor the server logs for detailed error messages

## Project Structure

```
.
├── docs/
│   ├── mcp-servers/           # MCP server documentation
│   │   └── openai-assistant/  # OpenAI Assistant MCP server docs
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
