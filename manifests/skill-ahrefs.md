---
name: skill-ahrefs
description: Ahrefs MCP integration (REQUESTED) - SEO research, backlink analysis, keyword tracking. Manual API access until MCP available.
---

# skill-ahrefs — SEO Research Integration

**MCP Status:** ❌ **REQUESTED - Not Yet Available**
**Alternative:** Ahrefs API via HTTP calls
**Escalation:** Use httpx for Ahrefs API integration

---

## What Ahrefs MCP Would Do (When Available)

**SEO Research:**
- Domain ranking analysis
- Backlink profile analysis
- Keyword research and difficulty scores
- Competitor analysis
- Content gap analysis

**Keyword Tracking:**
- Track keyword positions
- Get search volume data
- Find keyword opportunities
- Analyze SERP features

**Backlink Analysis:**
- List backlinks to domain
- Analyze link quality
- Find broken backlinks
- Monitor new/lost links

**Site Audit:**
- Technical SEO issues
- Site health score
- Page speed insights
- Mobile usability

---

## Current Workaround (Until MCP Available)

**Use Ahrefs API:**

```python
import httpx

params = {"token": AHREFS_API_TOKEN}
async with httpx.AsyncClient() as client:
    r = await client.get("https://apiv2.ahrefs.com/",
        params={
            "from": "backlinks",
            "target": "mountainedgeplumbing.com",
            "mode": "domain",
            **params
        })
```

**Setup:**
1. Get API token from Ahrefs account
2. Store in .env: `AHREFS_API_TOKEN=...`
3. Note: Ahrefs API requires paid subscription

---

## When To Use Ahrefs vs Manual

**Use Ahrefs integration when:**
- Automated SEO audits for multiple sites
- Tracking keyword rankings over time
- Competitor monitoring
- Backlink quality analysis
- Content opportunity research

**Do it manually when:**
- Initial SEO strategy planning
- Deep competitive research with visualization
- Learning about specific SEO tactics
- Detailed SERP analysis with screenshots

---

## Common Use Cases (Future MCP)

### 1. SEO Audit

**User Request:** "Run an SEO audit on mountainedgeplumbing.com"

**Future Action:**
1. Get domain ranking (DR)
2. Get backlink count and quality
3. Get top ranking keywords
4. Check technical SEO issues
5. Generate report with recommendations

---

### 2. Competitor Analysis

**User Request:** "How does our SEO compare to competitors?"

**Future Action:**
1. List competitors for target keywords
2. Compare domain ratings
3. Analyze their top pages
4. Find keyword gaps
5. Suggest opportunities

---

### 3. Keyword Research

**User Request:** "Find keywords for plumbing services in Idaho"

**Future Action:**
1. Search keywords related to query
2. Get search volume and difficulty
3. Filter by relevance
4. Return top opportunities

---

## Integration with skill-seo.md

**Enhanced SEO Pipeline:**
```
skill-seo.md runs on-page audit
  ↓
skill-ahrefs provides off-page data
  ↓
Combined analysis in report
  ↓
skill-reporter.md generates comprehensive SEO report
```

---

## The Bottom Line

Ahrefs MCP is **requested but not yet available**.

Until MCP exists, use Ahrefs API for SEO research.
When MCP becomes available, Worker Bee can run full SEO audits.

For now: Build Ahrefs API integration when needed for deep SEO work.
Pairs perfectly with skill-seo.md for complete SEO coverage.
