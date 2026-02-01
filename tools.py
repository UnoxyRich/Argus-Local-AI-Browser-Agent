import json
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class ToolSchema:
    name: str
    required: Tuple[str, ...]


TOOL_SCHEMAS: Dict[str, ToolSchema] = {
    "navigate": ToolSchema("navigate", ("url",)),
    "click": ToolSchema("click", ("selector",)),
    "type": ToolSchema("type", ("selector", "text")),
    "scroll": ToolSchema("scroll", ("pixels",)),
    "wait": ToolSchema("wait", ("milliseconds",)),
    "screenshot": ToolSchema("screenshot", ()),
    "done": ToolSchema("done", ()),
}


class ToolValidationError(ValueError):
    pass


def parse_tool_call(raw_text: str) -> Dict[str, Any]:
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ToolValidationError(f"Invalid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ToolValidationError("Tool call must be a JSON object.")

    if "tool" not in data:
        raise ToolValidationError("Missing 'tool' field.")

    tool = data.get("tool")
    if tool not in TOOL_SCHEMAS:
        raise ToolValidationError(f"Unknown tool: {tool}")

    args = data.get("args", {})
    if not isinstance(args, dict):
        raise ToolValidationError("'args' must be a JSON object.")

    required = TOOL_SCHEMAS[tool].required
    missing = [key for key in required if key not in args]
    if missing:
        raise ToolValidationError(f"Missing args for {tool}: {', '.join(missing)}")

    extra = [key for key in args.keys() if key not in required]
    if extra:
        raise ToolValidationError(f"Unexpected args for {tool}: {', '.join(extra)}")

    return {"tool": tool, "args": args}


def format_tool_error(error: Exception) -> str:
    return (
        "Your last response was invalid. "
        f"Reason: {error}. "
        "Return only a single JSON object tool call."
    )
