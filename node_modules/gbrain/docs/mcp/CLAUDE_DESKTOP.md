# Connect GBrain to Claude Desktop

**Important:** Claude Desktop does NOT connect to remote MCP servers via `claude_desktop_config.json`. That file only works for local stdio servers. Remote HTTP servers must be added through the GUI.

## Setup

1. Open Claude Desktop
2. Go to **Settings > Integrations**
3. Click **Add Integration** (or **Add Connector**)
4. Enter the MCP server URL:
   ```
   https://YOUR_REF.supabase.co/functions/v1/gbrain-mcp/mcp
   ```
5. Set authentication to **Bearer Token** and paste your token
6. Save

## Verify

Start a new conversation and try:

```
Search my brain for [any topic]
```

Claude Desktop will use your GBrain tools automatically.

## Common Mistakes

**Using claude_desktop_config.json for remote servers** — this silently fails. The JSON config only works for local stdio MCP servers. Remote HTTP servers must be added via Settings > Integrations.

**Using the wrong URL** — make sure the URL ends with `/mcp` (not `/health` or just the function name).
