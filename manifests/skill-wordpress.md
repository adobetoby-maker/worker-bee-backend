---
name: skill-wordpress
description: WordPress.com MCP integration - manage posts, pages, media. Escalate to Claude API. IMPORTANT: Only works with WordPress.com, not self-hosted WordPress.org sites.
---

# skill-wordpress — WordPress.com MCP Integration

**MCP Status:** ✅ Available via claude.ai proxy
**Escalation Required:** YES - Claude API only
**Authentication:** OAuth (use /mcp to authenticate)

**⚠️ CRITICAL LIMITATION:** This MCP only works with **WordPress.com** hosted sites.
Does NOT work with self-hosted **WordPress.org** installations.

---

## What This MCP Can Do

**Expected capabilities (post-authentication):**
- List posts and pages
- Read post content
- Create/edit posts
- Manage categories and tags
- Upload media
- Update SEO metadata
- Manage comments

**Current Status:** Requires OAuth authentication to activate tools.
Use `/mcp` command and select "claude.ai WordPress.com" to authenticate.

---

## When To Use WordPress MCP vs Manual

**Use WordPress MCP when:**
- Bulk post operations (update multiple posts)
- SEO audit across all posts
- Content extraction for analysis
- Automated post creation from templates
- Programmatic content updates

**Do it manually when:**
- Visual post editing with blocks
- Image placement and formatting
- Theme customization
- Plugin configuration
- One-off post creation

**Rule of thumb:** If it's content automation/analysis → use MCP. If it's visual editing → use WordPress dashboard.

---

## How To Escalate to Claude API

**Escalation Pattern:**

```python
if "wordpress" in user_content.lower() or "blog" in user_content.lower():
    # Check if user's site is WordPress.com
    if self._is_wordpress_com_site(site_url):
        use_claude_api = True
    else:
        return "This site appears to be self-hosted WordPress.org. " \
               "WordPress MCP only works with WordPress.com sites. " \
               "For self-hosted sites, use WordPress REST API directly."
```

---

## Jay's Sites - Important Check

**Before using WordPress MCP with Jay's sites:**

1. Verify hosting platform:
   - WordPress.com → MCP works ✅
   - WordPress.org (self-hosted) → MCP doesn't work ❌

2. If self-hosted, use WordPress REST API instead:
   - Authentication: Application Password
   - Endpoint: `https://site.com/wp-json/wp/v2/`
   - No MCP needed, direct HTTP calls

**Action Required:** Add Jay's sites to site registry with platform info.

---

## Authentication Flow

**First-time setup:**

1. User (or you) runs `/mcp` command
2. Select "claude.ai WordPress.com"
3. Browser opens for WordPress.com OAuth
4. User authorizes Worker Bee access
5. MCP tools become available

**Subsequent uses:** Authentication persists across sessions.

---

## Common Use Cases (Post-Auth)

### 1. SEO Audit

**User Request:** "Audit all blog posts for missing meta descriptions"

**Worker Bee Action:**
1. List all posts
2. Check each for meta description
3. Flag missing or short descriptions
4. Generate suggestions

---

### 2. Bulk Content Update

**User Request:** "Add a disclaimer to all posts from 2024"

**Worker Bee Action:**
1. List posts filtered by date
2. For each post, append disclaimer
3. Update via API
4. Return count of updated posts

---

### 3. Content Extraction

**User Request:** "What topics do we write about most?"

**Worker Bee Action:**
1. Read all post content
2. Extract categories and tags
3. Analyze keyword frequency
4. Present topic distribution

---

## Integration with Worker Bee

**Works with:**
- **skill-seo.md** - SEO audits on WordPress content
- **skill-reporter.md** - Content performance reports
- **skill-composer.md** - Draft blog posts

---

## What Success Looks Like

**Good:**
- Posts readable and editable
- SEO metadata accessible
- Bulk operations complete without errors
- OAuth authentication persists

**Red Flags:**
- 403 Forbidden (wrong site type)
- OAuth fails repeatedly
- Content updates don't appear on site
- Rate limits hit frequently

---

## Failure Modes & Recovery

**403 Forbidden:**
- Site is likely WordPress.org, not .com
- Switch to REST API approach
- Document in site registry

**OAuth Expired:**
- Re-run `/mcp` authentication
- Check WordPress.com account access

**Rate Limit:**
- WordPress.com has API rate limits
- Add delays between bulk operations
- Process in smaller batches

---

## The Bottom Line

WordPress MCP is powerful BUT limited to WordPress.com hosted sites.

For Jay's sites: **Check hosting platform first.**
- WordPress.com → use this MCP
- Self-hosted → use REST API instead

When in doubt, test with a simple post list call.
If it fails with 403, it's the wrong platform.
