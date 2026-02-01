import argparse
from typing import Dict, List

from browser import Browser
from llm_client import LLMClient
from prompts import SYSTEM_PROMPT
from tools import ToolValidationError, format_tool_error, parse_tool_call
from utils import build_image_message, hash_text


def build_observation_message(
    goal: str,
    url: str,
    dom: str,
    screenshot_path: str,
    step: int,
) -> Dict:
    text = (
        f"Step {step}\n"
        f"User goal: {goal}\n"
        f"Current URL: {url}\n"
        "Visible DOM summary:\n"
        f"{dom}\n"
        "Return the next tool call JSON."
    )
    content = [{"type": "text", "text": text}, build_image_message(screenshot_path)]
    return {"role": "user", "content": content}


def run_agent(goal: str, headless: bool, max_steps: int) -> None:
    browser = Browser(headless=headless)
    llm = LLMClient()
    messages: List[Dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    tool_history: List[str] = []
    same_obs_count = 0
    last_obs_hash = ""

    try:
        browser.start()
        dom, screenshot_path = browser.observe()

        for step in range(1, max_steps + 1):
            obs_message = build_observation_message(
                goal=goal,
                url=browser.page.url,
                dom=dom,
                screenshot_path=screenshot_path,
                step=step,
            )
            messages.append(obs_message)

            response = llm.chat(messages)
            try:
                tool_call = parse_tool_call(response)
            except ToolValidationError as exc:
                messages.append({"role": "user", "content": format_tool_error(exc)})
                response = llm.chat(messages)
                tool_call = parse_tool_call(response)

            tool_name = tool_call["tool"]
            args = tool_call["args"]
            tool_signature = f"{tool_name}:{args}"
            tool_history.append(tool_signature)

            if tool_name == "done":
                break

            if tool_name == "navigate":
                browser.navigate(args["url"])
            elif tool_name == "click":
                browser.click(args["selector"])
            elif tool_name == "type":
                browser.type(args["selector"], args["text"])
            elif tool_name == "scroll":
                browser.scroll(int(args["pixels"]))
            elif tool_name == "wait":
                browser.wait(int(args["milliseconds"]))
            elif tool_name == "screenshot":
                browser.screenshot()
            else:
                raise RuntimeError(f"Unsupported tool: {tool_name}")

            dom, screenshot_path = browser.observe()
            obs_hash = hash_text(dom + browser.page.url)
            if obs_hash == last_obs_hash:
                same_obs_count += 1
            else:
                same_obs_count = 0
            last_obs_hash = obs_hash

            if same_obs_count >= 2:
                break

            if len(tool_history) >= 3 and len(set(tool_history[-3:])) == 1:
                break

    finally:
        browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Argus local browser agent")
    parser.add_argument("goal", help="User goal for the agent")
    parser.add_argument("--headless", action="store_true", help="Run Chromium headless")
    parser.add_argument("--max-steps", type=int, default=20, help="Max steps")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_agent(args.goal, headless=args.headless, max_steps=args.max_steps)
