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

## Project Structure

```
.
├── docs/
│   ├── mcp-servers/           # MCP server documentation
│   │   └── openai-assistant/  # OpenAI Assistant MCP server docs
│   └── openai-assistant/      # OpenAI Assistant API documentation
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
└── README.md
```

## MCP Servers

### OpenAI Assistant Server

The OpenAI Assistant MCP server provides a complete interface to the OpenAI Assistant API. It supports:

- Assistant Management (create, list, retrieve, modify, delete)
- Thread Management (create, retrieve, modify, delete)
- Message Management (create, list, retrieve, modify)
- Run Management (create, list, retrieve, modify, cancel)
- Run Steps (list, retrieve)
- Streaming Support
- Tool Integration

For detailed documentation on the OpenAI Assistant MCP server, see [docs/mcp-servers/openai-assistant/README.md](docs/mcp-servers/openai-assistant/README.md).

## Dependencies

- `openai>=1.18.0` - Official OpenAI Python client library with Assistants API support

## Configuration

Each MCP server requires specific configuration. For the OpenAI Assistant server:

```json
{
  "api_key": "your-openai-api-key"
}
```

## Usage

The MCP servers can be used with any MCP-compatible client. The servers provide tools that map directly to OpenAI Assistant API endpoints, making it easy to:

1. Create and manage AI assistants
2. Handle conversations through threads
3. Process messages and manage runs
4. Integrate with various tools (Code Interpreter, File Search, Function Calling)
5. Handle streaming responses

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
