FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Runtime deps for TraceHunt + the MCP SDK
RUN pip install --no-cache-dir -r requirements.txt "mcp"

# Start the MCP server over stdio
CMD ["python", "mcp/tracehunt_mcp.py"]
