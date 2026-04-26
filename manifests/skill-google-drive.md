---
name: skill-google-drive
description: Google Drive MCP integration - read/write files, search documents, manage permissions. Escalate to Claude API for Drive operations.
---

# skill-google-drive — Google Drive MCP Integration

**MCP Status:** ✅ Available via claude.ai proxy
**Escalation Required:** YES - Claude API only
**Authentication:** OAuth (use /mcp to authenticate)

---

## What This MCP Can Do

**Read Operations:**
- Search files by name, content, or properties
- Read file content (text, documents, spreadsheets)
- Get file metadata (name, size, modified date, owner)
- List recent files
- Get file permissions/sharing status
- Download file content

**Write Operations:**
- Create new files
- Update existing file content
- Change file metadata
- Manage file permissions (share, unshare)

**Supported File Types:**
- Google Docs (read as markdown/text)
- Google Sheets (read as CSV/structured data)
- Text files (.txt, .md, .csv)
- Code files (.py, .js, .md, etc.)
- PDFs (metadata only, not full text extraction)

---

## When To Use Google Drive MCP vs Manual

**Use Google Drive MCP when:**
- Searching across many files ("find all docs mentioning client X")
- Batch operations (update multiple files, check permissions)
- Automated file creation (generate reports, save logs)
- Content extraction for processing (read doc content for analysis)
- Programmatic file management (organize, rename, share)

**Do it manually when:**
- Single file to view (faster to open in browser)
- Complex document editing with formatting
- Uploading large media files (images, videos)
- Need Drive UI features (comments, suggestions)

**Rule of thumb:** If it involves search, automation, or content extraction → use MCP. If it's visual editing or single file access → manual is faster.

---

## How To Escalate to Claude API

Google Drive MCP is only available when Worker Bee escalates to Claude API.

**Escalation Pattern:**

```python
# In chat(), when user asks about Drive:
if any(word in user_content.lower() for word in ["drive", "document", "sheet", "doc"]):
    if self._needs_drive_access(user_content):
        use_claude_api = True
```

**What Worker Bee Should Say:**

"I'll escalate this to Claude API to access Google Drive.
This requires MCP authentication if not already connected."

---

## Available MCP Tools

**Search & Discovery:**
- `mcp__claude_ai_Google_Drive__search_files` - Search by query
- `mcp__claude_ai_Google_Drive__list_recent_files` - List recent files

**Read:**
- `mcp__claude_ai_Google_Drive__read_file_content` - Get file content
- `mcp__claude_ai_Google_Drive__download_file_content` - Download file
- `mcp__claude_ai_Google_Drive__get_file_metadata` - Get file properties

**Write:**
- `mcp__claude_ai_Google_Drive__create_file` - Create new file
- `mcp__claude_ai_Google_Drive__get_file_permissions` - Check sharing

---

## Common Use Cases

### 1. Search for Client Documents

**User Request:** "Find all documents related to MountainEdge project"

**Worker Bee Action:**
1. Escalate to Claude API
2. Use `search_files` with query: "MountainEdge"
3. Filter results by file type (Docs, Sheets)
4. Present list with links

**Success:** Returns relevant files with last modified dates

---

### 2. Extract Document Content

**User Request:** "What does the contract say about payment terms?"

**Worker Bee Action:**
1. Search for contract document
2. Read content with `read_file_content`
3. Parse payment terms section
4. Summarize findings

**Success:** Accurate extraction of specific content from doc

---

### 3. Create Report File

**User Request:** "Save this analysis as a Google Doc"

**Worker Bee Action:**
1. Format content as markdown
2. Use `create_file` with type: "application/vnd.google-apps.document"
3. Return link to new document

**Success:** New Google Doc created and accessible

---

### 4. Check File Sharing

**User Request:** "Who has access to the pricing spreadsheet?"

**Worker Bee Action:**
1. Search for pricing file
2. Get file ID
3. Use `get_file_permissions` to list collaborators
4. Present sharing status

**Success:** Lists all users with access levels (editor, viewer, etc.)

---

## Integration with Worker Bee Workflows

**Document Research:**
```
User asks about content
  ↓
Search Drive for relevant files
  ↓
Read file content
  ↓
skill-memory.md stores context
  ↓
Answer with source citations
```

**Report Generation:**
```
skill-reporter.md creates report
  ↓
Format as Google Doc
  ↓
skill-google-drive creates file
  ↓
Share link with user
```

---

## What Success Looks Like

**Good:**
- File found in < 3 seconds
- Content readable and properly formatted
- New files created with correct permissions
- Search returns relevant results

**Red Flags:**
- OAuth fails (check /mcp auth)
- Content garbled (encoding issue)
- Files created but not accessible (permission error)
- Search returns nothing when files exist (query syntax)

---

## Failure Modes & Recovery

**Authentication Failed:**
- Re-run /mcp and authenticate Google Drive
- Verify user has Drive access

**File Not Found:**
- Try broader search query
- Check if file name exact or partial
- Verify user has access to file

**Content Read Error:**
- Check file type supported
- Verify file not corrupted
- Try downloading instead of reading

**Permission Denied:**
- User may not own file
- Request access from file owner
- Check if file is publicly accessible

---

## Security & Approval Gates

**Safety Rules:**

1. **Read-Only Preferred** - Default to reading, not writing
2. **Show Before Create** - Preview file content before creating
3. **No Bulk Delete** - Cannot delete files (safety restriction)
4. **Permission Changes Require Approval** - Ask before sharing

**Approval Pattern:**

```
Worker Bee: "I'll create a Google Doc with this content:

[Show preview]

File name: 'Analysis Report - 2026-04-26'
Sharing: Private to you

Approve? (yes/no)"
```

---

## Performance Notes

**Fast (< 2s):**
- List recent files
- Get file metadata
- Search with simple query

**Medium (2-10s):**
- Read small file content
- Create new file
- Search entire Drive

**Slow (10s+):**
- Read large files (> 1MB)
- Complex searches across many files
- Download binary files

**Optimization:**
- Cache file IDs instead of searching repeatedly
- Use metadata instead of full content when possible
- Limit search results to recent files

---

## Pairs With

- **skill-reporter.md** - Generate reports, save to Drive
- **skill-memory.md** - Store Drive file context
- **skill-seo.md** - Analyze site content saved in Docs
- **skill-composer.md** - Draft content before creating Doc

---

## The Bottom Line

Google Drive MCP is Worker Bee's file cabinet.

Use it to search, read, and organize documents programmatically.
Perfect for research, report generation, and content extraction.

When user needs Drive intelligence, escalate to Claude API.
When user needs visual editing, point them to browser.
