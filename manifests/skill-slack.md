---
name: skill-slack
description: Slack MCP integration (REQUESTED) - send messages, read channels, manage team communication. Manual API access until MCP available.
---

# skill-slack — Team Communication Integration

**MCP Status:** ❌ **REQUESTED - Not Yet Available**
**Alternative:** Slack Web API via HTTP calls
**Escalation:** Use httpx for Slack API integration

---

## What Slack MCP Would Do (When Available)

**Messaging:**
- Send messages to channels/DMs
- Read message history
- Thread replies
- React to messages
- Edit/delete messages

**Channels:**
- List channels
- Create channels
- Invite users
- Archive channels

**Users:**
- List team members
- Get user info
- Set user status
- Check online status

**Files:**
- Upload files
- Share files to channels
- List uploaded files

**Notifications:**
- Send notifications
- @mention users
- Send reminders

---

## Current Workaround (Until MCP Available)

**Use Slack Web API:**

```python
import httpx

headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
async with httpx.AsyncClient() as client:
    r = await client.post("https://slack.com/api/chat.postMessage",
        headers=headers,
        json={"channel": "C12345", "text": "Hello from Worker Bee!"})
```

**Setup:**
1. Create Slack App at api.slack.com
2. Add Bot Token Scopes (chat:write, channels:read, etc.)
3. Install app to workspace
4. Store bot token in .env: `SLACK_BOT_TOKEN=xoxb-...`

---

## When To Use Slack vs Manual

**Use Slack integration when:**
- Automated notifications (deployment alerts, errors)
- Bot responses to team questions
- Scheduled reminders
- Status updates from Worker Bee workflows
- Log aggregation to channel

**Do it manually when:**
- Casual team conversation
- File sharing with comments
- Setting up channels and permissions
- Voice/video calls

---

## Common Use Cases (Future MCP)

### 1. Send Deployment Notification

**Worker Bee Action:**
After successful Vercel deployment:
1. Send message to #deployments channel
2. Include project name, URL, commit message
3. @mention relevant team members

---

### 2. Error Alerting

**Worker Bee Action:**
When build fails:
1. Send message to #alerts channel
2. Include error log snippet
3. Link to full logs

---

### 3. Daily Standup Bot

**Worker Bee Action:**
Every morning:
1. Send reminder to #standup channel
2. Collect responses
3. Summarize for team

---

## Integration with Worker Bee (Future)

**Alert Pipeline:**
```
Monitoring detects issue
  ↓
skill-slack sends alert to #alerts
  ↓
Team member responds with command
  ↓
Worker Bee executes fix
  ↓
skill-slack confirms resolution
```

---

## Security & Approval Gates

**Approval required for:**
1. **Posting to public channels** - Confirm message first
2. **@channel or @here mentions** - Verify necessary
3. **DMs to users** - Ensure appropriate

**Approval Pattern:**

```
Worker Bee: "Ready to send Slack message:

Channel: #general
Message: "Deployment complete! mountainedgeplumbing.com is live."

Send? (yes/no)"
```

---

## The Bottom Line

Slack MCP is **requested but not yet available**.

Until MCP exists, use Slack Web API for notifications.
When MCP becomes available, Worker Bee can be a full Slack bot.

For now: Build Slack API integration when needed for alerts/notifications.
