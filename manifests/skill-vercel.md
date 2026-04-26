---
name: skill-vercel
description: Vercel MCP integration - deploy projects, check deployment status, view logs, manage domains. Escalate to Claude API for Vercel operations.
---

# skill-vercel — Vercel MCP Integration

**MCP Status:** ✅ Available via claude.ai proxy
**Escalation Required:** YES - Claude API only
**Authentication:** Vercel CLI token required

---

## What This MCP Can Do

**Deployment:**
- Deploy projects to Vercel
- List deployments
- Get deployment status
- Get build logs
- Get runtime logs
- Access deployment URLs

**Project Management:**
- List projects
- Get project details
- Search Vercel documentation

**Domains:**
- Check domain availability and pricing
- (Domain registration requires manual Vercel dashboard)

**Collaboration (Toolbar):**
- List toolbar threads (comments)
- Get thread details
- Reply to threads
- Add reactions
- Edit/resolve threads

---

## When To Use Vercel MCP vs Manual

**Use Vercel MCP when:**
- Automated deployments from code
- Checking deployment status programmatically
- Debugging with build/runtime logs
- Listing all projects across teams
- Monitoring deployment health

**Do it manually when:**
- Initial project setup
- Domain configuration
- Environment variable management
- Analytics review
- Team/billing management

**Rule of thumb:** If it's deployment/logs/status → use MCP. If it's configuration/settings → use dashboard.

---

## How To Escalate to Claude API

**Escalation Pattern:**

```python
if any(word in user_content.lower() for word in ["deploy", "vercel", "deployment"]):
    use_claude_api = True
```

**What Worker Bee Should Say:**

"I'll escalate this to Claude API to access Vercel.
Checking deployment status..."

---

## Available MCP Tools

**Core:**
- `deploy_to_vercel` - Deploy project
- `list_deployments` - List all deployments
- `get_deployment` - Get deployment details
- `list_projects` - List projects
- `get_project` - Get project details
- `list_teams` - List teams

**Logs:**
- `get_deployment_build_logs` - Build logs
- `get_runtime_logs` - Runtime logs

**Access:**
- `get_access_to_vercel_url` - Get deployment URL
- `web_fetch_vercel_url` - Fetch deployment content

**Domains:**
- `check_domain_availability_and_price` - Check domain

**Toolbar (Comments):**
- `list_toolbar_threads` - List comments
- `get_toolbar_thread` - Get thread
- `reply_to_toolbar_thread` - Add reply
- `add_toolbar_reaction` - Add emoji
- `edit_toolbar_message` - Edit message
- `change_toolbar_thread_resolve_status` - Resolve

**Docs:**
- `search_vercel_documentation` - Search docs

---

## Common Use Cases

### 1. Deploy Project

**User Request:** "Deploy the latest changes to Vercel"

**Worker Bee Action:**
1. Verify project is in ~/worker-bee/projects/
2. Use `deploy_to_vercel` with project path
3. Monitor deployment status
4. Return deployment URL

**Success:** Site live at vercel.app URL in < 2 minutes

---

### 2. Check Deployment Status

**User Request:** "Did the MountainEdge deployment succeed?"

**Worker Bee Action:**
1. Use `list_deployments` filtered by project
2. Get latest deployment
3. Check status (READY, ERROR, BUILDING)
4. If error, get build logs

**Success:** Clear status with error details if failed

---

### 3. Debug Build Failure

**User Request:** "Why did the build fail?"

**Worker Bee Action:**
1. Get deployment ID
2. Use `get_deployment_build_logs`
3. Parse error messages
4. Identify root cause
5. Suggest fix

**Success:** Specific error identified (missing env var, build command failed, etc.)

---

### 4. Monitor Runtime Errors

**User Request:** "Are there any errors in production?"

**Worker Bee Action:**
1. Get production deployment ID
2. Use `get_runtime_logs`
3. Filter for ERROR level
4. Present recent errors with timestamps

**Success:** Lists runtime errors with stack traces

---

## Integration with Worker Bee Workflows

**Build Pipeline:**
```
skill-builder.md creates code
  ↓
skill-checker.md validates
  ↓
skill-vercel deploys
  ↓
skill-navigator tests live site
```

**Morning Report:**
```
Check all project deployments
  ↓
Flag any failed builds
  ↓
Include deployment URLs
```

---

## What Success Looks Like

**Good:**
- Deployment completes in < 3 minutes
- Build logs clear and readable
- Runtime logs show normal operation
- URLs accessible immediately

**Red Flags:**
- Build timeout (> 10 min)
- Runtime errors in logs
- Deployment stuck in BUILDING
- URL returns 404

---

## Failure Modes & Recovery

**Build Failed:**
- Check build logs for specific error
- Verify build command in vercel.json
- Check for missing dependencies
- Verify Node version compatibility

**Deployment Timeout:**
- Check for large file builds
- Verify no infinite loops in build script
- Check Vercel status page

**Runtime Errors:**
- Check environment variables set
- Verify API endpoints accessible
- Check for CORS issues
- Review function timeout settings

**Authentication Failed:**
- Re-authenticate with `vercel login`
- Verify token in ~/.vercel

---

## Security & Approval Gates

**Dangerous Operations:**

1. **Production Deploy** - Confirm before deploying to main
2. **Domain Purchase** - Manual only, not via MCP
3. **Project Deletion** - Not available via MCP (safety)

**Approval Pattern:**

```
Worker Bee: "Ready to deploy to production:

Project: mountainedgeplumbing
Branch: main
Changes: [list recent commits]

This will update the live site.
Approve? (yes/no)"
```

---

## Performance Notes

**Fast (< 10s):**
- List deployments
- Get project details
- Check domain availability

**Medium (1-3 min):**
- Deploy small project
- Get build logs

**Slow (3-10 min):**
- Deploy large project
- First-time builds

---

## Pairs With

- **skill-builder.md** - Build before deploy
- **skill-checker.md** - Test before deploy
- **skill-navigator.md** - Test deployed site
- **skill-repair-pipeline.md** - Debug deployment issues

---

## The Bottom Line

Vercel MCP is Worker Bee's deployment engine.

Use it to deploy, monitor, and debug all Vercel projects.
Perfect for automated deployments and health monitoring.

When user needs deployment/logs/status, escalate to Claude API.
When user needs configuration/settings, point to Vercel dashboard.
