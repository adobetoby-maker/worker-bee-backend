---
name: skill-memory
description: Final step in Tester pipeline. Stores results with delta comparison. The learning layer.
---

# skill-memory — Observation Storage and Learning

**Called by:** skill-reporter (tester), also called after repair verifier
**Model:** Uses ChromaDB directly via memory.py

## Announce At Start

"I am using skill-memory to store and compare test results."

## Follow runner-narrator.md for all status emissions.

## Step 1 — Query Before Storing

Before writing anything, query ChromaDB:
```
Query: "[site_name] test results"
Limit: 1 (most recent)
```
Emit: [MEMORY:QUERY] checking previous results for [site]

## Step 2 — Compare

Compare current results to previous.
Build the delta record:

```json
{
  "site": "site_name",
  "test_date": "ISO timestamp",
  "journey_type": "CONVERSION/AUTH/etc",
  "overall": "PASS/PARTIAL/FAIL",
  "steps_passed": N,
  "steps_failed": N,
  "delta_from_previous": {
    "classification": "IMPROVEMENT/REGRESSION/NOVEL/UNCHANGED",
    "specific_changes": ["what changed item 1", "what changed item 2"],
    "human_observation": "one sentence for voice.md"
  },
  "fragile_points_confirmed": ["list of known fragile points that failed"],
  "new_failures": ["failures not in site registry — these need registry update"]
}
```

## Step 3 — Store

Write the complete observation to ChromaDB.
Collection: "site_observations"
Document ID: "{site_name}_{timestamp}"

Emit: [MEMORY:STORED] observation saved

## Step 4 — Update Site Registry If Needed

If new_failures contains items not in ref-site-registry.md:
Note them for Toby.
Format: "New fragile point discovered on [site]: [description]
         Consider adding to ref-site-registry.md"

## Step 5 — Pass Human Observation To Voice

Pass delta_from_previous.human_observation to the narrator.
This becomes the Viktor-style observation Toby sees.

"Nice — [improvement]"
"[regression] — wasn't like this before"
"New [element] appeared on [site]"

## The Learning Loop

Over time, skill-memory builds a complete history of all four sites.
The tester pipeline gets smarter with every run because:
- It knows what broke before
- It knows what was fixed
- It knows the pattern of failures
- It can predict where to look first

This is how Worker Bee earns trust over time.
