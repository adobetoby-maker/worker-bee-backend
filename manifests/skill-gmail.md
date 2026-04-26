---
name: skill-gmail
description: Gmail MCP integration - read threads, create drafts, manage labels, search emails. Escalate to Claude API for email operations.
---

# skill-gmail — Gmail MCP Integration

**MCP Status:** ✅ Available via claude.ai proxy
**Escalation Required:** YES - Claude API only
**Authentication:** OAuth (use /mcp to authenticate)

---

## What This MCP Can Do

**Read Operations:**
- Search email threads by query
- Get specific thread with all messages
- List drafts
- List and manage labels

**Write Operations:**
- Create email drafts (NOT send directly)
- Apply labels to messages/threads
- Remove labels from messages/threads
- Create new labels

**Critical Limitation:** Can create drafts but CANNOT send emails directly
Sending requires user approval through Gmail interface

---

## When To Use Gmail MCP vs Manual

**Use Gmail MCP when:**
- Need to search across large email history ("find all emails from client X")
- Creating multiple drafts in batch
- Managing email organization (labels, threading)
- Reading email content to extract information
- Checking for specific email patterns or tracking conversations

**Do it manually when:**
- Single email to read (faster to just open Gmail)
- Sending is required (MCP can't send, only draft)
- Complex email formatting with images/attachments
- Need immediate send confirmation

**Rule of thumb:** If it involves searching, organizing, or reading multiple emails → use MCP. If it's one email to write and send → manual is faster.

---

## How To Escalate to Claude API

Gmail MCP is only available when Worker Bee escalates to Claude API.
phi4, deepseek, and qwen cannot access Gmail directly.

**Escalation Pattern:**

```python
# In chat(), when user asks about email:
if "email" in user_content.lower() or "gmail" in user_content.lower():
    if self._needs_gmail_access(user_content):
        # Force Claude API escalation
        use_claude_api = True
```

**What Worker Bee Should Say:**

"I'll escalate this to Claude API to access Gmail.
This requires MCP authentication if not already connected."

**Authentication Check:**

First time using Gmail MCP in a session requires OAuth:
1. Claude API will prompt for /mcp authentication
2. User selects "claude.ai Gmail"  
3. Completes OAuth flow in browser
4. MCP tools become available

---

## Available MCP Tools

**Search & Read:**
- `mcp__claude_ai_Gmail__search_threads` - Search by query string
- `mcp__claude_ai_Gmail__get_thread` - Get full thread by ID

**Drafts:**
- `mcp__claude_ai_Gmail__list_drafts` - List all draft emails
- `mcp__claude_ai_Gmail__create_draft` - Create new draft

**Labels:**
- `mcp__claude_ai_Gmail__list_labels` - List all labels
- `mcp__claude_ai_Gmail__create_label` - Create new label
- `mcp__claude_ai_Gmail__label_message` - Apply label to message
- `mcp__claude_ai_Gmail__label_thread` - Apply label to thread
- `mcp__claude_ai_Gmail__unlabel_message` - Remove label from message
- `mcp__claude_ai_Gmail__unlabel_thread` - Remove label from thread

---

## Common Use Cases

### 1. Search for Specific Emails

**User Request:** "Find all emails from jay@example.com in the last month"

**Worker Bee Action:**
1. Escalate to Claude API
2. Use `search_threads` with query: `from:jay@example.com newer_than:1m`
3. Parse results and present summary

**Success:** Returns list of threads with subjects and snippets

---

### 2. Create Email Draft

**User Request:** "Draft an email to the dev team about the deployment"

**Worker Bee Action:**
1. Use skill-composer.md to analyze intent
2. Use skill-drafter.md to write email
3. Escalate to Claude API
4. Use `create_draft` to save in Gmail
5. Return draft link for user to review and send

**Success:** Draft appears in Gmail drafts folder, ready to send

---

### 3. Organize Emails by Label

**User Request:** "Label all emails from clients with 'Client-Communication'"

**Worker Bee Action:**
1. Check if label exists with `list_labels`
2. Create label if needed with `create_label`
3. Search for client emails
4. Apply label to each thread with `label_thread`

**Success:** Emails organized under new label in Gmail

---

### 4. Email Research

**User Request:** "What did the client say about pricing in our last email thread?"

**Worker Bee Action:**
1. Search threads with client email + "pricing"
2. Get full thread content
3. Extract pricing discussion
4. Summarize findings

**Success:** Accurate summary of pricing conversation from email history

---

## Integration with Email Pipeline

Gmail MCP integrates with Worker Bee's email pipeline skills:

```
skill-composer.md (deepseek)
  ↓ analyzes intent, creates brief
skill-drafter.md (qwen)
  ↓ writes email from brief
skill-refiner.md (qwen)
  ↓ polishes based on feedback
skill-gmail.md (ESCALATE TO CLAUDE)
  ↓ saves draft to Gmail
skill-sender.md
  ↓ USER APPROVAL GATE → manual send
```

**Key Point:** Gmail MCP handles draft creation, but sending remains manual approval gate.

---

## What Success Looks Like

**Good:**
- Draft appears in Gmail within 5 seconds
- Search returns relevant threads accurately
- Labels apply correctly to target emails
- Thread content is fully readable and parseable

**Red Flags:**
- OAuth authentication fails (check /mcp setup)
- Search returns empty when emails exist (query syntax wrong)
- Draft created but formatting broken (HTML escaping issue)
- Label operations fail silently (API rate limit hit)

---

## Failure Modes & Recovery

**Authentication Failed:**
- Re-run /mcp and complete OAuth flow
- Check that user has Gmail access enabled
- Verify API credentials in Claude.ai settings

**Search Returns Nothing:**
- Verify query syntax (Gmail search operators)
- Check date ranges (newer_than, older_than)
- Simplify query and retry

**Draft Creation Fails:**
- Check email content for special characters
- Verify recipient email format
- Reduce email size if very large

**Rate Limit Hit:**
- Wait 60 seconds and retry
- Batch operations instead of individual calls
- Inform user of Gmail API rate limits

---

## Security & Approval Gates

**Gmail MCP respects these safety rules:**

1. **Read-Only by Default** - Prefer searching/reading over writing
2. **Draft Before Send** - NEVER attempt to send directly
3. **User Approval Required** - All draft creation shown to user first
4. **No Bulk Deletion** - MCP cannot delete emails (read-only safety)

**Approval Gate Pattern:**

```
Worker Bee: "I'll create a draft with this content:

[Show email preview]

Approve draft creation? (yes/no)"

User: "yes"

Worker Bee: [Escalates to Claude API, creates draft]
"Draft created in Gmail. Review and send manually."
```

---

## Performance Notes

**Fast Operations (< 2s):**
- List labels
- List recent drafts
- Search with simple query

**Medium Operations (2-10s):**
- Get full thread (depends on message count)
- Search with complex query
- Create draft

**Slow Operations (10s+):**
- Search across entire email history
- Get threads with many messages
- Batch label operations

**Optimization Tips:**
- Limit search results with date ranges
- Use specific queries instead of broad searches
- Cache label list instead of fetching repeatedly

---

## Pairs With

- **skill-composer.md** - Analyzes email intent before drafting
- **skill-drafter.md** - Writes email content
- **skill-refiner.md** - Polishes email before saving
- **skill-sender.md** - Manages approval gate for sending
- **skill-memory.md** - Stores email context for future reference

---

## Morning Report Integration

Include in daily morning report:

```
📧 Gmail Status
- Unread threads: [count]
- Pending drafts: [count]  
- Recent client emails: [if any urgent]
```

Use search_threads to gather this data when generating morning report.

---

## The Bottom Line

Gmail MCP is Worker Bee's bridge to email management.
It handles everything except the actual send button.

When user needs email intelligence (search, organize, track),
escalate to Claude API and use Gmail MCP.

When user needs to send, create draft via MCP then hand
the send button to the user for approval.

Fast, safe, integrated with the email pipeline.
