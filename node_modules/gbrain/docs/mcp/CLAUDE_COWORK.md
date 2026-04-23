# Connect GBrain to Claude Cowork

Two ways to get GBrain into Cowork sessions:

## Option 1: Remote (via Edge Function)

For Team/Enterprise plans, an org Owner adds the connector:

1. Go to **Organization Settings > Connectors**
2. Add a new connector with the MCP server URL:
   ```
   https://YOUR_REF.supabase.co/functions/v1/gbrain-mcp/mcp
   ```
3. Optionally add Bearer token authentication in Advanced Settings
4. Save

Note: Cowork connects from Anthropic's cloud, not your device. The Edge Function is already publicly reachable via Supabase.

## Option 2: Local Bridge (via Claude Desktop)

If you already have GBrain configured in Claude Desktop (either via `gbrain serve` stdio or the remote MCP integration), Cowork gets access automatically. Claude Desktop bridges local MCP servers into Cowork via its SDK layer.

This means: if `gbrain serve` is running and configured in Claude Desktop, you don't need the Edge Function for Cowork at all.

## Which to use?

- **Remote Edge Function:** works even when your laptop is closed, available to all org members
- **Local Bridge:** zero extra setup if Claude Desktop already has GBrain, but requires your machine to be running
