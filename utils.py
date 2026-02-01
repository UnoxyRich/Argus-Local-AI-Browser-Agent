import base64
import hashlib
import os
import time
from typing import Dict


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def now_stamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_image_message(image_path: str) -> Dict[str, str]:
    with open(image_path, "rb") as handle:
        encoded = base64.b64encode(handle.read()).decode("utf-8")
    return {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}}


def save_screenshot(page, output_dir: str) -> str:
    ensure_dir(output_dir)
    filename = f"screenshot-{now_stamp()}.png"
    path = os.path.join(output_dir, filename)
    page.screenshot(path=path, full_page=True)
    return path


def extract_dom(page) -> str:
    script = """
() => {
  const elements = Array.from(document.querySelectorAll('*'));
  const rows = [];
  for (const el of elements) {
    const rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) continue;
    const style = window.getComputedStyle(el);
    if (style.visibility === 'hidden' || style.display === 'none') continue;

    const tag = el.tagName.toLowerCase();
    const id = el.id ? `#${el.id}` : '';
    const classes = el.className && typeof el.className === 'string'
      ? '.' + el.className.trim().split(/\s+/).slice(0, 3).join('.')
      : '';
    const role = el.getAttribute('role') || '';
    const name = el.getAttribute('aria-label') || el.getAttribute('name') || '';
    const text = (el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 160);
    if (!text && !name) continue;
    rows.push([tag + id + classes, role, name, text].filter(Boolean).join(' | '));
    if (rows.length >= 300) break;
  }
  return rows.join('\n');
}
"""
    return page.evaluate(script)
