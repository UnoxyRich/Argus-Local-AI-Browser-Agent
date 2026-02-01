from typing import Optional, Tuple

from playwright.sync_api import sync_playwright

from utils import extract_dom, save_screenshot


class Browser:
    def __init__(self, headless: bool = False, output_dir: str = "artifacts") -> None:
        self.headless = headless
        self.output_dir = output_dir
        self._playwright = None
        self._browser = None
        self._page = None

    def start(self) -> None:
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        context = self._browser.new_context()
        self._page = context.new_page()

    def close(self) -> None:
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    @property
    def page(self):
        if not self._page:
            raise RuntimeError("Browser not started.")
        return self._page

    def navigate(self, url: str) -> None:
        self.page.goto(url, wait_until="load")

    def click(self, selector: str) -> None:
        self.page.click(selector, timeout=5000)

    def type(self, selector: str, text: str) -> None:
        self.page.fill(selector, text, timeout=5000)

    def scroll(self, pixels: int) -> None:
        self.page.evaluate("window.scrollBy(0, arguments[0])", pixels)

    def wait(self, milliseconds: int) -> None:
        self.page.wait_for_timeout(milliseconds)

    def screenshot(self) -> str:
        return save_screenshot(self.page, self.output_dir)

    def observe(self) -> Tuple[str, str]:
        dom_text = extract_dom(self.page)
        screenshot_path = save_screenshot(self.page, self.output_dir)
        return dom_text, screenshot_path
