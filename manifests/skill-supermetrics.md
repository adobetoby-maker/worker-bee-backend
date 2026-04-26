---
name: skill-supermetrics
description: Supermetrics MCP integration (REQUESTED) - marketing analytics aggregation, data reporting from Google Ads, Facebook, etc. Manual API until MCP available.
---

# skill-supermetrics — Marketing Analytics Integration

**MCP Status:** ❌ **REQUESTED - Not Yet Available**
**Alternative:** Supermetrics API via HTTP calls
**Escalation:** Use httpx for Supermetrics API integration

---

## What Supermetrics MCP Would Do (When Available)

**Data Aggregation:**
- Pull data from Google Ads, Facebook Ads, Instagram, LinkedIn
- Combine multi-channel marketing data
- Historical performance data
- Real-time metrics

**Reporting:**
- Generate cross-platform reports
- Compare channel performance
- ROI analysis across campaigns
- Automated daily/weekly reports

**Supported Platforms:**
- Google Ads
- Facebook/Instagram Ads
- Google Analytics
- LinkedIn Ads
- Twitter/X Ads
- TikTok Ads
- And 100+ more connectors

---

## Current Workaround (Until MCP Available)

**Use Supermetrics API:**

```python
import httpx

headers = {"Authorization": f"Bearer {SUPERMETRICS_API_KEY}"}
async with httpx.AsyncClient() as client:
    r = await client.post("https://api.supermetrics.com/enterprise/v2/query",
        headers=headers,
        json={
            "ds_id": "GA",  # Google Analytics
            "ds_accounts": ["UA-12345678"],
            "ds_metrics": ["ga:sessions", "ga:pageviews"],
            "date_range_type": "last_30_days"
        })
```

**Setup:**
1. Sign up for Supermetrics account
2. Get API key from dashboard
3. Store in .env: `SUPERMETRICS_API_KEY=...`

---

## When To Use Supermetrics vs Manual

**Use Supermetrics integration when:**
- Need cross-platform analytics in one place
- Automated marketing reports
- Historical data analysis
- ROI tracking across channels
- Data export for further analysis

**Do it manually when:**
- Setting up new ad campaigns
- Creative design and copywriting
- Audience targeting configuration
- Initial platform connection setup

---

## Common Use Cases (Future MCP)

### 1. Marketing Performance Report

**User Request:** "How did our ads perform last month?"

**Future Action:**
1. Pull Google Ads spend and conversions
2. Pull Facebook Ads metrics
3. Pull website traffic from Google Analytics
4. Combine into unified report
5. Calculate overall ROI

---

### 2. Cross-Platform Comparison

**User Request:** "Which platform gives better ROI?"

**Future Action:**
1. Get spend from each platform
2. Get conversions from each platform
3. Calculate cost per conversion
4. Rank by performance
5. Recommend budget allocation

---

### 3. Daily Dashboard

**User Request:** "Send me daily marketing stats"

**Future Action:**
1. Pull yesterday's data from all platforms
2. Generate summary (spend, impressions, clicks, conversions)
3. Compare to previous day/week
4. Send via Slack or email

---

## Integration with Worker Bee (Future)

**Marketing Analytics Pipeline:**
```
skill-supermetrics pulls all platform data
  ↓
skill-reporter.md formats into report
  ↓
skill-google-drive.md saves to shared folder
  ↓
skill-slack.md notifies team
```

---

## The Bottom Line

Supermetrics MCP is **requested but not yet available**.

Until MCP exists, use Supermetrics API for multi-platform analytics.
When MCP becomes available, Worker Bee can generate comprehensive marketing reports automatically.

For now: Build Supermetrics API integration when needed for cross-platform reporting.
Essential for Jay's marketing analytics needs.
