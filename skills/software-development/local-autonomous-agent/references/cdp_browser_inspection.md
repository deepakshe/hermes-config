# CDP browser inspection (Chrome/Brave via DevTools Protocol)

## What works
- HTTP `/json` endpoint lists open pages and gives the `webSocketDebuggerUrl`:
  `curl -s http://127.0.0.1:9222/json`
  Returns JSON array: each entry has `id`, `type` (page/iframe/worker/background_page), `title`, `url`, `webSocketDebuggerUrl`.
- Use it to answer: current URL, page title, whether a site is logged in (e.g. Instagram `/accounts/edit/` is only reachable while authenticated), and to enumerate tabs.

## What fails
- Reading the DOM / executing JS via the browser-use harness (`js(...)`) frequently TIMES OUT when the page is behind a Chrome "Allow remote debugging?" permission popup. The harness reports: `Runtime.evaluate timed out`.
- WebSocket CDP connections from a script get `403 Forbidden` unless Chrome was launched with `--remote-allow-origins=*`.
- The `browser_exec` tool itself blocks with: `Chrome is asking "Allow remote debugging?" — click Allow to continue.`

## Honest reporting rule
- If a field value cannot be read (e.g. a form input on `/accounts/edit/`, or any DOM attribute), report it as unreadable and give the evidence you DO have (URL, title, login state). Never fabricate a username, field value, or "logged in as X" you did not actually verify.
- Example correct output: "Title: Edit profile • Instagram; URL: /accounts/edit/ → account is logged in; username field value: could not be read (DOM read timed out at CDP layer)."

## Bypasses that sometimes help (only if user explicitly permits)
- Launch the browser with `--remote-allow-origins=*` so WebSocket CDP works.
- Use the `/json` HTTP list (no WebSocket) for page metadata — that path does not need the extra flag.
- For real DOM interaction, prefer the Playwright tool layer (`tools/browser.py`) over CDP, since Playwright controls the page directly and is not gated by the debugging popup.
