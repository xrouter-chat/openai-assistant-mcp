# OpenAI Assistant MCP Server

This document describes the OpenAI Assistant MCP server that provides tools for interacting with the OpenAI Assistant API.

## Overview

The OpenAI Assistant MCP server provides a set of tools for creating and managing AI assistants through OpenAI's Assistant API. It acts as a thin wrapper around the official OpenAI API, providing direct access to assistant management, thread operations, messaging, and run execution capabilities.

## Dependencies

- `openai>=1.18.0` - Official OpenAI Python client library with Assistants API support

## Configuration

The server requires the following configuration:

```json
{
  "api_key": "your-openai-api-key"
}
```

## Tools

### Assistant Management

#### create_assistant
Creates a new assistant with specified configuration.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "model": {
      "type": "string",
      "description": "ID of the model to use"
    },
    "name": {
      "type": "string",
      "description": "The name of the assistant (max 256 characters)"
    },
    "description": {
      "type": "string",
      "description": "The description of the assistant (max 512 characters)"
    },
    "instructions": {
      "type": "string",
      "description": "System instructions for the assistant (max 256k characters)"
    },
    "tools": {
      "type": "array",
      "description": "List of tools enabled for the assistant",
      "items": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "enum": ["code_interpreter", "file_search", "function"]
          }
        }
      }
    }
  },
  "required": ["model"]
}
```

#### list_assistants
Lists available assistants.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "limit": {
      "type": "integer",
      "description": "Number of assistants to return (1-100)",
      "default": 20
    },
    "order": {
      "type": "string",
      "enum": ["asc", "desc"],
      "default": "desc"
    },
    "after": {
      "type": "string",
      "description": "Pagination cursor for the next page"
    },
    "before": {
      "type": "string",
      "description": "Pagination cursor for the previous page"
    }
  }
}
```

#### retrieve_assistant
Retrieves a specific assistant by ID.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "assistant_id": {
      "type": "string",
      "description": "The ID of the assistant to retrieve"
    }
  },
  "required": ["assistant_id"]
}
```

#### modify_assistant
Modifies an existing assistant.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "assistant_id": {
      "type": "string",
      "description": "The ID of the assistant to modify"
    },
    "model": {
      "type": "string",
      "description": "ID of the model to use"
    },
    "name": {
      "type": "string",
      "description": "The name of the assistant"
    },
    "description": {
      "type": "string",
      "description": "The description of the assistant"
    },
    "instructions": {
      "type": "string",
      "description": "System instructions for the assistant"
    },
    "tools": {
      "type": "array",
      "description": "List of tools enabled for the assistant"
    }
  },
  "required": ["assistant_id"]
}
```

#### delete_assistant
Deletes an assistant.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "assistant_id": {
      "type": "string",
      "description": "The ID of the assistant to delete"
    }
  },
  "required": ["assistant_id"]
}
```

### Thread Management

#### create_thread
Creates a new thread, optionally with initial messages.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "messages": {
      "type": "array",
      "description": "Initial messages for the thread",
      "items": {
        "type": "object",
        "properties": {
          "role": {
            "type": "string",
            "enum": ["user", "assistant"]
          },
          "content": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

#### retrieve_thread
Retrieves a specific thread.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread to retrieve"
    }
  },
  "required": ["thread_id"]
}
```

#### modify_thread
Modifies a thread's metadata.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread to modify"
    },
    "metadata": {
      "type": "object",
      "description": "Set of key-value pairs for the thread"
    }
  },
  "required": ["thread_id"]
}
```

#### delete_thread
Deletes a thread.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread to delete"
    }
  },
  "required": ["thread_id"]
}
```

### Message Management

#### create_message
Creates a new message in a thread.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread to create a message in"
    },
    "role": {
      "type": "string",
      "enum": ["user", "assistant"],
      "description": "The role of the entity creating the message"
    },
    "content": {
      "type": "string",
      "description": "The content of the message"
    }
  },
  "required": ["thread_id", "role", "content"]
}
```

#### list_messages
Lists messages in a thread.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread"
    },
    "limit": {
      "type": "integer",
      "description": "Number of messages to return (1-100)",
      "default": 20
    },
    "order": {
      "type": "string",
      "enum": ["asc", "desc"],
      "default": "desc"
    },
    "after": {
      "type": "string",
      "description": "Pagination cursor for the next page"
    },
    "before": {
      "type": "string",
      "description": "Pagination cursor for the previous page"
    }
  },
  "required": ["thread_id"]
}
```

#### retrieve_message
Retrieves a specific message.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread"
    },
    "message_id": {
      "type": "string",
      "description": "The ID of the message to retrieve"
    }
  },
  "required": ["thread_id", "message_id"]
}
```

#### modify_message
Modifies a message's metadata.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread"
    },
    "message_id": {
      "type": "string",
      "description": "The ID of the message to modify"
    },
    "metadata": {
      "type": "object",
      "description": "Set of key-value pairs for the message"
    }
  },
  "required": ["thread_id", "message_id"]
}
```

### Run Management

#### create_run
Creates a new run on a thread.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread to run"
    },
    "assistant_id": {
      "type": "string",
      "description": "The ID of the assistant to use"
    },
    "model": {
      "type": "string",
      "description": "Optional model override for this run"
    },
    "instructions": {
      "type": "string",
      "description": "Optional instructions override for this run"
    },
    "stream": {
      "type": "boolean",
      "description": "Whether to stream the response",
      "default": false
    }
  },
  "required": ["thread_id", "assistant_id"]
}
```

#### create_thread_and_run
Creates a new thread and immediately runs it.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "assistant_id": {
      "type": "string",
      "description": "The ID of the assistant to use"
    },
    "thread": {
      "type": "object",
      "properties": {
        "messages": {
          "type": "array",
          "description": "Initial messages for the thread"
        }
      }
    },
    "model": {
      "type": "string",
      "description": "Optional model override"
    },
    "instructions": {
      "type": "string",
      "description": "Optional instructions override"
    },
    "stream": {
      "type": "boolean",
      "description": "Whether to stream the response",
      "default": false
    }
  },
  "required": ["assistant_id"]
}
```

#### list_runs
Lists runs in a thread.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread"
    },
    "limit": {
      "type": "integer",
      "description": "Number of runs to return (1-100)",
      "default": 20
    },
    "order": {
      "type": "string",
      "enum": ["asc", "desc"],
      "default": "desc"
    }
  },
  "required": ["thread_id"]
}
```

#### retrieve_run
Retrieves a specific run.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread"
    },
    "run_id": {
      "type": "string",
      "description": "The ID of the run to retrieve"
    }
  },
  "required": ["thread_id", "run_id"]
}
```

#### modify_run
Modifies a run's metadata.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread"
    },
    "run_id": {
      "type": "string",
      "description": "The ID of the run to modify"
    },
    "metadata": {
      "type": "object",
      "description": "Set of key-value pairs for the run"
    }
  },
  "required": ["thread_id", "run_id"]
}
```

#### submit_tool_outputs
Submits outputs for tool calls.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread"
    },
    "run_id": {
      "type": "string",
      "description": "The ID of the run"
    },
    "tool_outputs": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "tool_call_id": {
            "type": "string",
            "description": "The ID of the tool call"
          },
          "output": {
            "type": "string",
            "description": "The output of the tool call"
          }
        },
        "required": ["tool_call_id", "output"]
      }
    }
  },
  "required": ["thread_id", "run_id", "tool_outputs"]
}
```

#### cancel_run
Cancels a run.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread"
    },
    "run_id": {
      "type": "string",
      "description": "The ID of the run to cancel"
    }
  },
  "required": ["thread_id", "run_id"]
}
```

### Run Steps

#### list_run_steps
Lists steps in a run.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread"
    },
    "run_id": {
      "type": "string",
      "description": "The ID of the run"
    },
    "limit": {
      "type": "integer",
      "description": "Number of run steps to return (1-100)",
      "default": 20
    },
    "order": {
      "type": "string",
      "enum": ["asc", "desc"],
      "default": "desc"
    }
  },
  "required": ["thread_id", "run_id"]
}
```

#### retrieve_run_step
Retrieves a specific run step.

Input schema:
```json
{
  "type": "object",
  "properties": {
    "thread_id": {
      "type": "string",
      "description": "The ID of the thread"
    },
    "run_id": {
      "type": "string",
      "description": "The ID of the run"
    },
    "step_id": {
      "type": "string",
      "description": "The ID of the step to retrieve"
    }
  },
  "required": ["thread_id", "run_id", "step_id"]
}
```

## Response Formats

All tools return responses in the following format:

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "The ID of the created/retrieved object"
    },
    "object": {
      "type": "string",
      "description": "The type of object (e.g., 'assistant', 'thread', 'message', etc.)"
    },
    "created_at": {
      "type": "integer",
      "description": "Unix timestamp for when the object was created"
    }
  }
}
```

Additional properties are included based on the specific object type being returned.

## Error Handling

The server returns standard HTTP error codes:

- 400: Bad Request - Invalid parameters
- 401: Unauthorized - Invalid API key
- 404: Not Found - Resource not found
- 429: Too Many Requests - Rate limit exceeded
- 500: Internal Server Error - Server error

Error responses include:
```json
{
  "type": "object",
  "properties": {
    "error": {
      "type": "object",
      "properties": {
        "message": {
          "type": "string",
          "description": "Human-readable error message"
        },
        "type": {
          "type": "string",
          "description": "Error type identifier"
        },
        "code": {
          "type": "string",
          "description": "Error code"
        }
      }
    }
  }
}
