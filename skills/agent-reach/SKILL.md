---
name: agent-reach
description: Read and search external sources through the channels installed on this machine. Use when the task needs content from a feed, a video, Reddit, or LinkedIn.
---

# agent-reach

Installed channels only. Run `agent-reach doctor` first if a call fails; a channel can be installed but unauthenticated.

Every command returns the same envelope, so the output shape does not change per channel.
Use `--max-tokens` whenever the source could be long.

```
agent-reach get <channel>.<command> <query> [--max-tokens N] [--limit N] [--json]
```

## Channels

### rss
Read any RSS or Atom feed as clean text.
- `agent-reach get rss.feed <query>`

### youtube
Video metadata and transcripts, via yt-dlp.
- `agent-reach get youtube.transcript <query>`
- `agent-reach get youtube.info <query>`

### Custom Extensions (Reddit & LinkedIn)
Scrape Reddit threads or LinkedIn profile pages as clean markdown via Jina Reader.
- `python "C:/Users/admin/.gemini/config/skills/agent-reach/scripts/scrape.py" --reddit <url_or_query>`
- `python "C:/Users/admin/.gemini/config/skills/agent-reach/scripts/scrape.py" --linkedin <profile_url>`
