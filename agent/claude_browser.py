"""
Claude.ai Browser Automation

Drives claude.ai via Playwright for learning sessions.
Separate Chrome profile, file uploads, conversation capture.

Fragile - claude.ai UI changes will break selectors.
Screenshot every step for debugging.
"""

import asyncio
import base64
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
from playwright.async_api import async_playwright, Page, Browser


class ClaudeBrowser:
    """
    Automates claude.ai for structured learning sessions.
    Uses persistent Chrome profile for Worker Bee.
    """

    PROFILE_DIR = Path.home() / "Library/Application Support/Google/Chrome/Worker Bee Claude"
    SCREENSHOT_DIR = Path.home() / "worker-bee/logs/learning-screenshots"
    TIMEOUT = 30000  # 30 seconds

    # Claude.ai selectors (will break when UI updates)
    SELECTORS = {
        "chat_input": [
            "div[contenteditable='true']",
            "textarea[placeholder*='Reply']",
            ".ProseMirror",
            "[role='textbox']"
        ],
        "send_button": [
            "button[aria-label*='Send']",
            "button:has-text('Send')",
            "button[type='submit']"
        ],
        "file_upload": [
            "button[aria-label*='Attach']",
            "button:has-text('Attach')",
            "input[type='file']"
        ],
        "messages": [
            "div[data-test-render-count]",
            ".font-claude-message",
            "[class*='message']"
        ],
        "new_chat": [
            "a[href='/new']",
            "button:has-text('New chat')"
        ]
    }

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.session_id = None
        self.transcript = []

        # Create directories
        self.PROFILE_DIR.mkdir(parents=True, exist_ok=True)
        self.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    async def launch(self, session_id: str):
        """Launch browser with Worker Bee profile"""
        self.session_id = session_id
        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.PROFILE_DIR),
            headless=False,  # Visible so Toby can peek if needed
            viewport={"width": 1400, "height": 1000},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )

        # Get or create page
        if self.browser.pages:
            self.page = self.browser.pages[0]
        else:
            self.page = await self.browser.new_page()

        await self._screenshot("browser_launched")

    async def navigate_to_claude(self) -> bool:
        """Navigate to claude.ai and verify login"""
        try:
            await self.page.goto("https://claude.ai/new", timeout=self.TIMEOUT)
            await asyncio.sleep(2)
            await self._screenshot("navigated_to_claude")

            # Check if logged in by looking for chat input
            is_logged_in = await self._is_logged_in()

            if not is_logged_in:
                await self._screenshot("login_required")
                return False

            await self._screenshot("login_verified")
            return True

        except Exception as e:
            await self._screenshot(f"navigation_error")
            raise Exception(f"Failed to navigate to claude.ai: {e}")

    async def _is_logged_in(self) -> bool:
        """Check if logged in by detecting chat input"""
        for selector in self.SELECTORS["chat_input"]:
            try:
                element = await self.page.wait_for_selector(
                    selector, timeout=5000, state="visible"
                )
                if element:
                    return True
            except:
                continue
        return False

    async def upload_files(self, file_paths: List[str]):
        """Upload files to claude.ai conversation"""
        if not file_paths:
            return

        for file_path in file_paths:
            if not Path(file_path).exists():
                continue

            try:
                # Find file upload button/input
                upload_input = None
                for selector in self.SELECTORS["file_upload"]:
                    try:
                        upload_input = await self.page.wait_for_selector(
                            selector, timeout=5000
                        )
                        if upload_input:
                            break
                    except:
                        continue

                if upload_input:
                    # If it's an input[type=file], set files directly
                    if await upload_input.get_attribute("type") == "file":
                        await upload_input.set_input_files(file_path)
                    else:
                        # Otherwise click button, then find file input
                        await upload_input.click()
                        await asyncio.sleep(1)
                        file_input = await self.page.wait_for_selector(
                            "input[type='file']", timeout=5000
                        )
                        if file_input:
                            await file_input.set_input_files(file_path)

                    await asyncio.sleep(1)
                    await self._screenshot(f"uploaded_{Path(file_path).name}")

            except Exception as e:
                await self._screenshot(f"upload_error_{Path(file_path).name}")
                # Continue even if upload fails - session can proceed

    async def send_message(self, message: str) -> bool:
        """Send message to Claude"""
        try:
            # Find chat input
            chat_input = None
            for selector in self.SELECTORS["chat_input"]:
                try:
                    chat_input = await self.page.wait_for_selector(
                        selector, timeout=5000, state="visible"
                    )
                    if chat_input:
                        break
                except:
                    continue

            if not chat_input:
                raise Exception("Could not find chat input")

            # Type message
            await chat_input.click()
            await chat_input.fill(message)
            await asyncio.sleep(0.5)
            await self._screenshot("message_typed")

            # Find and click send button
            send_button = None
            for selector in self.SELECTORS["send_button"]:
                try:
                    send_button = await self.page.wait_for_selector(
                        selector, timeout=5000, state="visible"
                    )
                    if send_button:
                        break
                except:
                    continue

            if not send_button:
                raise Exception("Could not find send button")

            await send_button.click()
            await self._screenshot("message_sent")

            # Record in transcript
            self.transcript.append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })

            return True

        except Exception as e:
            await self._screenshot("send_error")
            raise Exception(f"Failed to send message: {e}")

    async def wait_for_response(self, timeout_seconds: int = 60) -> str:
        """Wait for Claude's response and extract it"""
        try:
            # Wait for response to appear (detect typing indicator disappearing)
            await asyncio.sleep(3)  # Initial wait

            # Get all message elements
            messages_selector = self.SELECTORS["messages"][0]
            await self.page.wait_for_selector(messages_selector, timeout=timeout_seconds * 1000)

            # Extract last message (Claude's response)
            messages = await self.page.query_selector_all(messages_selector)
            if messages:
                last_message = messages[-1]
                response_text = await last_message.inner_text()

                await self._screenshot("response_received")

                # Record in transcript
                self.transcript.append({
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": datetime.now().isoformat()
                })

                return response_text
            else:
                return ""

        except Exception as e:
            await self._screenshot("response_error")
            return f"[Error getting response: {e}]"

    async def run_conversation(self, initial_message: str,
                               duration_minutes: int = 20) -> List[Dict]:
        """
        Run full conversation for specified duration.
        Returns transcript.
        """
        start_time = datetime.now()
        end_time = start_time.replace(
            minute=start_time.minute + duration_minutes
        )

        # Send initial message
        await self.send_message(initial_message)
        await self.wait_for_response()

        # Continue conversation until time limit
        # This is simplified - in reality, would need more sophisticated
        # dialogue management based on session phases
        while datetime.now() < end_time:
            await asyncio.sleep(30)  # Wait for user input or auto-continue

            # In practice, this would be driven by session brief phases
            # and would include teach-back evaluation, etc.

        return self.transcript

    async def extract_claude_summary(self) -> Optional[str]:
        """
        Extract claude-summary.md from conversation.
        Claude should output this at end of session.
        """
        # Look for Claude's final message containing summary
        if self.transcript:
            for message in reversed(self.transcript):
                if message["role"] == "assistant":
                    # Check if this looks like a summary
                    content = message["content"]
                    if "summary" in content.lower() or "## What we covered" in content:
                        return content

        return None

    async def save_transcript(self, output_dir: Path):
        """Save full conversation transcript to markdown"""
        output_dir.mkdir(parents=True, exist_ok=True)
        transcript_file = output_dir / "transcript.md"

        with open(transcript_file, 'w') as f:
            f.write(f"# Learning Session Transcript\n")
            f.write(f"**Session ID:** {self.session_id}\n")
            f.write(f"**Started:** {self.transcript[0]['timestamp'] if self.transcript else 'N/A'}\n\n")
            f.write("---\n\n")

            for message in self.transcript:
                role = "🧑 User" if message["role"] == "user" else "🤖 Claude"
                f.write(f"## {role} — {message['timestamp']}\n\n")
                f.write(f"{message['content']}\n\n")
                f.write("---\n\n")

    async def _screenshot(self, name: str):
        """Take screenshot for debugging"""
        if self.page:
            try:
                screenshot_path = self.SCREENSHOT_DIR / f"{self.session_id}_{name}.png"
                await self.page.screenshot(path=str(screenshot_path))
            except:
                pass  # Don't fail session if screenshot fails

    async def close(self):
        """Close browser and cleanup"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


# Example usage for testing
async def test_session():
    """Test browser automation"""
    browser = ClaudeBrowser()

    try:
        await browser.launch("test-2026-04-25-0900")
        logged_in = await browser.navigate_to_claude()

        if not logged_in:
            print("Not logged in to claude.ai")
            print("Please log in manually in the browser window")
            await asyncio.sleep(60)  # Give time to log in manually

        # Test message
        await browser.send_message("Hello, this is a test message from Worker Bee automation.")
        response = await browser.wait_for_response()
        print(f"Claude responded: {response[:100]}...")

        # Save transcript
        output_dir = Path.home() / "worker-bee/manifests/practice/learning-sessions/test-2026-04-25-0900"
        await browser.save_transcript(output_dir)

    finally:
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_session())
