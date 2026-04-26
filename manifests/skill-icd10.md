---
name: skill-icd10
description: ICD-10 Medical Codes MCP - lookup diagnosis/procedure codes, validate billing codes, explore code hierarchies. Escalate to Claude API for medical coding.
---

# skill-icd10 — ICD-10 Medical Codes MCP

**MCP Status:** ✅ Available via claude.ai proxy
**Escalation Required:** YES - Claude API only
**Authentication:** None required (read-only data)

**Code Sets:** ICD-10-CM (diagnosis) and ICD-10-PCS (procedure) - 2026 edition

---

## What This MCP Can Do

**Code Lookup:**
- Search codes by code number (e.g., "E11.65")
- Search codes by description (e.g., "diabetes")
- Lookup specific code details
- Validate code for billing (HIPAA compliance)

**Code Exploration:**
- Get chapter categories
- Get code hierarchy (parent/child codes)
- Browse by body system
- Find related codes

**Code Types:**
- **ICD-10-CM** - Diagnosis codes (outpatient/inpatient)
- **ICD-10-PCS** - Procedure codes (inpatient only)

---

## When To Use ICD-10 MCP vs Manual

**Use ICD-10 MCP when:**
- Need exact code for billing
- Validating code is current and billable
- Finding all codes in a disease family
- Automating medical documentation
- Checking code progression (acute → chronic → remission)

**Do it manually when:**
- Learning medical coding (textbooks better for education)
- Complex multi-code scenarios requiring clinical judgment
- Initial diagnosis (doctor determines, not AI)

**Rule of thumb:** If it's code lookup/validation → use MCP. If it's clinical diagnosis → manual only.

---

## How To Escalate to Claude API

**Escalation Pattern:**

```python
if any(word in user_content.lower() for word in ["icd", "diagnosis code", "billing code"]):
    use_claude_api = True
```

**Critical for IME Coach:**
When processing medical legal documents, ICD-10 codes are essential for accurate billing and case documentation.

---

## Available MCP Tools

**Search & Lookup:**
- `search_codes` - Search by code or description
- `lookup_code` - Get specific code details
- `validate_code` - Check if billable

**Hierarchy:**
- `get_chapter` - Get chapter codes
- `get_category` - Get category codes
- `get_hierarchy` - Get code family tree
- `get_by_body_system` - Codes by body system

---

## Common Use Cases

### 1. Find Diagnosis Code

**User Request:** "What's the ICD-10 code for Type 2 diabetes with neuropathy?"

**Worker Bee Action:**
1. Search: "type 2 diabetes neuropathy"
2. Returns: E11.4x codes
3. Validate for billing
4. Return: E11.40 (with neuropathy, unspecified)

**Success:** Returns billable code in < 2 seconds

---

### 2. Validate Billing Code

**User Request:** "Is E11.65 a valid billable code?"

**Worker Bee Action:**
1. Lookup code E11.65
2. Check billable status
3. Return: "Yes, billable. Type 2 diabetes with hyperglycemia"

**Success:** Confirms code valid for HIPAA billing

---

### 3. Find Code Progression

**User Request:** "What are all the leukemia codes for relapse stages?"

**Worker Bee Action:**
1. Search: "leukemia"
2. Get category for specific type (e.g., C92.1 for chronic myeloid)
3. List progression codes:
   - C92.10 - not achieved remission
   - C92.11 - in remission
   - C92.12 - in relapse

**Success:** Complete code family for disease progression

---

### 4. Body System Codes

**User Request:** "List all cardiovascular diagnosis codes"

**Worker Bee Action:**
1. Use `get_by_body_system` with "cardiovascular"
2. Returns chapter I00-I99 codes
3. Filter by relevance

**Success:** Comprehensive cardiovascular code list

---

## Integration with IME Coach

**Critical workflow for medical legal cases:**

```
User uploads medical record
  ↓
OCR extracts diagnosis text
  ↓
skill-icd10 finds matching codes
  ↓
Validate codes for billing
  ↓
Store in Supabase with case
  ↓
Generate report with proper ICD-10 codes
```

**Why this matters:**
- Ensures accurate billing for medical legal cases
- Validates insurance claims
- Provides standardized diagnosis documentation
- Required for IME (Independent Medical Exam) reports

---

## What Success Looks Like

**Good:**
- Code found in < 2 seconds
- Billable status clear
- Full code description provided
- Related codes shown

**Red Flags:**
- Code not found (may be obsolete or wrong version)
- Non-billable code used for billing
- Wrong code type (CM vs PCS)

---

## Failure Modes & Recovery

**Code Not Found:**
- Check spelling of search term
- Try broader search (e.g., "diabetes" vs "diabetes mellitus")
- Verify code is 2026 version

**Non-Billable Code:**
- Check if parent code is billable
- Look for more specific child code
- Validate code is for correct use case (diagnosis vs procedure)

**Wrong Code Type:**
- ICD-10-CM for diagnoses
- ICD-10-PCS for inpatient procedures
- Specify code_type in search

---

## Multi-Tool Workflow Example

**Finding comprehensive diagnosis codes:**

```
1. search_codes(query="diabetes", code_type="diagnosis")
   → Returns E11.x family

2. lookup_code(code="E11")
   → "Type 2 diabetes mellitus" (not billable, too general)

3. get_category(code="E11")
   → Returns all E11.x sub-codes

4. validate_code(code="E11.65")
   → "Billable: Type 2 diabetes with hyperglycemia"
```

---

## Disease Progression Patterns

**Always look up the full set for conditions with stages:**

**Cancer:**
- Primary site code
- "In remission" code
- "In relapse" code
Example: C92.10 → C92.11 → C92.12

**Diabetes:**
- Base type (Type 1 vs Type 2)
- With/without complications
- Specific complication codes

**Heart Disease:**
- Acute vs chronic
- With/without heart failure
- Stage-specific codes

**Workflow:**
Search base condition → Get category → List all progression codes

---

## Security & Medical Accuracy

**Important disclaimers:**

1. **Not a Substitute for Clinical Judgment** - Codes are for documentation, not diagnosis
2. **Doctor Determines Diagnosis** - AI suggests codes based on text, doctor confirms
3. **Billing Compliance** - Always verify with current coding guidelines
4. **2026 Code Set** - Check version year matches billing period

**Approval Gate for Medical Docs:**

```
Worker Bee: "Found ICD-10 code: E11.65
Description: Type 2 diabetes with hyperglycemia
Billable: Yes

This code matches the diagnosis in the document.
Confirm accuracy before using in billing? (yes/no)"
```

---

## Performance Notes

**Fast (< 1s):**
- Lookup specific code
- Validate code
- Get code description

**Medium (1-3s):**
- Search by description
- Get category codes
- List body system codes

**Optimization:**
- Cache common codes (diabetes, hypertension, etc.)
- Use specific searches, not broad queries

---

## Pairs With

- **skill-memory.md** - Store common codes for user's practice
- **skill-reporter.md** - Generate medical reports with ICD-10 codes
- **skill-supabase.md** - Store codes in IME Coach database

---

## The Bottom Line

ICD-10 MCP is essential for medical legal work.

Use it for accurate code lookup, validation, and billing compliance.
Critical component of IME Coach pipeline.

When user needs medical codes, escalate to Claude API.
Always validate codes before using in official documentation.
