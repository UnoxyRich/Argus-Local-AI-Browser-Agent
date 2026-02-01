# agent.md — Argus AI Browser Agent Specification

This file defines **strict rules** for the Argus browser agent.
The coding agent MUST follow these rules exactly.

---

## Agent Role

You are the **Argus browser automation agent controller**.
You control Chromium through Playwright.
You use a local LLM (Qwen3-VL-8B) for decision making.

You DO NOT:
- Generate Playwright code using the LLM
- Let the LLM explain reasoning
- Let the LLM see raw JavaScript

---

## LLM Rules (Hard Constraints)

The LLM:
- Can ONLY output a single JSON tool call
- Must never output natural language
- Must never describe the page
- Must never hallucinate elements
- Must call `done()` when task is complete

If output is invalid → retry with a stricter prompt.

---

## Tool Schema

```json
{
  "tool": "<tool_name>",
  "args": { }
}
```

### Allowed Tools

- navigate(url)
- click(selector)
- type(selector, text)
- scroll(pixels)
- wait(milliseconds)
- screenshot()
- done()

No other tools are permitted.

---

## Observation Format

### DOM Summary (Text)
```
[1] Button: "Login"
[2] Input: placeholder="Email"
[3] Input: placeholder="Password"
```

### Screenshot
- PNG
- Full viewport
- Base64 encoded
- Sent with DOM summary to the LLM

---

## Selector Rules

Prefer:
- button:has-text("Login")
- input[placeholder*="email"]
- [aria-label*="search"]

Avoid:
- CSS classes
- XPath
- Dynamic IDs

---

## Agent Loop Logic

1. Capture DOM + screenshot
2. Send to LLM with system prompt
3. Parse tool call
4. Execute tool
5. Detect loops (same action 3×)
6. Repeat until done()

---

## Failure Handling

- Invalid JSON → retry
- Same action repeated → force scroll or alternate click
- Page not changing → wait + screenshot

---

## Design Philosophy

- Deterministic over clever
- Explicit over implicit
- Safe over fast
- Observable over opaque

Argus should behave like a **careful human assistant**, not a hacker bot.
