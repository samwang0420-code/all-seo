# Connect GBrain to Claude Code

## Setup

```bash
claude mcp add gbrain -t http \
  https://YOUR_REF.supabase.co/functions/v1/gbrain-mcp/mcp \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Replace `YOUR_REF` with your Supabase project ref and `YOUR_TOKEN` with a token from `bun run src/commands/auth.ts create "claude-code"`.

## Verify

In Claude Code, try:

```
search for [any topic in your brain]
```

You should see results from your GBrain knowledge base.

## Remove

```bash
claude mcp remove gbrain
```
