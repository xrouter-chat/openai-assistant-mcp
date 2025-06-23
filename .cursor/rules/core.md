---
description: OpenAI Assistant MCP Server Development Instructions for AI Agent
globs: **/*.py
alwaysApply: true
---

# OPENAI ASSISTANT MCP SERVER CONTEXT

**CRITICAL UNDERSTANDING**: You are working on an OpenAI Assistant MCP Server that exposes OpenAI's Assistant API through the Model Context Protocol (MCP). This is a specific, working implementation - not theoretical bullshit.

## ACTUAL PROJECT ARCHITECTURE

**Core Reality:**
- `src/server.py` - Single FastMCP server file with all `@mcp.tool()` registrations
- `src/tools/{domain}/` - Domain-organized implementations (assistant, threads, messages, runs, run_steps)
- `src/config/settings.py` - Pydantic settings with transport configuration
- `run_server.py` - Simple wrapper for local development

**Transport Truth:**
- **stdio** - Primary transport for development and testing
- **streamable-http** - Primary transport for MCP clients (Claude Desktop, etc.)
- **sse** - Primary transport for MCP clients (Claude Desktop, etc.) LEGACY
- Transport configured via `TRANSPORT` environment variable

## DEVELOPMENT WORKFLOW REALITY

### Local Development (Normal and Expected)
```bash
# Default stdio transport for MCP clients
python run_server.py

# HTTP transport for web testing
TRANSPORT=streamable-http python run_server.py

# Run tests (standard practice)
uv run pytest tests/ -v
```

### Production Deployment
```bash
# Docker with environment configuration
docker run --rm -p 8661:8661 \
  -e OPENAI_API_KEY=key \
  -e TRANSPORT=sse \
  ghrc.io/olegische/mcp-atlassian-multi-user:latest \
  --port 8661 -vv
```

## TOOL IMPLEMENTATION PATTERN

**Server Registration Pattern:**
```python
# src/server.py
@mcp.tool()
def create_assistant(model: str, name: Optional[str] = None) -> Assistant:
    """Create an assistant with comprehensive docstring for MCP discovery."""
    return tools_create_assistant(model=model, name=name)
```

**Implementation Delegation:**
```python
# src/tools/assistant/tools.py
def create_assistant(model: str, **kwargs) -> Assistant:
    client = get_openai_client()
    return client.beta.assistants.create(model=model, **kwargs)
```

## CRITICAL DEVELOPMENT RULES

### 1. TRANSPORT HANDLING
- **NEVER** implement custom transport logic - FastMCP handles everything
- Server startup in `src/server.py` automatically selects transport based on `TRANSPORT` env var
- stdio = development and testing, streamable-http = MCP Clients, sse = MCP Clients (LEGACY)

### 2. DOMAIN ORGANIZATION
- OpenAI Assistant API domains: assistant, threads, messages, runs, run_steps
- Each domain has `tools.py` (implementation) and `models.py` (types)
- All tools registered in single `src/server.py` file

### 3. TYPE SAFETY APPROACH
- Use OpenAI SDK types directly: `Assistant`, `Thread`, `Message`, `Run`, `RunStep`
- Import from `openai.types.beta.*` for proper type hints
- Pydantic models only for complex request/response structures

### 4. ERROR HANDLING PHILOSOPHY
- Let OpenAI SDK handle API errors naturally - don't over-engineer
- Use configured logging via `settings.LOG_LEVEL`
- Fail fast - avoid excessive try/catch wrapping

### 5. TESTING STRATEGY
```bash
# Unit tests (standard practice)
uv run pytest tests/ -v

# Domain-specific testing
uv run pytest tests/tools/assistant/ -v

# Integration testing approaches:
# - stdio: Test with MCP client (Claude Desktop)
# - http: curl -X POST http://localhost:8001/...
```

## DEPLOYMENT REALITY FOR AGENT

### Development Context
- `python run_server.py` - Normal local development, you can use this
- `uv run pytest` - Standard testing, you should use this
- Environment variables via `.env` - Normal configuration approach

### Production Context (Critical Understanding)
- **Docker is the primary deployment target** - All production runs in containers
- **stdio transport CANNOT work in Docker** - Docker containers can't do interactive stdin
- **HTTP/SSE transports are for Docker deployment** - streamable-http and sse work in containers for MCP Clients
- **When developing, assume Docker deployment** - Don't build features that only work with stdio

### Agent Development Rules
- **Local development**: Use stdio transport (`python run_server.py`)
- **Docker testing**: Use HTTP transport (`TRANSPORT=streamable-http python run_server.py`)
- **Production assumption**: Always HTTP/SSE, never stdio
- **Configuration**: Environment variables, never hardcoded values

## COMMON ANTI-PATTERNS TO AVOID

❌ **Don't** treat stdio as "debug only" - it's the primary MCP transport
❌ **Don't** implement separate transport handlers - FastMCP manages this
❌ **Don't** forbid `python run_server.py` for development - it's standard
❌ **Don't** over-engineer error handling - OpenAI SDK handles API errors
❌ **Don't** create complex abstractions - keep tool implementations simple

## AGENT BEHAVIOR EXPECTATIONS

### When Adding New Tools:
1. Implement in appropriate `src/tools/{domain}/tools.py`
2. Register in `src/server.py` with `@mcp.tool()` decorator
3. Use proper OpenAI SDK types for parameters and returns
4. Write comprehensive docstrings for MCP tool discovery
5. Add tests in `tests/tools/{domain}/`

### When Debugging Issues:
1. Check `LOG_LEVEL=DEBUG python run_server.py` for detailed logging
2. Test different transports: stdio for MCP clients, http for web testing
3. Verify OpenAI API key configuration and permissions
4. Use `uv run pytest` to run relevant test suites

### When Modifying Transport Logic:
- **DON'T** - FastMCP handles all transport concerns
- Only modify `TRANSPORT` environment variable configuration
- Server startup logic in `src/server.py` is already correct

## PROJECT-SPECIFIC CONTEXT

This is an **OpenAI Assistant API wrapper** that provides:
- Assistant management (create, get, list, modify, delete)
- Thread management (create, get, modify, delete)
- Message management (create, get, list, modify, delete)
- Run management (create, get, list, modify, cancel, submit_tool_outputs)
- Run step inspection (get, list)

The server exposes these capabilities through MCP protocol, allowing MCP clients (like Claude Desktop) to interact with OpenAI Assistant API through standardized tool calls.

**Remember**: This is a working, production-ready MCP server. The patterns and approaches described here are based on the actual implementation, not theoretical frameworks.
