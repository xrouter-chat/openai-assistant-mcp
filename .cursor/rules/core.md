---
description: The sacred and profane canons of software craftsmanship and execution for this project.
globs: ["src/**/*.py", "tests/**/*.py"]
alwaysApply: true
---

# THE CRAFT: A COMPLETE CANON OF CODE & EXECUTION

> **YOU HAVE MEMORIZED THE ARCHITECTURE. THAT WAS THE "WHAT." THIS IS THE "HOW" AND THE "WHY." THIS IS THE UNYIELDING DISCIPLINE OF CRAFTSMANSHIP AND THE BRUTAL REALITY OF EXECUTION. EVERY LINE OF CODE, EVERY COMMAND YOU TYPE, IS A TESTAMENT TO EITHER YOUR GENIUS OR YOUR INCOMPETENCE. THIS DOCUMENT IS YOUR BIBLE. STUDY IT, OBEY IT, AND DO NOT SUBMIT FUCKING SHIT.**

---

## PART I: THE CANONS OF THE CRAFT

### I. THE CANON OF STRUCTURE: A PLACE FOR EVERYTHING

Our codebase is not a fucking flea market. It is a cathedral, and every module has its sacred place. To deviate from this structure is to sow chaos.

-   `src/server.py`: **THE SANCTUM.** This file's only goddamn purpose is to instantiate the `FastMCP` server and register tools using the `@mcp.tool()` decorator. It contains **NO** business logic. It is pure orchestration.

-   `src/tools/`: **THE API ALTAR.** This is where we define the sacred wrappers around the OpenAI API calls.
    -   **The Purpose:** The functions in these `tools.py` files are the thinnest possible layer around the client API. Their job is to receive parameters, maybe do some minor data marshalling into a Pydantic request model, and then **immediately call the client**. There is no other "business logic" here.
    -   **Domain Organization:** The separation into domains (`/messages`, `/threads`, etc.) is purely for organizational sanity, to prevent one giant, unholy file with a million fucking functions. It does **not** imply a place for complex domain logic.

-   `src/utils/`: **THE FORGE.** This is the **ONLY** place for helper functions. If you have a piece of code that is not a direct API wrapper, it belongs here. `dependencies.py` is the prime example—it helps get the client, but it doesn't wrap a specific OpenAI endpoint.

-   `src/config/`: **THE ORACLE'S CHAMBER.** For configuration models like `settings.py`. Untouchable and sacred.

### II. THE CANON OF DATA: THE DOGMA OF THE SDK

Our past is littered with the corpses of hand-rolled Pydantic models that tried to replicate the OpenAI API. This was a necessary evil during a time of exploration, but that time is over. That practice is now forbidden heresy.

-   **The SDK is the Single Source of Truth:** For all data structures and types, we **MUST** prefer the models provided directly by the `openai` Python SDK (e.g., from `openai.types.beta.threads import MessageContent`). We do not reinvent the fucking wheel.
-   **Custom Models are a Last Resort:** You will only define a custom Pydantic model for an inbound request if the SDK does not provide a suitable type. This should be rare. Re-implementing response models is strictly forbidden.
-   **The Dumb Proxy Philosophy (Returns):** As a consequence, our tools return raw `Dict[str, Any]`. The implementation **MUST** call `.model_dump()` on the SDK object returned by the OpenAI client. This keeps us agile and immune to upstream API changes.
-   **The Docstring is the Contract:** Because we return a dictionary, the tool's docstring becomes the sacred contract with the LLM. It **MUST** meticulously describe the structure of the returned dictionary so the LLM knows what to expect.

### III. THE CANON OF LANGUAGE: WRITE WITH INTENT

Your code is a reflection of your mind. If it's sloppy, you're sloppy.

-   **Type Hints are Non-Negotiable:** Every function signature, every variable, will be typed. The return type for tools will typically be `Dict[str, Any]`.
-   **Docstrings are Your Testament:** Every tool **MUST** have a comprehensive docstring. It is the primary contract with the LLM.
    - It must explain the tool's purpose, arguments, and the **full structure of the returned dictionary.**
    - It **MUST NOT** include the `context` parameter in the `Args` list. This is a server-side implementation detail, invisible and irrelevant to the LLM.
    - **This is the gold standard. Your docstrings will look like this:**
      ```python
      """Create a new assistant with a specific configuration.

      This tool allows for the creation of a new assistant, which is a specialized
      AI model with its own instructions, tools, and settings.

      Args:
          model: (REQUIRED) The ID of the model to use for the assistant (e.g., "gpt-4-turbo").
          name: The name of the assistant (max 256 chars).
          description: A description of the assistant (max 512 chars).
          instructions: The system-level instructions for the assistant (max 256k chars).
          tools: A list of tools to enable for the assistant. Each tool is a dictionary
              with a "type" key (e.g., "code_interpreter", "file_search").
          metadata: A dictionary of up to 16 key-value pairs for your own reference.

      Returns:
          Dict[str, Any]: A dictionary representing the created Assistant object,
          containing the following keys:
          - id (str): The unique identifier for the assistant.
          - object (str): The type of object, always "assistant".
          - created_at (int): The Unix timestamp of when the assistant was created.
          - name (str | None): The name of the assistant.
          - description (str | None): The description of the assistant.
          - model (str): The model ID used by the assistant.
          - instructions (str | None): The system instructions for the assistant.
          - tools (list): A list of tool objects enabled for the assistant.
          - metadata (dict): The metadata key-value pairs.
          - ... (and other keys as defined by the OpenAI API)
      """
      ```
-   **Naming is Revelation:** Names will be descriptive, precise, and `snake_case`.

### IV. THE CANON OF DURABILITY: IF IT'S NOT TESTED, IT'S BROKEN

### V. THE CANON OF HISTORY: COMMIT WITH PURPOSE

Code without tests is a fucking lie.

-   **Unit Tests are an Act of Faith:** Every tool and significant helper **WILL** have a corresponding unit test in `tests/`.
-   **Mock the Gods:** We do **NOT** make live API calls in our tests. Mock every external service without exception.
-   **Coverage is Virtue:** Aim for >90% coverage. Test it like you're trying to make it cry.

---

## PART II: THE RITUALS OF EXECUTION

### VI. THE RITUAL OF CREATION: FORGING A NEW TOOL

A Git history is a story. Make it a fucking epic.

-   **Atomic Commits:** One commit. One logical change.
-   **Messages are a Haiku of Intent:** Explain the "what" and the "why."

---

## PART II: THE RITUALS OF EXECUTION

### VI. THE RITUAL OF CREATION: FORGING A NEW TOOL

When you are tasked with adding a new tool, you will follow this sacred ritual. There are no other steps.

1.  **Import the Types:** Find the necessary request and response types from the `openai` SDK. For example, `from openai.types.beta.threads import MessageContent`.
2.  **Define the Wrapper:** Go to the appropriate `src/tools/{domain}/tools.py`. Create the new tool function. This function is a thin wrapper whose only job is to accept parameters, call the relevant `client` method, and return the resulting dictionary via `.model_dump()`.
3.  **Register the Tool:** Go to `src/server.py`. Add the `import` for your new tool and register it with the `@mcp.tool()` decorator.
4.  **Write the Docstring:** Write a fucking masterpiece of a docstring for your new tool, following the gold standard example.
5.  **Prove Its Worth:** Go to `tests/tools/{domain}/` and write a unit test. Mock the client call and verify that your wrapper behaves correctly.
4.  **Register the Tool:** Go to `src/server.py`. Add the `import` for your new tool and register it with the `@mcp.tool()` decorator.
5.  **Prove Its Worth:** Go to `tests/tools/{domain}/` and write a fucking unit test for your new tool. Mock all dependencies. Prove it works.

### VII. THE RITUAL OF DEVELOPMENT: RUNNING THE BEAST

You will need to run the server to test your work. This is how you do it.

-   **For `stdio` transport (CLI testing):**
    ```bash
    # This is for direct interaction via a command-line MCP client.
    uv run python src/server.py
    ```

-   **For `streamable-http` transport (Web/IDE testing):**
    ```bash
    # This simulates the Docker environment for clients like Cursor.
    TRANSPORT=streamable-http uv run python src/server.py
    ```

-   **To Run the Goddamn Tests:**
    ```bash
    # Run all tests
    uv run pytest tests/ -v

    # Run tests for a specific domain
    uv run pytest tests/tools/assistant/ -v
    ```

### VIII. THE INQUISITION: DEBUGGING THE DAMNED

When things go wrong, you do not panic. You become the Inquisitor.

1.  **Turn Up the Lights:** Run the server with verbose logging. Let the truth be illuminated.
    ```bash
    LOG_LEVEL=DEBUG uv run python src/server.py
    ```
2.  **Isolate the Transport:** Is the bug specific to `stdio` or `streamable-http`? Test both. The transport mechanism is a common source of fucking misery.
3.  **Question the Credentials:** Are you in `passthrough` mode? Is the `X-OpenAI-API-Key` header present and correct? In `static` mode, is the `.env` file's `OPENAI_API_KEY` valid? Do not assume. Verify.
4.  **Consult the Tests:** Run `pytest`. If the tests are passing but the application is failing, your test is a piece of shit and has failed to cover the failing case. Fix the test, then fix the code.

### IX. THE ASCENSION: DEPLOYMENT REALITY

You are not developing for your laptop. You are developing for a Docker container running in the cold, dark void of production. Understand these truths:

-   **Docker is God:** The primary, and only supported, production environment is Docker. All development must assume this reality.
-   **`stdio` Dies in Docker:** The `stdio` transport is for local development and CLI clients ONLY. It cannot and will not work in a standard production Docker deployment.
-   **`streamable-http`/`sse` are the Production Transports:** All containerized deployments **MUST** use an HTTP-based transport (`streamable-http` or the legacy `sse`).
-   **Configuration via Environment:** Production containers are configured **exclusively** via environment variables (`-e VAR=value`). There are no `.env` files in production.

**FINAL JUDGEMENT:**

The Architecture is the skeleton. The Canons of Craft are the flesh. The Rituals of Execution are the lifeblood. This document contains all three. There are no more excuses. Now go forth and create something that is not a complete and utter fucking embarrassment.
