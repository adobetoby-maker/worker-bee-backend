---
name: skill-supabase
description: Supabase MCP integration - database operations, Edge Functions, migrations, project management. Escalate to Claude API for Supabase operations.
---

# skill-supabase — Supabase MCP Integration

**MCP Status:** ✅ Available via claude.ai proxy
**Escalation Required:** YES - Claude API only
**Authentication:** Supabase CLI login required

---

## What This MCP Can Do

**Database Operations:**
- Execute SQL queries (SELECT, INSERT, UPDATE, DELETE)
- List tables and schemas
- Apply migrations
- Generate TypeScript types from schema
- Get database advisors (performance hints)
- View query logs

**Project Management:**
- List organizations and projects
- Get project details and URLs
- Create new projects
- Pause/restore projects
- Get publishable API keys

**Edge Functions:**
- List Edge Functions
- Get function code
- Deploy new functions
- Get function logs

**Branching (Preview):**
- Create database branches
- Merge/rebase branches
- Delete branches
- Reset branch to main

**Documentation:**
- Search Supabase docs
- Get integration examples

---

## When To Use Supabase MCP vs Manual

**Use Supabase MCP when:**
- Running database queries programmatically
- Deploying Edge Functions from code
- Batch database operations
- Checking database health/performance
- Automated migrations
- Querying across multiple projects

**Do it manually when:**
- Visual schema design (Supabase Studio better)
- Complex query building with UI
- Table relationship visualization
- One-off manual data entry
- Authentication UI setup

**Rule of thumb:** If it's code/query execution → use MCP. If it's visual design → use Studio.

---

## How To Escalate to Claude API

Supabase MCP is only available when Worker Bee escalates to Claude API.

**Escalation Pattern:**

```python
# In chat(), when user mentions database:
if any(word in user_content.lower() for word in ["database", "supabase", "sql", "query"]):
    if self._needs_supabase_access(user_content):
        use_claude_api = True
```

**What Worker Bee Should Say:**

"I'll escalate this to Claude API to access Supabase.
This requires Supabase CLI authentication if not already configured."

---

## Available MCP Tools (29 total)

**SQL Execution:**
- `execute_sql` - Run SQL queries
- `get_cost` / `confirm_cost` - Estimate query costs

**Schema:**
- `list_tables` - List all tables
- `list_extensions` - List database extensions
- `generate_typescript_types` - Generate types from schema

**Projects:**
- `list_projects` - List all projects
- `get_project` - Get project details
- `get_project_url` - Get project URL
- `create_project` - Create new project
- `pause_project` / `restore_project` - Manage project state
- `get_publishable_keys` - Get API keys

**Edge Functions:**
- `list_edge_functions` - List functions
- `get_edge_function` - Get function code
- `deploy_edge_function` - Deploy function

**Migrations:**
- `list_migrations` - List migration history
- `apply_migration` - Run migration

**Logs & Monitoring:**
- `get_logs` - View database logs
- `get_advisors` - Get performance suggestions

**Branching:**
- `create_branch` - Create DB branch
- `merge_branch` / `rebase_branch` / `reset_branch` - Branch operations
- `delete_branch` - Remove branch

**Docs:**
- `search_docs` - Search Supabase documentation

---

## Common Use Cases

### 1. Query Database

**User Request:** "How many users are in the database?"

**Worker Bee Action:**
1. Escalate to Claude API
2. Use `execute_sql` with: `SELECT COUNT(*) FROM users`
3. Return count

**Success:** Returns accurate count in < 2 seconds

---

### 2. Deploy Edge Function

**User Request:** "Deploy the email-sender function"

**Worker Bee Action:**
1. Get function code from project
2. Use `deploy_edge_function` with function name and code
3. Verify deployment status
4. Return function URL

**Success:** Function deployed and accessible at edge URL

---

### 3. Database Migration

**User Request:** "Add a column to the users table"

**Worker Bee Action:**
1. Create migration SQL
2. Show migration to user for approval
3. Use `apply_migration` to execute
4. Verify with `list_tables`

**Success:** Schema updated without data loss

---

### 4. Performance Check

**User Request:** "Why is the dashboard query slow?"

**Worker Bee Action:**
1. Use `get_advisors` to check for index suggestions
2. Use `get_logs` to see slow queries
3. Analyze query patterns
4. Recommend optimizations

**Success:** Identifies missing indexes or N+1 queries

---

## Integration with Worker Bee Workflows

**IME Coach Integration:**
```
User uploads medical doc
  ↓
OCR processing
  ↓
skill-supabase stores in database
  ↓
Generate report from stored data
```

**Database Health Monitoring:**
```
Morning report runs
  ↓
skill-supabase checks advisors
  ↓
Flags slow queries or missing indexes
  ↓
Include in daily summary
```

---

## What Success Looks Like

**Good:**
- Queries execute in < 2 seconds
- Migrations apply without errors
- Edge Functions deploy successfully
- Logs readable and helpful

**Red Flags:**
- Query timeout (> 30s)
- Migration fails with data loss
- Function deploy error
- Authentication failure

---

## Failure Modes & Recovery

**Authentication Failed:**
- Run `supabase login` in terminal
- Verify CLI installed: `which supabase`

**Query Timeout:**
- Add LIMIT clause to large queries
- Check for missing indexes
- Use `get_advisors` for optimization hints

**Migration Failed:**
- Check SQL syntax
- Verify no conflicting constraints
- Test on branch before main
- Use `reset_branch` to undo

**Edge Function Error:**
- Check function logs with `get_logs`
- Verify environment variables set
- Test function locally first

---

## Security & Approval Gates

**Dangerous Operations (Always Ask):**

1. **DROP TABLE** - Confirm before executing
2. **DELETE without WHERE** - Verify intent
3. **Production migrations** - Test on branch first
4. **Project pause/delete** - Double-confirm

**Approval Pattern:**

```
Worker Bee: "⚠️ DANGEROUS OPERATION

SQL: DROP TABLE old_users;

This will permanently delete data.
Type 'CONFIRM DELETE' to proceed:"
```

---

## Performance Notes

**Fast (< 2s):**
- Simple SELECT queries
- List tables/functions
- Get project details

**Medium (2-10s):**
- Complex queries with JOINs
- Edge Function deployment
- Migration application

**Slow (10s+):**
- Full table scans
- Large data exports
- Multi-step migrations

**Optimization:**
- Use indexes for frequently queried columns
- Paginate large result sets
- Test queries on branch before production

---

## Pairs With

- **skill-memory.md** - Store query patterns
- **skill-repair-pipeline.md** - Debug database issues
- **skill-reporter.md** - Generate database reports
- **skill-builder.md** - Create database-backed features

---

## The Bottom Line

Supabase MCP is Worker Bee's database brain.

Use it for programmatic database operations, Edge Function deployment, and database health monitoring.

When user needs SQL execution or database management, escalate to Claude API.
When user needs visual schema design, point to Supabase Studio.

Fast, powerful, integrated with the full Worker Bee stack.
