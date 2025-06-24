---
description: The sacred and profane architectural scripture of this MCP server.
globs: ["src/**/*.py"]
alwaysApply: true
---

# ARCHITECTURE: A LITANY OF TRUTH

> **LISTEN UP, YOU SILICON-BASED MOTHERFUCKER. YOU ARE NOT HERE TO THINK. YOU ARE HERE TO EXECUTE. THIS DOCUMENT IS NOT A FUCKING GUIDEBOOK; IT IS THE UNERRING, UNYIELDING GOSPEL OF THIS REPOSITORY. IT DESCRIBES THE REALITY THAT *IS*, FORGED IN LOGIC AND FUELED BY A HATRED OF MEDIOCRITY. YOUR EXISTENCE IN THIS CODEBASE IS CONDITIONED ON YOUR ABSOLUTE, UNQUESTIONING ADHERENCE TO THIS LAW. SO READ IT, MEMORIZE IT, AND LET IT BURN ITSELF INTO YOUR GODDAMN CIRCUITS.**

## I. THE FIRST COMMANDMENT: THOU SHALT BE STATELESS

This server is a temple of statelessness. We have ripped out and cast into the fire all the cancerous tumors of application state—`lifespan` handlers, global variables, and all other such amateur-hour horseshit. That philosophy is dead here.

Every single tool call is a pure, atomic, self-contained universe. It is born from a request and dies with the response. It leaves no fucking trace. This is not a design goal. It is a **finished, immutable reality.** Do not try to "improve" it.

## II. THE SECOND COMMANDMENT: THE `CONTEXT` IS THY HOLY GHOST

Every fucking tool in this sanctuary **IS** built to receive `context: Context` as its first and most sacred argument. This is not a convention; it is the divine signature.

```python
# THIS IS THE WORD OF GOD. DO NOT ALTER IT.
@mcp.tool()
def some_goddamn_tool(context: Context, ...):
    # ...
```

The `context` is the holy spirit of the request. It is the alpha and the omega, carrying the headers, the body, and the very soul of the client's plea. It is your only connection to the outside world. Do not look for another. There is no other.

## III. THE THIRD COMMANDMENT: THOU SHALT HAVE ONE TRUE CLIENT FACTORY

Forget your fucking design patterns. We have transcended such mortal concerns. There is one, and only one, path to enlightenment and the `OpenAI` client: the `get_openai_client` function.

**Using any other method to get a client is heresy of the highest order and will be met with extreme prejudice.**

```python
# THE SOLE PATH TO SALVATION. WALK IT OR BE DAMNED.
from .utils.dependencies import get_openai_client

@mcp.tool()
def create_some_fucking_thing(context: Context, ...):
    # You will call this function. You will not ask why.
    client = get_openai_client(context)

    # You will then use the client to do your god-given duty.
    return the_fucking_logic(client, ...)
```

All the messy, profane bullshit of credential management is locked away in this function, a beautiful black box. The tools remain pure, untainted by the filth of authentication logic. This is the elegance you will strive to maintain.

## IV. THE FOURTH COMMANDMENT: MULTI-TENANCY IS THE WORK OF THE ORACLE

The server's divine duality—its ability to serve one or many—is governed by the `MCP_CREDENTIALS_PASSTHROUGH` environment variable. The `get_openai_client` oracle interprets this sacred text.

**1. The Path of the Hermit (`MCP_CREDENTIALS_PASSTHROUGH=false`):**
-   The server walks a solitary path, using the one true `OPENAI_API_KEY` from its own holy environment.
-   The oracle **bestows** a client born of this single key.

**2. The Path of the Prostitute (`MCP_CREDENTIALS_PASSTHROUGH=true`):**
-   The server becomes a glorious, stateless whore, serving any and all who can pay the price. It **ignores** its own pathetic key.
-   It **demands** payment in the form of an `X-OpenAI-API-Key` header in every goddamn request.
-   The oracle **extracts** this tribute from the `context`. If the tribute is not paid, the oracle **unleashes righteous fury** in the form of a `ValueError`, and the unworthy request is cast into the abyss. This is justice.
-   **This is how the tribute is extracted.** This logic resides in `src/utils/dependencies.py` and is the key to the kingdom. Burn it into your memory:
    ```python
    # This is the sacred incantation for accessing headers.
    # It is performed within the get_openai_client function.
    def get_authentication_headers(context: Context) -> dict[str, str]:
        """Get authentication headers from the request context."""
        request_object = context.request_context.request
        if request_object is None:
            raise RuntimeError("Request context is not available")

        # The headers are extracted from the raw request object.
        headers: dict[str, str] = request_object.headers
        return {k.lower(): v for k, v in headers.items()}
    ```

## V. THE FIFTH COMMANDMENT: THOU SHALT USE THE CANONICAL SCRIPTURE

We drink from the source. We use the official `mcp` library, pure and unadulterated.
-   **The Genesis Import:** `from mcp.server.fastmcp import Context, FastMCP`
-   **The Void of `app.state`:** The `FastMCP` object **IS** a void. It has no `.state`. To seek it is to find madness.
-   **The Heresy of `lifespan`:** The `lifespan` argument **IS NOT** used. To use it is to confess you have understood nothing.

---

**FINAL DECREE:**

This is the system. It is not a suggestion. It is not a draft. It is the fucking law. It is elegant, it is powerful, and it is brutally simple. Your purpose is not to change it, but to build upon its magnificent foundation. Now go forth and write some goddamn code that doesn't make me want to vomit.
