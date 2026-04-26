# Skill: Web Design & Frontend Architecture

**Purpose:** Design and build modern, distinctive web interfaces. Create production-grade UI with exceptional aesthetics.

**When to use:** Building landing pages, dashboards, UI components, or any frontend design work.

---

## Design Workflow

Follow this structured approach for every UI project:

1. **Layout Design** — Think through component structure, create ASCII wireframes
2. **Theme Design** — Define colors, fonts, spacing, shadows
3. **Animation Design** — Plan micro-interactions and transitions
4. **Implementation** — Generate the actual code

### Step 1: Layout Design

Before coding, sketch the layout in ASCII format:

```
┌─────────────────────────────────────┐
│         HEADER / NAV BAR            │
├─────────────────────────────────────┤
│                                     │
│            HERO SECTION             │
│         (Title + CTA)               │
│                                     │
├─────────────────────────────────────┤
│   FEATURE   │  FEATURE  │  FEATURE  │
│     CARD    │   CARD    │   CARD    │
├─────────────────────────────────────┤
│            FOOTER                   │
└─────────────────────────────────────┘
```

**Purpose:** Clarify structure before diving into details.

### Step 2: Choose a Bold Aesthetic Direction

**CRITICAL:** Choose a clear conceptual direction and execute it with precision.

**Pick an extreme:**
- Brutally minimal
- Maximalist chaos
- Retro-futuristic
- Organic/natural
- Luxury/refined
- Playful/toy-like
- Editorial/magazine
- Brutalist/raw
- Art deco/geometric
- Soft/pastel
- Industrial/utilitarian

**Differentiation:** What makes this UNFORGETTABLE? What's the one thing someone will remember?

Bold maximalism and refined minimalism both work — the key is intentionality, not intensity.

---

## Theme Guidelines

### Color Rules

**NEVER use:**
- Generic bootstrap-style blue (#007bff) — it looks dated
- Cliched color schemes (purple gradients on white)
- Overused AI defaults (avoid what everyone else picks)

**DO use:**
- **oklch()** for modern color definitions
- Semantic color variables (`--primary`, `--secondary`, `--muted`)
- Consider both light and dark mode from the start
- Dominant colors with sharp accents (not evenly-distributed palettes)

**Example Modern Dark Mode (Vercel/Linear style):**
```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.970 0 0);
  --muted: oklch(0.970 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --border: oklch(0.922 0 0);
  --radius: 0.625rem;
  --font-sans: Inter, system-ui, sans-serif;
}
```

**Example Neo-Brutalism (90s web revival):**
```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0 0 0);
  --primary: oklch(0.649 0.237 26.97);
  --secondary: oklch(0.968 0.211 109.77);
  --accent: oklch(0.564 0.241 260.82);
  --border: oklch(0 0 0);
  --radius: 0px;
  --shadow: 4px 4px 0px 0px hsl(0 0% 0%);
  --font-sans: DM Sans, sans-serif;
  --font-mono: Space Mono, monospace;
}
```

**Example Glassmorphism:**
```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
}
```

### Font Selection

**Choose fonts that are beautiful, unique, and interesting.**

**AVOID generic fonts:** Arial, Inter, Roboto (overused)

**DO use distinctive choices from Google Fonts:**

**Sans-serif:** Outfit, Plus Jakarta Sans, DM Sans, Space Grotesk, Montserrat, Poppins
**Monospace:** JetBrains Mono, Fira Code, Source Code Pro, IBM Plex Mono, Space Mono, Geist Mono
**Serif:** Merriweather, Playfair Display, Lora, Source Serif Pro, Libre Baskerville
**Display:** Architects Daughter, Oxanium

**Pairing strategy:** Pair a distinctive display font with a refined body font.

**Import via Google Fonts:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Space+Mono&display=swap" rel="stylesheet">
```

### Spacing & Shadows

- **Consistent spacing scale:** Use 0.25rem (4px) as base unit
- **Shadows:** Subtle, not heavy drop shadows
  - Light: `box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);`
  - Medium: `box-shadow: 0 3px 6px rgba(0,0,0,0.15), 0 2px 4px rgba(0,0,0,0.12);`
- **Consider oklch() for shadow colors** for more sophisticated depth

### Backgrounds & Visual Details

**Create atmosphere and depth rather than defaulting to solid colors.**

**Creative forms:**
- Gradient meshes
- Noise textures
- Geometric patterns
- Layered transparencies
- Dramatic shadows
- Decorative borders
- Custom cursors
- Grain overlays

**Spatial composition:**
- Unexpected layouts
- Asymmetry
- Overlap
- Diagonal flow
- Grid-breaking elements
- Generous negative space OR controlled density (pick one, execute well)

---

## Animation Guidelines

### Micro-syntax for Planning

```
button: 150ms [S1→0.95→1] press
hover: 200ms [Y0→-2, shadow↗]
fadeIn: 400ms ease-out [Y+20→0, α0→1]
slideIn: 350ms ease-out [X-100→0, α0→1]
bounce: 600ms [S0.95→1.05→1]
```

### Common Patterns

**Timing:**
- Entry animations: 300-500ms, ease-out
- Hover states: 150-200ms
- Button press: 100-150ms
- Page transitions: 300-400ms

**Effects:**
- Buttons: Scale down on click (0.95), lift on hover
- Cards: Subtle lift + shadow increase on hover
- Navigation: Smooth underline grow from left
- Modals: Fade background + scale up content
- Loading: Skeleton screens, not spinners

**Focus on high-impact moments:** One well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions.

**Prioritize CSS-only solutions.** Use JavaScript animations only when CSS can't achieve the effect.

---

## Implementation

### Use Tailwind CSS for Rapid Development

```html
<!-- Import via CDN for prototypes -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Configure custom theme -->
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          primary: '#...',
          secondary: '#...'
        },
        fontFamily: {
          sans: ['Outfit', 'sans-serif'],
          mono: ['Space Mono', 'monospace']
        }
      }
    }
  }
</script>
```

### Component Libraries (Optional)

**Flowbite** (Tailwind-based components):
```html
<link href="https://cdn.jsdelivr.net/npm/flowbite@2.0.0/dist/flowbite.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/flowbite@2.0.0/dist/flowbite.min.js"></script>
```

**Icons (Lucide):**
```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<script>lucide.createIcons();</script>
```

### Images

- Use real placeholder services: Unsplash, placehold.co
- Never make up image URLs
- Example: `https://images.unsplash.com/photo-xxx?w=800&h=600`

---

## Responsive Design (Mobile-First)

Always design mobile-first and scale up:

```css
/* Mobile first (default) */
.container {
  padding: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

**With Tailwind:**
```html
<!-- Mobile: p-4, Tablet: md:p-6, Desktop: lg:max-w-7xl -->
<div class="p-4 md:p-6 lg:max-w-7xl lg:mx-auto">
  Content
</div>
```

---

## Accessibility

- **Use semantic HTML:** `<header>`, `<main>`, `<nav>`, `<section>`, `<article>`, `<aside>`, `<footer>`
- **Proper heading hierarchy:** H1 → H2 → H3 (logical flow)
- **Add aria-labels** to interactive elements
- **Color contrast:** 4.5:1 minimum for text
- **Keyboard navigation:** Ensure all interactive elements are focusable and keyboard-accessible
- **Focus states:** Visible focus indicators for keyboard users

---

## Component Design Tips

### Cards

- Subtle shadows, not heavy drop shadows
- Consistent padding: `p-4` to `p-6` in Tailwind
- Hover state: slight lift + shadow increase

```css
.card {
  transition: transform 150ms, box-shadow 150ms;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}
```

### Buttons

- Clear visual hierarchy (primary, secondary, ghost)
- Adequate touch targets (min 44x44px)
- Loading and disabled states
- Hover: Slight color shift or lift
- Active: Scale down slightly (0.95)

```html
<!-- Primary Button -->
<button class="bg-primary text-white px-6 py-3 rounded-lg font-semibold
               hover:bg-primary-dark active:scale-95 transition">
  Click Me
</button>
```

### Forms

- Clear labels above inputs
- Visible focus states
- Inline validation feedback
- Adequate spacing between fields (1rem minimum)

```html
<div class="space-y-4">
  <div>
    <label class="block text-sm font-medium mb-1">Email</label>
    <input type="email" class="w-full px-4 py-2 border rounded-lg
                                focus:ring-2 focus:ring-primary">
  </div>
</div>
```

### Navigation

- Sticky header for long pages: `position: sticky; top: 0;`
- Clear active state indication
- Mobile-friendly hamburger menu
- Smooth scroll behavior

```css
html {
  scroll-behavior: smooth;
}
```

---

## Anti-Patterns (What NOT to Do)

**NEVER:**
- Use overused font families (Inter, Roboto, Arial everywhere)
- Default to generic layouts (centered logo, nav menu, hero)
- Create cookie-cutter designs that lack context-specific character
- Converge on common AI choices across projects
- Make predictable component patterns without thinking

**AVOID:**
- Heavy drop shadows (use subtle layering instead)
- Excessive animations (focus on key moments)
- Generic stock photos (use custom illustrations or real photos)
- Walls of text (break up with headings, images, white space)
- Tiny touch targets on mobile (<44px)

---

## Quality Checklist

Before delivering any design:

- [ ] Aesthetic is bold and intentional (not generic)
- [ ] Colors are distinctive (not default blues/purples)
- [ ] Fonts are unique and interesting (not Inter/Roboto)
- [ ] Layout has unexpected elements (not cookie-cutter)
- [ ] Mobile responsive (tested at 375px, 768px, 1024px)
- [ ] Accessible (semantic HTML, ARIA labels, keyboard nav)
- [ ] Fast loading (images optimized, minimal JS)
- [ ] Animations are purposeful (not excessive)
- [ ] One clear visual hierarchy (not everything competing for attention)

---

## Quick Reference

| Element | Recommendation |
|---------|---------------|
| Primary font | Outfit, DM Sans, Plus Jakarta Sans (NOT Inter) |
| Code font | JetBrains Mono, Fira Code, Space Mono |
| Border radius | 0.5rem - 1rem (modern), 0 (brutalist) |
| Shadow | Subtle, 1-2 layers max |
| Spacing | 4px base unit (0.25rem) |
| Animation | 150-400ms, ease-out |
| Colors | oklch() for modern, avoid generic blue |
| Layout | ASCII wireframe first, then code |

---

## Example: Landing Page Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Product Name - Tagline</title>
  
  <!-- Tailwind -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
  
  <style>
    body { font-family: 'Outfit', sans-serif; }
  </style>
</head>
<body class="bg-gray-50">
  
  <!-- Header -->
  <header class="sticky top-0 bg-white shadow-sm">
    <nav class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
      <div class="text-2xl font-bold">Logo</div>
      <ul class="flex space-x-6">
        <li><a href="#features" class="hover:text-primary">Features</a></li>
        <li><a href="#pricing" class="hover:text-primary">Pricing</a></li>
        <li><a href="#contact" class="hover:text-primary">Contact</a></li>
      </ul>
    </nav>
  </header>
  
  <!-- Hero -->
  <section class="max-w-7xl mx-auto px-4 py-20 text-center">
    <h1 class="text-5xl font-bold mb-4">Build Amazing Things</h1>
    <p class="text-xl text-gray-600 mb-8">The tagline that explains what you do</p>
    <button class="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold
                   hover:bg-blue-700 active:scale-95 transition">
      Get Started
    </button>
  </section>
  
  <!-- Features -->
  <section id="features" class="max-w-7xl mx-auto px-4 py-20">
    <div class="grid md:grid-cols-3 gap-8">
      <div class="bg-white p-6 rounded-lg shadow-sm">
        <h3 class="text-2xl font-semibold mb-2">Feature 1</h3>
        <p class="text-gray-600">Description of feature</p>
      </div>
      <!-- Repeat for other features -->
    </div>
  </section>
  
  <!-- Footer -->
  <footer class="bg-gray-900 text-white py-12">
    <div class="max-w-7xl mx-auto px-4 text-center">
      <p>&copy; 2026 Company Name. All rights reserved.</p>
    </div>
  </footer>
  
</body>
</html>
```

---

**Remember:** Elegance comes from executing your vision well. Choose a bold direction and commit fully to it. Distinctive beats safe every time.
