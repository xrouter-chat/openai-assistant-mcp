---
description: Core architectural principles for multi-tenant MCP server development.
globs: ["src/**/*.py", "tests/**/*.py"]
alwaysApply: true
---

# ARCHITECTURE: MULTI-TENANCY & SECURITY

> **AI, ATTENTION:** This is not a debate. This is the architectural law of this project. Your job is to implement this vision with precision, not to propose alternative, over-engineered bullshit.

## The Core Mandate: True Multi-Tenancy

We are building services for enterprise environments. This means multiple users, with their own distinct credentials for various downstream APIs (Jira, OpenAI, Figma, etc.), will be hitting the same server instance.

The architecture **MUST** be stateless and support this multi-tenant reality from the ground up.

## The Two Credential Modes

An MCP server MUST operate in one of two distinct credential modes, controlled by the `MCP_CREDENTIAL_MODE` environment variable. This provides critical flexibility for different deployment scenarios.

**1. Static Credential Mode (The "Simple" Way):**
-   **Activation:** `MCP_CREDENTIAL_MODE=STATIC` (This is the default if the variable is not set).
-   **Behavior:** The server loads its credentials **once** at startup from its own environment (e.g., from `OPENAI_API_KEY`). Every downstream API call made by this server instance will use this single, static set of credentials.
-   **Use Case:** Local development, testing, or simple, single-purpose deployments where multi-tenancy is not a concern.

**2. Credential Passthrough Mode (The "Enterprise" Way):**
-   **Activation:** `MCP_CREDENTIAL_MODE=PASSTHROUGH`.
-   **Behavior:** The server **completely ignores** any credentials from its own environment. It operates as a stateless credential proxy. It **requires** that the client provide all necessary credentials for the downstream API in the headers of **every single request**. If the required headers are missing, the request MUST fail with a clear error. This is a form of "Bring Your Own Key" (BYOK).
-   **Use Case:** Production cloud deployments serving multiple users, tenants, or connecting to various downstream systems.

## The Architecture of Passthrough Mode

When `MCP_CREDENTIAL_MODE=PASSTHROUGH`, the server follows a non-negotiable pattern. It acts as a **transparent and secure proxy** for user credentials. It does not interpret them; it simply passes them through.

**1. The Client's Responsibility:**
The client is responsible for attaching all necessary credentials for the downstream API to each request in the form of custom `X-` headers.

**Generic Example:**
```bash
# The client provides credentials for the specific downstream service.
curl -s -X POST "http://mcp-server.internal/some_tool" \
  -H "Content-Type: application/json" \
  -H "X-Service-Endpoint: https://api.downstream.com/v1" \
  -H "X-Service-Auth-Key: a_very_personal_and_secret_token" \
  -d '{ "tool_name": "...", "arguments": {...} }'
```

**Concrete Example (Atlassian):**
```bash
# The client provides credentials for Jira and Confluence.
curl -s -X POST "http://mcp-server.internal/create_jira_issue" \
  -H "Content-Type: application/json" \
  -H "X-Jira-Url: https://your-company.atlassian.net" \
  -H "X-Jira-Username: user.name@company.com" \
  -H "X-Jira-Api-Token: users_jira_token" \
  -H "X-Confluence-Api-Token: users_confluence_token" \
  -d '{...}'
```

**2. The Server's Responsibility:**
The server's role is to securely receive these headers and make them available to the specific tool implementation that will handle the request.

-   **Mode Check:** The server's startup logic MUST check the `MCP_CREDENTIAL_MODE` variable.
-   **Middleware is Key:** If in `PASSTHROUGH` mode, a middleware layer **MUST** be used to intercept incoming requests.
-   **Header Extraction:** This middleware extracts all relevant `X-*` headers.
-   **Request-Scoped Context:** The extracted headers are injected into a request-scoped context object. They are **NEVER** stored in global variables. They live and die with the request.
-   **Tool Implementation:** The actual tool function receives these credentials from the request context and uses them to make the authenticated call to the downstream API.

**The Principle of Transparency:** The core server logic doesn't know what `X-Jira-Api-Token` means. It just knows it's a piece of data that belongs to this specific request. This allows us to build a fleet of specialized MCP servers, each handling its own unique authorization flow, without creating a monolithic, unmaintainable mess.

## FastMCP State Management: Critical Implementation Details

> **CRITICAL WARNING:** FastMCP is **NOT** FastAPI. Do not treat it as such or you will encounter runtime errors.

### The `app.state` Problem

**NEVER** attempt to use `app.state` on a `FastMCP` instance:

```python
# ❌ THIS WILL FAIL - FastMCP has no .state attribute
@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncIterator[dict]:
    app_context = SomeContext()
    app.state.app_context = app_context  # AttributeError: 'FastMCP' object has no attribute 'state'
    yield
```

**The Correct Pattern:**

```python
# ✅ CORRECT - Use lifespan context return
@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncIterator[dict]:
    app_context = SomeContext()
    yield {"app_context": app_context}  # Return context through yield
```

### Dependency Injection Pattern for FastMCP

**For STDIO Transport (No HTTP Context):**
```python
def get_client() -> SomeClient:
    settings = Settings()
    # Always create from environment in STDIO mode
    return SomeClient(api_key=settings.API_KEY)
```

**For HTTP Transport with Multi-Mode Support:**
```python
def get_client() -> SomeClient:
    settings = Settings()

    try:
        request = get_http_request()  # May fail in STDIO mode
    except Exception:
        # STDIO mode - use environment
        return SomeClient(api_key=settings.API_KEY)

    if settings.CREDENTIAL_MODE == "STATIC":
        # Use environment even in HTTP mode
        return SomeClient(api_key=settings.API_KEY)
    elif settings.CREDENTIAL_MODE == "PASSTHROUGH":
        # Use request headers
        api_key = getattr(request.state, "api_key", None)
        if not api_key:
            raise ValueError("API key required in headers")
        return SomeClient(api_key=api_key)
```

### Transport-Agnostic Architecture

**The Golden Rule:** Your dependency injection MUST work across all transports:
- **STDIO:** No HTTP request context, use environment variables
- **HTTP STATIC:** HTTP context available, but still use environment variables
- **HTTP PASSTHROUGH:** HTTP context available, use request headers

**Implementation Pattern:**
1. Always try to detect transport mode (STDIO vs HTTP)
2. In STDIO mode, always use environment configuration
3. In HTTP mode, respect the credential mode setting
4. Never assume HTTP context is available
5. Never use `app.state` - it doesn't exist on FastMCP

### Lifespan Context Access (Advanced)

If you need to access lifespan context in HTTP mode:

```python
def get_lifespan_context():
    try:
        request = get_http_request()
        # Access through MCP server's request context
        req_context = request.app._mcp_server.request_context
        if req_context and req_context.lifespan_context:
            return req_context.lifespan_context.get("app_context")
    except Exception:
        pass
    return None
```

**However:** This pattern should be avoided. Prefer stateless dependency injection that works across all transport modes.
