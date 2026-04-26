---
name: ref-site-registry
description: Read before any tester or repair pipeline runs. Know the four sites.
---

# Site Registry — The Four Production Sites

## How To Use This File

Before writing any test plan or repair diagnosis,
read the relevant site entry completely.
The fragile points are where failures happen.
The known journeys are what Viktor tested.
Do not test what does not matter.
Test what breaks.

---

## 1. mountainedgeplumbing.com

**Purpose:** Public plumbing business website, Twin Falls Idaho
**Client portal:** mountainedgeplumbing.com/login

**Primary journeys to test:**
- ACQUISITION: Homepage → Services → Contact form → Confirmation
- CONVERSION: "Request a Quote" form — fill with realistic data → submit → confirm
- AUTH: Client portal login → dashboard access → logout

**Known fragile points:**
- Contact form submission — verify it actually hits backend, not just shows confirmation
- Client portal login — check for session timeout behavior
- Mobile menu — verify hamburger menu works on narrow viewport

**Test data to use:**
- Name: John Smith
- Phone: 208-555-0142
- Service needed: Water heater replacement
- Address: 450 Shoshone St N, Twin Falls ID

**What good looks like:**
- Form submits and shows "Thank you, we'll be in touch"
- Portal login reaches dashboard with job list
- All pages load under 3 seconds

**Delta watch:**
- Any new services or pages added
- Contact form availability
- Portal authentication changes

---

## 2. ime-coach.com (MedLegal Nexus)

**Purpose:** Medical legal case management — OCR + AI report building
**Auth:** ime-coach.com/auth

**Primary journeys to test:**
- CONVERSION: File upload → OCR trigger → citation links clickable → report generated
- AUTH: Login → case list → upload new case → logout

**Known fragile points:**
- OCR pipeline — has been slow repeatedly, watch response time
- File upload — verify file actually processes, not just uploads
- Clickable citations — these break when OCR output format changes
- Auth session — check token refresh behavior on long sessions

**Test data to use:**
- Upload a small PDF (under 1MB) for OCR testing
- Check that citations in output are clickable links, not plain text

**What good looks like:**
- Upload completes in under 30 seconds
- OCR result appears with clickable citations
- Report generation completes without timeout

**Delta watch:**
- OCR response time — flag if over 30 seconds (was fast, has slowed)
- Citation format — flag if links become plain text
- Any authentication errors

---

## 3. growyournumber.com

**Purpose:** Financial suite for doctors — contract eval, tax bots, file vault
**Auth:** embedded in app

**Primary journeys to test:**
- CONVERSION: Contract upload → evaluation → recommendations displayed
- CONVERSION: Tax bot — input question → receive answer
- ACQUISITION: File vault — upload → retrieve → download

**Known fragile points:**
- File vault — upload/retrieve cycle needs end to end verification
- Tax bot responses — verify answers are coherent, not truncated
- Contract evaluation — check that PDF parsing works on varied formats

**What good looks like:**
- Contract evaluation returns structured analysis within 60 seconds
- Tax bot answers are complete (not cut off)
- File vault round-trip works (upload → list → download same file)

**Delta watch:**
- This site needs serious stress testing (noted in session notes)
- Any new features need immediate E2E verification
- Response times for all AI-powered features

---

## 4. language-lens-elite.lovable.app (LinguaLens)

**Purpose:** Language learning platform — Toby's most impressive build
**Languages:** Spanish, French, German, Italian, Japanese, Korean

**Primary journeys to test:**
- ACQUISITION: Land → select language → start lesson → complete first exercise
- CONVERSION: Battle game — start → complete round → XP awarded → score saved
- RETENTION: XP system — verify XP persists between sessions

**Known fragile points:**
- TTS (text to speech) — verify audio actually plays, not just shows player
- Battle game scoring — was broken, then fixed — watch for regression
- XP persistence — verify XP saves to storage between sessions
- Dual reader — verify both language panels render simultaneously

**Test data to use:**
- Language: Spanish (most tested, most stable)
- Battle game: complete one full round

**What good looks like:**
- TTS plays audio within 2 seconds of trigger
- Battle game completes round and shows score
- XP total matches expected after exercise
- Dual reader shows English + Spanish simultaneously

**Delta watch:**
- Battle game scoring (known regression point)
- TTS playback (depends on browser audio permissions)
- XP persistence across session boundary

---

## Morning Sweep Priority Order

When running morning sweep of all four sites, test in this order:
1. ime-coach.com — highest business stakes, OCR fragility
2. growyournumber.com — needs stress testing attention
3. mountainedgeplumbing.com — client-facing, professional stakes
4. LinguaLens — Toby's personal project, lower urgency

Flag immediately to Toby:
- Any auth failure on any site
- OCR response over 30 seconds
- Contact form failure on mountainedge
- Battle game regression on LinguaLens
