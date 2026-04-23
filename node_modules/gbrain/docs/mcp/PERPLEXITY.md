# Connect GBrain to Perplexity Computer

Perplexity Computer supports remote MCP servers with bearer token authentication.

## Setup

1. Open Perplexity (requires Pro subscription)
2. Go to **Settings > Connectors** (or **MCP Servers**)
3. Add a new remote connector:
   - **URL:** `https://YOUR_REF.supabase.co/functions/v1/gbrain-mcp/mcp`
   - **Authentication:** API Key / Bearer Token
   - **Token:** your GBrain access token
4. Save

## Verify

In a Perplexity conversation, ask it to use your brain:

```
Use my GBrain to search for [topic]
```

## Notes

- Perplexity Computer is available to Pro subscribers
- Both the Perplexity Mac app and web version support MCP connectors
- The Mac app also supports local MCP servers if you prefer `gbrain serve` (stdio)
