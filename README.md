# Argus — Local AI Browser Agent (Qwen3-VL + Chromium)

Argus is a **local-first AI browser agent** inspired by Atlas-style agents.
It uses **Qwen/Qwen3-VL-8B** running via **LM Studio** as the reasoning + vision model,
and **Chromium (Playwright)** as the browser execution layer.

The agent can:
- Navigate websites
- Click buttons and links
- Fill forms
- Scroll pages
- Observe DOM + screenshots
- Decide next actions step-by-step

All reasoning happens **locally**. No GPT or cloud APIs are required.


## Project Name

**Argus** is named after the all-seeing watcher from Greek mythology.
The name reflects the agent’s core abilities:
- Observing web pages visually and structurally
- Acting carefully and deterministically
- Remaining always under human control

Argus is designed to *watch, decide, and act* — never to guess blindly.


---

## Architecture Overview

```
User Goal
   ↓
Agent Controller (Python)
   ↓
LM Studio (Qwen3-VL-8B, OpenAI-compatible API)
   ↓
Tool Call (JSON)
   ↓
Playwright Chromium
   ↓
DOM + Screenshot Observation
   ↺
```

---

## Requirements

### Software
- Windows 10/11
- Python 3.10+
- LM Studio (latest)
- Chromium (auto-installed by Playwright)

### Python Dependencies
```
pip install playwright pillow requests
playwright install chromium
```

---

## Model Setup (LM Studio)

1. Download model:
   - `qwen/qwen3-vl-8b`

2. Enable:
   - **OpenAI-compatible API**
   - **Vision support**
   - Context length: 8k–16k
   - Temperature: 0.2

3. Confirm endpoint:
   - `http://localhost:1234/v1/chat/completions`

---

## How It Works

1. User provides a task (e.g. "Log into GitHub")
2. Agent extracts:
   - Visible DOM elements
   - Screenshot of the page
3. Qwen3-VL selects **one tool action**
4. Playwright executes the action
5. Loop continues until `done()`

---

## Supported Tools

- navigate(url)
- click(selector)
- type(selector, text)
- scroll(pixels)
- wait(milliseconds)
- screenshot()
- done()

The LLM is **not allowed** to generate code — only tool calls.

---

## Safety & Limitations

- No credential storage (manual input recommended)
- Some sites may block automation
- Local models are weaker at long-horizon planning than GPT-4

---

## Roadmap

- [ ] Memory summarization
- [ ] Loop detection & recovery
- [ ] GUI (Electron / Tauri)
- [ ] Human-in-the-loop takeover
- [ ] Multi-agent planner/executor split

---

## License

MIT — build whatever you want 🚀
