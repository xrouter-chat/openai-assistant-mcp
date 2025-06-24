#!/bin/bash

# Load environment variables from .env
set -a
source .env
set +a

echo "Starting OpenAI Assistant MCP server with MCP Inspector..."
echo "Server URL: http://localhost:${PORT}"
echo "Transport: ${TRANSPORT}"
echo "OpenAI API Key: ${OPENAI_API_KEY:0:20}..."

# Determine the correct endpoint based on transport
if [ "${TRANSPORT}" = "sse" ]; then
    ENDPOINT="/messages"
    SERVER_TYPE="sse"
elif [ "${TRANSPORT}" = "streamable-http" ] || [ "${TRANSPORT}" = "http" ]; then
    ENDPOINT=""
    SERVER_TYPE="http"
else
    echo "Error: Unsupported transport '${TRANSPORT}' for MCP Inspector"
    exit 1
fi

uvx mcpo --port 8600 --server-type "${SERVER_TYPE}" \
    --header "{
        \"X-OpenAI-API-Key\": \"${OPENAI_API_KEY}\"
    }" \
    -- http://localhost:${PORT}${ENDPOINT}
