---
name: skill-calendly
description: Calendly MCP integration (REQUESTED) - scheduling automation, event management, availability checking. Manual API access until MCP available.
---

# skill-calendly — Scheduling Integration

**MCP Status:** ❌ **REQUESTED - Not Yet Available**
**Alternative:** Calendly REST API via HTTP calls
**Escalation:** Use httpx for Calendly API integration

---

## What Calendly MCP Would Do (When Available)

**Scheduling:**
- List scheduled events
- Get event details
- Cancel/reschedule events
- Check availability
- Create event types

**User Management:**
- Get user info
- List team members
- Manage scheduling rules

**Webhooks:**
- Handle event created/canceled notifications
- Trigger workflows on bookings

---

## Current Workaround (Until MCP Available)

**Use Calendly REST API:**

```python
import httpx

headers = {"Authorization": f"Bearer {CALENDLY_TOKEN}"}
async with httpx.AsyncClient() as client:
    r = await client.get("https://api.calendly.com/scheduled_events", headers=headers)
    events = r.json()
```

**Setup:**
1. Get API token from Calendly settings
2. Store in .env: `CALENDLY_TOKEN=...`
3. Create helper in agent/tools/calendly_tool.py

---

## When To Use Calendly vs Manual

**Use Calendly integration when:**
- Need to check upcoming appointments programmatically
- Automated scheduling workflows
- Event notifications to other systems
- Bulk event management
- Availability checking for booking forms

**Do it manually when:**
- Setting up new event types
- Configuring calendar connections
- Customizing booking pages
- Managing team routing logic

---

## Common Use Cases (Future MCP)

### 1. List Upcoming Appointments

**User Request:** "What meetings do I have this week?"

**Future Action:**
1. Get scheduled events for user
2. Filter by date range (this week)
3. Return list with times and invitees

---

### 2. Check Availability

**User Request:** "Am I free tomorrow at 2pm?"

**Future Action:**
1. Get availability for time slot
2. Check for conflicts
3. Return: available/busy

---

### 3. Cancel Meeting

**User Request:** "Cancel my 3pm meeting with John"

**Future Action:**
1. Search events for "John" at 3pm
2. Get event UUID
3. Cancel event
4. Send cancellation notification

---

## Integration with Worker Bee (Future)

**Scheduling Pipeline:**
```
Gmail: Client requests meeting
  ↓
skill-calendly checks availability
  ↓
Creates event
  ↓
skill-gmail sends confirmation
  ↓
skill-google-calendar syncs to Google Calendar
```

---

## The Bottom Line

Calendly MCP is **requested but not yet available**.

Until MCP exists, use Calendly REST API for automation.
When MCP becomes available, it will enable full scheduling automation.

For now: Build Calendly API integration when needed.
