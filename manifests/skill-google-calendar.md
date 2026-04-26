---
name: skill-google-calendar
description: Google Calendar MCP integration (REQUESTED) - event management, scheduling automation, availability checking. Manual Google Calendar API until MCP available.
---

# skill-google-calendar — Calendar Integration

**MCP Status:** ❌ **REQUESTED - Not Yet Available**
**Alternative:** Google Calendar API via Google API Client
**Escalation:** Use google-api-python-client for Calendar integration

---

## What Google Calendar MCP Would Do (When Available)

**Event Management:**
- Create events
- Update/delete events
- List upcoming events
- Search events
- Set reminders

**Availability:**
- Check free/busy times
- Find meeting slots
- Suggest best meeting times
- Block time for focus work

**Calendar Management:**
- List all calendars
- Create new calendars
- Share calendars
- Set working hours

**Integrations:**
- Sync with Calendly events
- Add events from Gmail
- Meeting link generation (Google Meet)
- Timezone handling

---

## Current Workaround (Until MCP Available)

**Use Google Calendar API:**

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('token.json')
service = build('calendar', 'v3', credentials=creds)

# List upcoming events
events = service.events().list(
    calendarId='primary',
    timeMin='2026-04-26T00:00:00Z',
    maxResults=10,
    singleEvents=True,
    orderBy='startTime'
).execute()
```

**Setup:**
1. Enable Google Calendar API in Google Cloud Console
2. Download OAuth credentials
3. Authenticate and save token.json
4. Store in ~/worker-bee/.google/

---

## When To Use Google Calendar vs Manual

**Use Calendar integration when:**
- Automated event creation (e.g., from form submissions)
- Checking availability programmatically
- Bulk event management
- Syncing events across systems
- Generating calendar-based reports

**Do it manually when:**
- Casual event creation
- Rescheduling with attendees via UI
- Color-coding and visual organization
- Setting up recurring patterns with exceptions

---

## Common Use Cases (Future MCP)

### 1. Check Availability

**User Request:** "Am I free Thursday afternoon?"

**Future Action:**
1. Get events for Thursday
2. Filter afternoon (12pm-5pm)
3. Find gaps in schedule
4. Return: "Free from 2-4pm"

---

### 2. Schedule Meeting

**User Request:** "Schedule 1-hour meeting with Jay next week"

**Future Action:**
1. Check Jay's calendar (if shared)
2. Find mutual availability
3. Create event
4. Send invite to Jay

---

### 3. Daily Schedule Summary

**User Request:** "What's on my calendar today?"

**Future Action:**
1. List today's events
2. Format with times and titles
3. Include meeting links
4. Note any conflicts

---

### 4. Block Focus Time

**User Request:** "Block every morning 9-11am for deep work"

**Future Action:**
1. Create recurring "Focus Time" events
2. Set as busy
3. Decline meeting requests during this time

---

## Integration with Worker Bee (Future)

**Scheduling Automation:**
```
Gmail: Client requests meeting
  ↓
skill-google-calendar checks availability
  ↓
skill-calendly creates booking link (or)
skill-google-calendar creates event directly
  ↓
skill-gmail sends confirmation with details
```

**Morning Report Integration:**
```
Morning report runs
  ↓
skill-google-calendar lists today's events
  ↓
Include in daily summary
  ↓
Highlight conflicts or prep needed
```

---

## What Success Looks Like (Future)

**Good:**
- Events created with correct timezone
- Availability accurately reflects calendar
- Meeting links included automatically
- Reminders set appropriately

**Red Flags:**
- Timezone conversion errors
- Double-booked slots
- Missing attendees
- OAuth token expired

---

## Failure Modes & Recovery (Future)

**OAuth Expired:**
- Re-run authentication flow
- Refresh token automatically if possible
- Notify user if manual auth needed

**Event Not Found:**
- Check calendar ID correct
- Verify event not deleted
- Search by different parameters

**Availability Mismatch:**
- Refresh calendar data
- Check for syncing delays
- Verify correct calendar being checked

---

## Security & Approval Gates

**Approval required for:**
1. **Creating events on someone else's calendar** - Verify permission
2. **Deleting events with attendees** - Confirm cancellation
3. **Sharing calendar** - Verify recipient
4. **Bulk operations** - Show preview first

**Approval Pattern:**

```
Worker Bee: "Ready to create calendar event:

Title: Client Meeting - Jay & MountainEdge
Date: Thursday, May 1, 2026
Time: 2:00 PM - 3:00 PM
Attendees: jay@example.com

Create event? (yes/no)"
```

---

## Pairs With

- **skill-gmail.md** - Send meeting invites
- **skill-calendly.md** - Sync scheduled events
- **skill-slack.md** - Send meeting reminders
- **skill-google-drive.md** - Attach meeting materials

---

## The Bottom Line

Google Calendar MCP is **requested but not yet available**.

Until MCP exists, use Google Calendar API directly.
When MCP becomes available, Worker Bee can fully automate scheduling.

For now: Build Google Calendar API integration when needed.
Critical for Jay's appointment management and Worker Bee's daily reports.
