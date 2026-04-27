---
name: skill-planner
description: Builder pipeline step 1. Scout (deepseek) breaks down ideas into bite-sized tasks with code examples and verification steps.
version: 2.0.0
metadata:
  pipeline: builder
  step: 1
  model: deepseek-r1:14b
  hands_off_to: skill-builder
  tags: [planning, technical-brief, task-breakdown, implementation-ready]
  evolved_from: skill-planner v1.0 + hermes-agent/writing-plans v1.1.0
---

# skill-planner — Implementation-Ready Technical Briefs

**Model:** deepseek-r1:14b (Scout)
**Called by:** 01-master-controller (Builder pipeline)
**Hands off to:** skill-builder (qwen2.5-coder:32b)

---

## Core Principle

**A good brief makes implementation obvious.**  
If Builder has to guess, the brief is incomplete.

Each task = 2-5 minutes of focused work.  
Include complete code snippets.  
Builder should copy-paste and verify, not invent.

---

## Routing Triggers

QueenB routes to this skill when:
- **Keywords:** "build", "create", "add", "generate", "make", "component", "page", "feature"
- **Context:** User wants new code/component/feature
- **Prerequisites:** Project exists OR scaffold decision made
- **Escalate if:** Architecture unclear, multiple approaches possible, security implications

---

## Common Mistakes (What NOT To Do)

1. **Don't write vague briefs** — "Add a form" is not a brief, Builder will ask questions
2. **Don't skip code examples** — Descriptions aren't enough, show the actual code
3. **Don't make monolithic tasks** — One big component = too large. Break into 3-5 sub-tasks.
4. **Don't skip edge cases** — Builder won't think of them, you must list them
5. **Don't assume Builder knows patterns** — Include the pattern code, don't reference it
6. **Don't skip verification steps** — Builder needs to know what "done" looks like
7. **Don't write briefs without scanning existing code** — Context-blind briefs cause inconsistency

---

## Announce At Start

"I am using skill-planner to write an implementation-ready brief for [feature]. Breaking into bite-sized tasks with code examples."

---

## Follow runner-narrator.md for all status emissions.

---

## Step 1 — Understand The Idea

Read the user's request completely.

**What is the actual goal?** Not what they said — what they need.

**Questions to answer:**
- What problem does this solve?
- Who will use it?
- What's the expected behavior?
- What does success look like?

**Emit:** `[SCOUT:READING] understanding the request`

---

## Step 2 — Scan Existing Code for Context

**BEFORE planning, scan the project for patterns.**

Don't write briefs in a vacuum. Builder needs to match existing style.

**Scan for:**
- Similar components (forms, buttons, layouts)
- Styling patterns (Tailwind classes used)
- State management approach (useState, Context, props)
- File structure conventions (where components live)
- TypeScript patterns (interface naming, prop types)

**Action:**
```bash
# Find similar components
ls src/components/

# Read existing component for pattern
cat src/components/ExistingForm.tsx

# Check styling conventions
grep -r "className=" src/components/ | head -10
```

**Emit:** `[SCOUT:CONTEXT] scanned [N] existing files for patterns`

---

## Step 3 — Break Down Into Bite-Sized Tasks

**Each task = 2-5 minutes of focused work.**

**Too big:**
```
TASK 1: Build contact form
[50 lines of code across form, validation, submission, styling]
```

**Right size:**
```
TASK 1: Create ContactForm component scaffolding (2 min)
TASK 2: Add form fields with TypeScript types (3 min)
TASK 3: Add form validation (4 min)
TASK 4: Add submit handler with API call (5 min)
TASK 5: Add Tailwind styling (3 min)
TASK 6: Add loading and error states (4 min)
```

**Granularity rule:** If a task needs more than one `git commit`, it's too big. Split it.

**Emit:** `[SCOUT:BREAKDOWN] identified [N] bite-sized tasks`

---

## Step 4 — Write The Implementation Brief

### Brief Header (Required)

```markdown
# [Feature Name] Implementation Brief

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]
- Which existing patterns we're following
- Why this approach over alternatives
- What files will be created/modified

**Technology:**
- React 18 + TypeScript
- Tailwind CSS for styling
- [State management approach]
- [API integration if needed]

---
```

**Emit:** `[SCOUT:HEADER] brief header written`

### Task Structure (For Each Task)

````markdown
## Task N: [Descriptive Name]

**Objective:** [What this task accomplishes — one sentence]

**Files:**
- Create: `src/components/ContactForm.tsx`
- Modify: `src/App.tsx` (to import and use)
- Test verification: Watcher checks for [specific element]

**Step 1: Write the code**

```tsx
// Complete code snippet that Builder can copy-paste
export interface ContactFormProps {
  onSubmit?: (data: FormData) => void;
}

export function ContactForm({ onSubmit }: ContactFormProps) {
  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Contact Form</h2>
      {/* Placeholder - Task 2 will add fields */}
    </div>
  );
}
```

**Step 2: Integrate into App**

```tsx
// src/App.tsx - add this import and usage
import { ContactForm } from './components/ContactForm';

// Inside App component:
<ContactForm />
```

**Step 3: Verify**

What Watcher should see:
- Heading "Contact Form" visible
- Max width container centered
- Padding applied

**Step 4: Commit**

```bash
git add src/components/ContactForm.tsx src/App.tsx
git commit -m "feat: add ContactForm component scaffolding"
```

**Emit:** `[BUILDER:TASK_N_COMPLETE] scaffolding complete`

---
````

**Repeat for each task with complete code.**

**Emit:** `[SCOUT:TASKS] wrote [N] implementation tasks`

---

## Step 5 — Add Edge Cases and Error Handling

For each task that involves user input or external calls:

```markdown
## Edge Cases for Task 3 (Form Validation)

**Empty fields:**
```tsx
// Show error when email is empty
{errors.email && <p className="text-red-500 text-sm">{errors.email}</p>}
```

**Invalid email format:**
```tsx
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!emailRegex.test(formData.email)) {
  setErrors({ email: 'Please enter a valid email' });
}
```

**Network failure:**
```tsx
try {
  await submitForm(formData);
} catch (error) {
  setError('Submission failed. Please try again.');
}
```
```

**Emit:** `[SCOUT:EDGE_CASES] documented edge cases for [N] tasks`

---

## Step 6 — Define Success Criteria

**For each task, state EXACTLY what Watcher should verify.**

**Good success criteria:**
```
Watcher should see:
- Email input field with placeholder "your@email.com"
- Submit button with text "Send Message" in blue (bg-blue-600)
- When email is empty and submit clicked → red error text appears
- When form submits successfully → "Thank you!" message appears
```

**Bad success criteria:**
```
- Form should work
- Should look good
- User can submit
```

**Specific = Watcher can verify. Vague = Watcher guesses.**

**Emit:** `[SCOUT:SUCCESS_CRITERIA] defined verification criteria for all tasks`

---

## Hard Gates

<HARD-GATE>
The brief is not complete until Builder could implement it
without asking a single question.

Before handing to Builder, read your brief as if you are Builder
seeing it for the first time. Would you need to make ANY decisions?

If yes — make them in the brief. Add the code. Specify the approach.
</HARD-GATE>

<HARD-GATE>
Every task must include:
1. Complete code snippet (copy-paste ready)
2. File paths (exact, not "somewhere in src/")
3. Verification criteria (specific visual/functional checks)
4. Commit message (what this task accomplishes)

Tasks missing any of these are incomplete.
</HARD-GATE>

<HARD-GATE>
If you haven't scanned existing code for patterns (Step 2),
the brief will be context-blind.

Builder will create inconsistent code. MUST scan first.
</HARD-GATE>

**Emit:** `[SCOUT:BRIEF_COMPLETE] → handing implementation-ready brief to Builder`

---

## Example Brief (Good)

````markdown
# Contact Form Implementation Brief

**Goal:** Add a contact form to mountainedgeplumbing.com that emails submissions to owner

**Architecture:**
- Following existing form pattern from FeaturesForm.tsx
- Email submission via /api/contact endpoint (already exists)
- Tailwind styling matching site blue theme (bg-blue-600)

**Technology:**
- React 18 + TypeScript
- Tailwind CSS (existing classes)
- Fetch API for submission
- useState for form state and errors

---

## Task 1: Create ContactForm Component Scaffolding

**Objective:** Create basic component structure with container and heading

**Files:**
- Create: `src/components/ContactForm.tsx`
- Modify: `src/App.tsx` (import and render)

**Code:**

```tsx
// src/components/ContactForm.tsx
export interface ContactFormProps {
  onSuccess?: () => void;
}

export function ContactForm({ onSuccess }: ContactFormProps) {
  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Contact Us</h2>
      {/* Fields will be added in Task 2 */}
    </div>
  );
}
```

```tsx
// src/App.tsx - add to imports
import { ContactForm } from './components/ContactForm';

// Add to component tree where contact section goes
<section id="contact" className="py-12">
  <ContactForm />
</section>
```

**Verify:** Watcher should see "Contact Us" heading in white rounded card

**Commit:**
```bash
git add src/components/ContactForm.tsx src/App.tsx
git commit -m "feat: add ContactForm component scaffolding"
```

---

## Task 2: Add Form Fields with TypeScript Types

**Objective:** Add name, email, message fields with proper types

**Files:**
- Modify: `src/components/ContactForm.tsx`

**Code:**

```tsx
// Add to ContactForm.tsx after imports
interface FormData {
  name: string;
  email: string;
  message: string;
}

// Add inside ContactForm component, before return
const [formData, setFormData] = useState<FormData>({
  name: '',
  email: '',
  message: ''
});

const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
  setFormData(prev => ({
    ...prev,
    [e.target.name]: e.target.value
  }));
};

// Replace comment in JSX with:
<form className="space-y-4">
  <div>
    <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
      Name
    </label>
    <input
      type="text"
      id="name"
      name="name"
      value={formData.name}
      onChange={handleChange}
      className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
      placeholder="Your name"
    />
  </div>

  <div>
    <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
      Email
    </label>
    <input
      type="email"
      id="email"
      name="email"
      value={formData.email}
      onChange={handleChange}
      className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
      placeholder="your@email.com"
    />
  </div>

  <div>
    <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
      Message
    </label>
    <textarea
      id="message"
      name="message"
      value={formData.message}
      onChange={handleChange}
      rows={4}
      className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
      placeholder="How can we help?"
    />
  </div>

  {/* Submit button added in Task 3 */}
</form>
```

**Verify:** Watcher should see:
- Three input fields (name, email, message)
- All fields have labels
- Placeholder text visible
- Border turns blue when focused

**Commit:**
```bash
git add src/components/ContactForm.tsx
git commit -m "feat: add ContactForm input fields with state"
```

---

## Task 3: Add Form Validation

**Objective:** Validate email format and required fields before submission

**Files:**
- Modify: `src/components/ContactForm.tsx`

**Code:**

```tsx
// Add error state
const [errors, setErrors] = useState<Partial<FormData>>({});

// Add validation function
const validate = (): boolean => {
  const newErrors: Partial<FormData> = {};
  
  if (!formData.name.trim()) {
    newErrors.name = 'Name is required';
  }
  
  if (!formData.email.trim()) {
    newErrors.email = 'Email is required';
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
    newErrors.email = 'Please enter a valid email';
  }
  
  if (!formData.message.trim()) {
    newErrors.message = 'Message is required';
  }
  
  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};

// Add error display below each input (example for email):
{errors.email && (
  <p className="text-red-500 text-sm mt-1">{errors.email}</p>
)}
```

**Edge Cases:**
- Empty fields → show "X is required"
- Invalid email format → show "Please enter a valid email"
- Only whitespace → treated as empty
- Clear errors when user starts typing

**Verify:** Watcher should see:
- Red error text appears when field is empty and user tries to submit
- Error disappears when user starts typing
- Email validation catches "test" but accepts "test@example.com"

**Commit:**
```bash
git add src/components/ContactForm.tsx
git commit -m "feat: add ContactForm validation"
```

[Continue for remaining tasks...]

````

**Emit:** `[SCOUT:EXAMPLE] good brief structure demonstrated`

---

## Example Brief (Bad - Don't Do This)

```markdown
# Contact Form

Build a contact form.

It should have name, email, and message fields.
Make it look nice.
Submit to the API.
Show success message.

Files: ContactForm.tsx
```

**Why this is bad:**
- No task breakdown (monolithic)
- No code snippets (Builder has to invent)
- Vague styling ("look nice")
- No TypeScript types specified
- No verification criteria
- No edge cases
- No commit strategy

**Builder would have to ask:**
- What TypeScript types for form data?
- Which Tailwind classes for "nice"?
- Which API endpoint?
- What does success message say?
- Where does this component go?
- How to handle validation?

**This violates the Hard Gate: Builder has to make decisions.**

---

## Integration with Builder Pipeline

**Scout writes brief → hands to Builder (qwen)**

Builder receives:
- Complete task list
- Code snippets per task
- Verification criteria per task
- Commit messages per task

Builder's job:
1. Copy-paste code from Task 1
2. Verify with Watcher
3. Commit
4. Repeat for Task 2, 3, etc.

**No invention. No decisions. Just implementation.**

If Builder has questions = Scout's brief was incomplete = return to Scout for clarification.

---

## Real-World Impact

**Old brief format (v1.0):**
- High-level descriptions
- Builder had to invent code
- ~30% of builds needed clarification
- Watcher found issues in ~50% of first builds
- Multiple Builder → Scout → Builder cycles

**New brief format (v2.0):**
- Bite-sized tasks with code
- Copy-paste implementation
- <10% clarification rate (goal)
- <20% Watcher issues (goal)
- Mostly one-pass builds

**Better briefs = faster builds = fewer iterations = autonomous overnight operation.**
