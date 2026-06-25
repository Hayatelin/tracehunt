# TraceHunt MCP server

Give your AI coding agent the ability to run OSINT username recon — it can call
TraceHunt directly through the [Model Context Protocol](https://modelcontextprotocol.io).

## Install

```bash
pip install "mcp[cli]" requests requests-futures
```

## Tools exposed
- `hunt_username(username, sites?, timeout?)` → platforms the handle exists on + a 0–100 footprint score
- `footprint_score(username, timeout?)` → just the summary numbers

## Register with your agent

**Claude Code / Claude Desktop** — add to your MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "tracehunt": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/tracehunt/mcp/tracehunt_mcp.py"]
    }
  }
}
```

**Cursor** — Settings → MCP → Add, same command/args.

**Gemini CLI / Codex** — point their MCP server config at the same command.

Then just ask your agent: *"use tracehunt to check the username `octocat`"*.

> ⚠️ For authorized security research and OSINT only.
