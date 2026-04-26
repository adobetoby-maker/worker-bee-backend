from playwright.async_api import async_playwright
import base64, asyncio

class BrowserTool:
    def __init__(self):
        self._pw       = None
        self._browser  = None
        self._contexts = {}

    async def _ensure(self):
        if not self._browser:
            self._pw = await async_playwright().start()
            self._browser = await self._pw.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage",
                      "--disable-blink-features=AutomationControlled"]
            )

    async def _get_context(self, domain: str):
        await self._ensure()
        if domain in self._contexts:
            return self._contexts[domain]
        ctx = await self._browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
        )
        await ctx.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")
        self._contexts[domain] = ctx
        return ctx

    async def navigate(self, url: str) -> dict:
        await self._ensure()
        domain = url.split("/")[2] if "//" in url else url
        ctx    = await self._get_context(domain)
        page   = await ctx.new_page()
        try:
            await page.goto(url, timeout=30000, wait_until="networkidle")
            await page.wait_for_timeout(3000)
            for attempt in range(5):
                error_found = False
                for sel in ["text=An unexpected error occurred",
                            "text=Something went wrong",
                            "text=SOMETHING WENT WRONG",
                            "text=404"]:
                    try:
                        if await page.locator(sel).is_visible(timeout=1000):
                            error_found = True
                            break
                    except Exception:
                        pass
                if not error_found:
                    break
                clicked = False
                for sel in ["text=Try again", "text=Try Again",
                            "text=Retry", "button:has-text('Try')",
                            "button:has-text('Retry')"]:
                    try:
                        btn = page.locator(sel)
                        if await btn.is_visible(timeout=1000):
                            await btn.click()
                            clicked = True
                            break
                    except Exception:
                        pass
                if not clicked:
                    await page.reload(wait_until="networkidle")
                await page.wait_for_timeout(3000 + (attempt * 2000))
            shot = await page.screenshot(full_page=True)
            text = await page.inner_text("body")
            return {
                "url": page.url, "title": await page.title(),
                "text": text[:6000],
                "screenshot_b64": base64.b64encode(shot).decode(),
                "success": True
            }
        except Exception as e:
            return {"url": url, "error": str(e), "success": False}
        finally:
            await page.close()

    async def login(self, url: str, username: str,
                    password: str, max_attempts: int = 5) -> dict:
        await self._ensure()
        domain = url.split("/")[2] if "//" in url else url
        ctx    = await self._get_context(domain)
        EMAIL_SELS = [
            'input[type="email"]', 'input[name="email"]',
            'input[name="username"]', 'input[name="user"]',
            'input[id="email"]', 'input[id="username"]',
            'input[placeholder*="email" i]',
            'input[placeholder*="username" i]',
            'input[autocomplete="email"]',
            'input[autocomplete="username"]',
            'input:not([type="password"]):not([type="hidden"]):not([type="submit"])',
        ]
        PASS_SELS = [
            'input[type="password"]', 'input[name="password"]',
            'input[id="password"]', 'input[placeholder*="password" i]',
            'input[autocomplete="current-password"]',
        ]
        SUBMIT_SELS = [
            'button[type="submit"]', 'input[type="submit"]',
            'button:has-text("Sign in")', 'button:has-text("Log in")',
            'button:has-text("Login")', 'button:has-text("Continue")',
            'button:has-text("Next")', '[role="button"]:has-text("Sign in")',
        ]
        last_error = ""
        for attempt in range(1, max_attempts + 1):
            page = await ctx.new_page()
            try:
                await page.goto(url, timeout=60000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                filled_email = False
                for sel in EMAIL_SELS:
                    try:
                        el = page.locator(sel).first
                        if await el.is_visible(timeout=1000):
                            await el.click()
                            await el.fill(username)
                            filled_email = True
                            break
                    except Exception:
                        pass
                if not filled_email:
                    await page.keyboard.press("Tab")
                    await page.keyboard.type(username)
                await page.wait_for_timeout(500)
                pass_visible = False
                for sel in PASS_SELS[:2]:
                    try:
                        if await page.locator(sel).first.is_visible(timeout=500):
                            pass_visible = True
                            break
                    except Exception:
                        pass
                if not pass_visible:
                    for sel in ['button:has-text("Next")',
                                'button:has-text("Continue")',
                                'button[type="submit"]']:
                        try:
                            btn = page.locator(sel).first
                            if await btn.is_visible(timeout=1000):
                                await btn.click()
                                await page.wait_for_timeout(2000)
                                break
                        except Exception:
                            pass
                filled_pass = False
                for sel in PASS_SELS:
                    try:
                        el = page.locator(sel).first
                        if await el.is_visible(timeout=2000):
                            await el.click()
                            await el.fill(password)
                            filled_pass = True
                            break
                    except Exception:
                        pass
                if not filled_pass:
                    last_error = "Password field not found"
                    await page.close()
                    await asyncio.sleep(2)
                    continue
                await page.wait_for_timeout(500)
                submitted = False
                for sel in SUBMIT_SELS:
                    try:
                        btn = page.locator(sel).first
                        if await btn.is_visible(timeout=1000):
                            await btn.click()
                            submitted = True
                            break
                    except Exception:
                        pass
                if not submitted:
                    await page.keyboard.press("Enter")
                await page.wait_for_load_state("networkidle", timeout=10000)
                await page.wait_for_timeout(2000)
                failed = False
                for fail_text in ["incorrect password", "invalid credentials",
                                   "wrong password", "login failed"]:
                    try:
                        if await page.locator(f"text={fail_text}").is_visible(timeout=1000):
                            failed = True
                            last_error = fail_text
                            break
                    except Exception:
                        pass
                if failed:
                    await page.close()
                    await asyncio.sleep(2)
                    continue
                shot = await page.screenshot()
                text = await page.inner_text("body")
                self._contexts[domain] = ctx
                return {
                    "url": page.url, "title": await page.title(),
                    "text": text[:4000],
                    "screenshot_b64": base64.b64encode(shot).decode(),
                    "success": True, "attempts": attempt, "logged_in": True
                }
            except Exception as e:
                last_error = str(e)
                await page.close()
                await asyncio.sleep(2 + attempt)
        return {
            "url": url, "success": False, "attempts": max_attempts,
            "error": f"Login failed after {max_attempts} attempts: {last_error}"
        }

    async def navigate_authenticated(self, url: str) -> dict:
        domain = url.split("/")[2] if "//" in url else url
        if domain not in self._contexts:
            return await self.navigate(url)
        ctx  = self._contexts[domain]
        page = await ctx.new_page()
        try:
            await page.goto(url, timeout=30000, wait_until="networkidle")
            await page.wait_for_timeout(2000)
            shot = await page.screenshot(full_page=True)
            text = await page.inner_text("body")
            return {
                "url": page.url, "title": await page.title(),
                "text": text[:6000],
                "screenshot_b64": base64.b64encode(shot).decode(),
                "success": True, "authenticated": True
            }
        except Exception as e:
            return {"url": url, "error": str(e), "success": False}
        finally:
            await page.close()

    async def screenshot(self, url: str) -> str:
        await self._ensure()
        domain = url.split("/")[2] if "//" in url else url
        ctx    = await self._get_context(domain)
        page   = await ctx.new_page()
        await page.goto(url, timeout=30000, wait_until="networkidle")
        await page.wait_for_timeout(3000)
        shot = await page.screenshot(full_page=True)
        await page.close()
        return base64.b64encode(shot).decode()

    async def scrape(self, url: str) -> str:
        await self._ensure()
        domain = url.split("/")[2] if "//" in url else url
        ctx    = await self._get_context(domain)
        page   = await ctx.new_page()
        await page.goto(url, timeout=30000, wait_until="networkidle")
        await page.wait_for_timeout(3000)
        text = await page.inner_text("body")
        await page.close()
        return text

    async def close(self):
        for ctx in self._contexts.values():
            await ctx.close()
        if self._browser: await self._browser.close()
        if self._pw:      await self._pw.stop()
