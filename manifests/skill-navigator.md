# Skill: Browser Navigation & Testing

**Purpose:** Automate browser interactions for testing, data extraction, and workflow automation. Navigate websites systematically and reliably.

**When to use:** Web testing, form automation, data scraping, UI validation, automated workflows.

---

## Core Approach: Ref-Based Element Selection

Use accessibility tree snapshots with refs for deterministic element selection. This is more reliable than CSS selectors or XPath for AI-driven automation.

**Why this matters:**
- Accessibility tree focuses on interactive elements
- Refs (`@e1`, `@e2`) are stable identifiers
- Reduces brittleness from DOM changes
- Works with complex SPAs

---

## When to Use This Skill vs Built-in Browser Tool

**Use skill-navigator (agent-browser approach) when:**
- Automating multi-step workflows
- Need deterministic element selection
- Performance is critical
- Working with complex SPAs
- Need session isolation
- Building reusable automation scripts

**Use built-in browser tool when:**
- Need screenshots/PDFs for analysis
- Visual inspection required
- Simple one-off tasks
- Browser extension integration needed

---

## Core Workflow

```
1. Navigate to page
   ↓
2. Take snapshot (get accessibility tree with refs)
   ↓
3. Parse snapshot JSON to identify elements
   ↓
4. Interact with elements using refs (@e1, @e2, etc.)
   ↓
5. Re-snapshot after page changes
   ↓
6. Repeat steps 3-5 as needed
```

### Example Flow

```bash
# 1. Navigate and snapshot
browser.open("https://example.com")
snapshot = browser.snapshot(interactive=True, json=True)

# 2. Parse refs from JSON, identify elements
# Example: search_box = @e3, submit_button = @e5

# 3. Interact with elements
browser.fill("@e3", "search query")
browser.click("@e5")

# 4. Re-snapshot after page changes
snapshot = browser.snapshot(interactive=True, json=True)

# 5. Extract data
result_text = browser.get_text("@e7")
```

---

## Key Commands Reference

### Navigation

```python
browser.open(url)              # Navigate to URL
browser.back()                 # Go back
browser.forward()              # Go forward
browser.reload()               # Refresh page
browser.close()                # Close browser
```

### Snapshot (Most Important)

**Always use `-i` (interactive) and `--json` flags:**

```python
# Get interactive elements in JSON format
snapshot = browser.snapshot(interactive=True, json=True)

# With options:
snapshot = browser.snapshot(
    interactive=True,     # Focus on interactive elements only
    compact=True,         # Reduce verbosity
    depth=5,             # Limit DOM depth
    json=True,           # JSON output for parsing
    scope="#main"        # Limit to specific selector (optional)
)
```

**Snapshot Output Format:**
```json
{
  "success": true,
  "data": {
    "snapshot": "...",
    "refs": {
      "e1": {"role": "heading", "name": "Example Domain"},
      "e2": {"role": "button", "name": "Submit"},
      "e3": {"role": "textbox", "name": "Email"},
      "e4": {"role": "link", "name": "More information..."}
    }
  }
}
```

### Interactions (Ref-Based)

**All interactions use refs from snapshot:**

```python
browser.click("@e2")                  # Click element
browser.fill("@e3", "text")          # Fill input field
browser.type("@e3", "text")          # Type (slower, character by character)
browser.hover("@e4")                 # Hover over element
browser.check("@e5")                 # Check checkbox
browser.uncheck("@e5")               # Uncheck checkbox
browser.select("@e6", "value")       # Select dropdown option
browser.press("Enter")               # Press keyboard key
browser.scroll("down", 500)          # Scroll page
browser.drag("@e7", "@e8")           # Drag element to another
```

### Get Information

```python
# Extract data from elements
text = browser.get_text("@e1", json=True)
html = browser.get_html("@e2", json=True)
value = browser.get_value("@e3", json=True)
href = browser.get_attr("@e4", "href", json=True)

# Get page information
title = browser.get_title(json=True)
url = browser.get_url(json=True)
count = browser.get_count(".item", json=True)
```

### Check State

```python
# Verify element states
is_visible = browser.is_visible("@e2", json=True)
is_enabled = browser.is_enabled("@e3", json=True)
is_checked = browser.is_checked("@e4", json=True)
```

### Wait for Elements

```python
# Wait for element to appear
browser.wait("@e2")

# Wait for specific time
browser.wait(1000)  # milliseconds

# Wait for text to appear
browser.wait(text="Welcome")

# Wait for URL pattern
browser.wait(url="**/dashboard")

# Wait for network idle
browser.wait(load="networkidle")

# Wait for custom condition
browser.wait(fn="window.ready === true")
```

---

## Session Management (Isolated Browsers)

Use sessions to maintain separate browser contexts:

```python
# Create separate sessions for different users/contexts
browser.session("admin").open("https://site.com")
browser.session("user").open("https://site.com")

# List active sessions
browser.session_list()

# Or use environment variable
# AGENT_BROWSER_SESSION=admin browser.open(...)
```

**Use cases:**
- Testing with multiple user accounts
- Comparing logged-in vs logged-out states
- Isolating test data

---

## State Persistence (Skip Login Flows)

Save and load browser state (cookies, localStorage):

```python
# After logging in, save state
browser.state_save("auth.json")

# In future sessions, load state
browser.state_load("auth.json")
# Now you're logged in without repeating login flow
```

**Use cases:**
- Skip repetitive login steps
- Maintain authentication across test runs
- Save user preferences/settings

---

## Screenshots & PDFs

```python
# Take screenshot
browser.screenshot("page.png")

# Full page screenshot
browser.screenshot("page.png", full=True)

# Generate PDF
browser.pdf("page.pdf")
```

---

## Network Control

```python
# Block ads or trackers
browser.network_route("**/ads/*", abort=True)

# Mock API responses
browser.network_route("**/api/*", body='{"data": "mocked"}')

# View network requests
browser.network_requests(filter="api")
```

---

## Cookies & Storage

```python
# Get all cookies
cookies = browser.cookies()

# Set cookie
browser.cookies_set("name", "value")

# Get localStorage value
value = browser.storage_local("key")

# Set localStorage value
browser.storage_local_set("key", "value")
```

---

## Tabs & Frames

```python
# Open new tab
browser.tab_new("https://example.com")

# Switch to tab
browser.tab(2)

# Switch to iframe
browser.frame("@e5")

# Back to main frame
browser.frame("main")
```

---

## Best Practices

### 1. Always Use `-i` Flag (Interactive Elements Only)

Focus on interactive elements to reduce noise:
```python
snapshot = browser.snapshot(interactive=True, json=True)
```

### 2. Always Use `--json` (Easier to Parse)

JSON output is structured and easier to work with:
```python
result = browser.get_text("@e1", json=True)
```

### 3. Wait for Stability

After navigation or interactions, wait for network idle:
```python
browser.open(url)
browser.wait(load="networkidle")
snapshot = browser.snapshot(interactive=True, json=True)
```

### 4. Save Auth State (Skip Login Flows)

Don't repeat login steps:
```python
# First time: login and save
browser.open("https://app.example.com/login")
browser.fill("@email", "user@example.com")
browser.fill("@password", "password123")
browser.click("@submit")
browser.wait(load="networkidle")
browser.state_save("auth.json")

# Subsequent runs: just load
browser.open("https://app.example.com")
browser.state_load("auth.json")
# Now logged in
```

### 5. Use Sessions for Isolation

Isolate different browser contexts:
```python
# Admin session
browser.session("admin").open(url)
browser.session("admin").state_load("admin-auth.json")

# User session (simultaneous)
browser.session("user").open(url)
browser.session("user").state_load("user-auth.json")
```

### 6. Use `--headed` for Debugging

See what's happening when developing automation:
```python
browser.open(url, headed=True)
```

### 7. Re-Snapshot After Changes

Always take a fresh snapshot after page changes:
```python
browser.click("@e2")  # Click triggers page update
browser.wait(load="networkidle")
snapshot = browser.snapshot(interactive=True, json=True)
# Now refs are fresh
```

---

## Common Automation Patterns

### Pattern 1: Search and Extract

```python
# Navigate to search page
browser.open("https://www.google.com")
browser.wait(load="networkidle")

# Get snapshot, find search box
snapshot = browser.snapshot(interactive=True, json=True)
# Parse JSON to find search box ref (e.g., @e1)

# Perform search
browser.fill("@e1", "AI agents")
browser.press("Enter")
browser.wait(load="networkidle")

# Get results
snapshot = browser.snapshot(interactive=True, json=True)
# Parse JSON to find result refs

# Extract data
for ref in result_refs:
    text = browser.get_text(ref, json=True)
    link = browser.get_attr(ref, "href", json=True)
    print(f"{text}: {link}")
```

### Pattern 2: Form Submission

```python
browser.open("https://example.com/contact")
browser.wait(load="networkidle")

snapshot = browser.snapshot(interactive=True, json=True)
# Identify form field refs

# Fill form
browser.fill("@name", "John Doe")
browser.fill("@email", "john@example.com")
browser.fill("@message", "Hello, this is a test message.")
browser.click("@submit")

# Wait for confirmation
browser.wait(text="Thank you")
```

### Pattern 3: Multi-Page Workflow

```python
# Login
browser.open("https://app.example.com/login")
browser.state_load("auth.json")  # Skip login if have state

# Navigate to dashboard
browser.open("https://app.example.com/dashboard")
browser.wait(load="networkidle")

# Click on specific item
snapshot = browser.snapshot(interactive=True, json=True)
browser.click("@item3")

# Wait for detail page
browser.wait(load="networkidle")

# Extract details
snapshot = browser.snapshot(interactive=True, json=True)
details = browser.get_text("@details", json=True)
```

### Pattern 4: Data Scraping with Pagination

```python
browser.open(url)
all_data = []

while True:
    browser.wait(load="networkidle")
    snapshot = browser.snapshot(interactive=True, json=True)
    
    # Extract data from current page
    for item_ref in item_refs:
        data = browser.get_text(item_ref, json=True)
        all_data.append(data)
    
    # Check for next page button
    if next_button_exists:
        browser.click("@next")
    else:
        break

print(f"Scraped {len(all_data)} items")
```

---

## Troubleshooting

### Element Not Found

**Problem:** Ref not found or element not visible
**Solution:**
1. Take a fresh snapshot
2. Check if page has loaded (wait for networkidle)
3. Check if element is in a different frame
4. Use `--scope` to limit snapshot to specific area

### Action Fails

**Problem:** Click or fill doesn't work
**Solution:**
1. Use `browser.is_visible("@ref")` to check visibility
2. Use `browser.is_enabled("@ref")` to check if enabled
3. Wait for element: `browser.wait("@ref")`
4. Try `browser.hover("@ref")` before clicking

### Slow Performance

**Problem:** Automation is too slow
**Solution:**
1. Use `compact=True` in snapshots
2. Limit snapshot depth: `depth=5`
3. Use `scope="#container"` to focus on specific area
4. Reduce unnecessary waits

### State Not Persisting

**Problem:** State load doesn't work
**Solution:**
1. Ensure you're on the same domain
2. Check if cookies have expiration
3. Verify localStorage is supported
4. Load state AFTER navigating to the site

---

## Integration with Worker Bee Testing Pipeline

When testing Lovable.ai sites or Worker Bee projects:

1. **Navigate to preview URL**
   ```python
   browser.open("https://preview.tobyandertonmd.com:5173")
   ```

2. **Take snapshot to understand UI**
   ```python
   snapshot = browser.snapshot(interactive=True, json=True)
   ```

3. **Interact with UI elements**
   ```python
   browser.click("@nav_button")
   browser.fill("@search_input", "test query")
   ```

4. **Verify expected behavior**
   ```python
   result = browser.get_text("@result", json=True)
   assert "Expected Text" in result
   ```

5. **Take screenshot for documentation**
   ```python
   browser.screenshot("test-result.png")
   ```

6. **Report findings to skill-reporter.md**

---

## Quick Reference

| Task | Command |
|------|---------|
| Navigate | `browser.open(url)` |
| Get snapshot | `browser.snapshot(interactive=True, json=True)` |
| Click element | `browser.click("@e2")` |
| Fill input | `browser.fill("@e3", "text")` |
| Get text | `browser.get_text("@e1", json=True)` |
| Wait for element | `browser.wait("@e2")` |
| Wait for network | `browser.wait(load="networkidle")` |
| Take screenshot | `browser.screenshot("page.png")` |
| Save state | `browser.state_save("auth.json")` |
| Load state | `browser.state_load("auth.json")` |
| New session | `browser.session("name").open(url)` |

---

**Remember:** Ref-based selection is more reliable than CSS selectors. Always snapshot, parse refs, then interact.
