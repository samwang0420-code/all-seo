# Alternative: Self-Hosted MCP Server

If you prefer running GBrain on your own machine instead of Supabase Edge Functions, you can expose `gbrain serve --http` via a tunnel.

## Tailscale Funnel

[Tailscale Funnel](https://tailscale.com/kb/1223/tailscale-funnel) gives you a permanent public HTTPS URL with automatic TLS. Free tier available.

```bash
# 1. Install Tailscale
brew install tailscale

# 2. Start gbrain with HTTP transport (when available)
gbrain serve --http 3000

# 3. Expose via Funnel
tailscale funnel 3000
# Your brain is now at https://your-machine.ts.net
```

Pros: zero deployment, no Deno bundling, no cold start, no timeout limits.
Cons: requires your machine to be running and connected.

## ngrok

[ngrok](https://ngrok.com) provides temporary or persistent tunnels.

```bash
# 1. Install ngrok
brew install ngrok

# 2. Start gbrain with HTTP transport
gbrain serve --http 3000

# 3. Expose via ngrok
ngrok http 3000
# Use the generated URL in your MCP client config
```

Pros: quick setup, works behind firewalls.
Cons: free tier URLs change on restart (paid tier for persistent URLs), requires running process.

## When to use alternatives vs Edge Functions

| | Edge Functions | Tailscale/ngrok |
|--|---|---|
| Works when laptop is off | Yes | No |
| Zero cold start | No (~300ms) | Yes |
| No timeout limits | No (60s) | Yes |
| sync_brain remotely | No | Yes |
| file_upload remotely | No | Yes |
| Extra accounts needed | None | Tailscale or ngrok |

Note: `gbrain serve --http` is planned but not yet implemented. Currently only stdio transport is available via `gbrain serve`.
