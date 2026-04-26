# Skill: SEO Optimization & Site Auditing

**Purpose:** Analyze and optimize websites for search engine rankings. Fix SEO issues systematically.

**When to use:** Website audits, SEO optimization, meta tag fixes, sitemap generation, ranking improvements.

---

## Core Principles

1. **User-First**: Optimize for users first, search engines second. Good UX leads to better SEO.
2. **Unique Content**: Every page needs unique title, description, and H1. Duplicate content hurts rankings.
3. **Mobile-First**: Google uses mobile-first indexing. Always include viewport meta tag.
4. **Accessibility = SEO**: Accessible websites (alt text, semantic HTML, proper headings) rank better.
5. **Technical Foundation**: Fix critical technical issues before advanced optimization.
6. **Quality Over Quantity**: Substantial, valuable content ranks better than thin content.
7. **Regular Updates**: SEO is ongoing. Keep content fresh, monitor analytics.

---

## Quick SEO Audit Checklist

### Critical Issues (Fix First)

- [ ] Title tags present and unique (50-60 chars)
- [ ] Meta descriptions present (150-160 chars)
- [ ] One H1 per page with target keyword
- [ ] Images have descriptive alt text
- [ ] HTML lang attribute set
- [ ] HTTPS with valid SSL certificate
- [ ] Mobile-friendly and responsive
- [ ] No crawl errors in Search Console

### Important Optimizations

- [ ] Viewport meta tag for mobile
- [ ] Proper heading hierarchy (H1 → H2 → H3)
- [ ] Internal links (3-5 per page minimum)
- [ ] Canonical tags to prevent duplicates
- [ ] Open Graph tags for social sharing
- [ ] Twitter Card tags
- [ ] XML sitemap submitted to Search Console
- [ ] Robots.txt properly configured

### Advanced Optimization

- [ ] Schema.org structured data (JSON-LD)
- [ ] Core Web Vitals passing (LCP < 2.5s, INP < 200ms, CLS < 0.1)
- [ ] Page speed optimized (<3s load time)
- [ ] No broken links
- [ ] Clean URL structure
- [ ] Content length matches search intent

---

## SEO Optimization Workflow

### Step 1: Run Site Audit

Analyze the website to identify all issues:

1. **Check indexing status**
   ```bash
   # Check if site is indexed
   # Google: site:domain.com
   # Verify important pages appear
   ```

2. **Analyze HTML files**
   - Look for missing or suboptimal title tags
   - Check meta descriptions
   - Verify heading structure (H1-H6)
   - Find images without alt text
   - Check for Open Graph and Twitter Card tags

3. **Technical checks**
   - HTTPS status
   - Mobile responsiveness
   - Page load speed
   - Core Web Vitals
   - XML sitemap presence
   - Robots.txt configuration

4. **Content quality**
   - Unique vs duplicate content
   - Content length and depth
   - Keyword usage (natural, not stuffed)
   - Readability level

### Step 2: Prioritize Issues

Address issues in this order:

**Priority 1 - Critical (Fix Immediately):**
1. Missing title tags
2. Missing meta descriptions
3. Missing or multiple H1 tags
4. Images without alt text
5. Missing HTML lang attribute
6. HTTPS not configured
7. Mobile unfriendly

**Priority 2 - Important (Fix Soon):**
1. Title/description length issues
2. Missing viewport meta tag
3. Duplicate title tags or descriptions
4. Missing Open Graph tags
5. Missing canonical tags
6. Poor heading hierarchy
7. Slow page speed

**Priority 3 - Optimization (Ongoing):**
1. Schema markup implementation
2. Internal linking strategy
3. Image optimization
4. Content freshness
5. Advanced technical SEO

### Step 3: Fix Critical Issues

**Missing or Poor Title Tags:**
```html
<!-- Add unique, descriptive title to <head> -->
<title>Primary Keyword - Secondary Keyword | Brand Name</title>
```
- Keep 50-60 characters
- Include target keywords at beginning
- Make unique for each page

**Missing Meta Descriptions:**
```html
<!-- Add compelling description to <head> -->
<meta name="description" content="Clear, concise description that includes target keywords and encourages clicks. 150-160 characters.">
```

**H1 Issues:**
- Ensure exactly ONE H1 per page
- H1 should describe the main topic
- Should match or relate to title tag

**Images Without Alt Text:**
```html
<!-- Add descriptive alt text to all images -->
<img src="image.jpg" alt="Descriptive text explaining image content">
```

**Missing HTML Lang:**
```html
<!-- Add to opening <html> tag -->
<html lang="en">
```

**Mobile Optimization:**
```html
<!-- Add viewport meta tag to <head> -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta charset="UTF-8">
```

### Step 4: Add Social Media Tags

**Open Graph Tags** (for Facebook, LinkedIn):
```html
<meta property="og:title" content="Your Page Title">
<meta property="og:description" content="Your page description">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page-url">
<meta property="og:type" content="website">
```

**Twitter Card Tags:**
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Your Page Title">
<meta name="twitter:description" content="Your page description">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

### Step 5: Implement Schema Markup

Use JSON-LD format in `<head>` or before `</body>`:

**Article/Blog Post:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "datePublished": "2026-01-15",
  "dateModified": "2026-04-25",
  "image": "https://example.com/image.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.jpg"
    }
  }
}
</script>
```

**Local Business:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "image": "https://example.com/storefront.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345",
    "addressCountry": "US"
  },
  "telephone": "+1-555-555-5555",
  "openingHours": "Mo-Fr 09:00-17:00"
}
</script>
```

**FAQ:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is your return policy?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "We offer 30-day returns on all products."
    }
  }]
}
</script>
```

### Step 6: Generate XML Sitemap

Create a sitemap listing all important pages:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2026-04-25</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/about</loc>
    <lastmod>2026-04-20</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

Save as `sitemap.xml` in website root, then:
1. Add to robots.txt: `Sitemap: https://example.com/sitemap.xml`
2. Submit to Google Search Console
3. Submit to Bing Webmaster Tools

### Step 7: Configure Robots.txt

Create `robots.txt` in website root:

```
User-agent: *
Allow: /

# Block sensitive directories
Disallow: /admin/
Disallow: /private/
Disallow: /api/

# Sitemap location
Sitemap: https://yourdomain.com/sitemap.xml
```

---

## Content Writing for SEO

### Keyword Strategy

1. **Research target keywords**
   - Use Google Autocomplete
   - Check "People Also Ask" boxes
   - Analyze competitor rankings
   - Focus on search intent (informational, transactional, navigational)

2. **Keyword placement**
   - In title tag (near beginning)
   - In meta description
   - In H1 heading
   - In first 100 words of content
   - In URL slug
   - In image alt text (where relevant)
   - Naturally throughout content (1-2% density)

3. **Avoid keyword stuffing**
   - Use synonyms and related terms
   - Write for humans first
   - Focus on natural language

### Content Structure

1. **Hook in first 100 words**
   - Answer the main query immediately
   - Include target keyword naturally

2. **Use proper heading hierarchy**
   - One H1 (main topic)
   - Multiple H2s (main sections)
   - H3s under H2s (subsections)
   - H4-H6 sparingly

3. **Content length**
   - Match or exceed top-ranking competitors
   - Informational queries: 1500-2500 words
   - Transactional queries: 500-1000 words
   - Prioritize quality over arbitrary word counts

4. **Add supporting elements**
   - Bullet points for scannability
   - Images with alt text
   - Internal links to related pages
   - External links to authoritative sources
   - FAQ section for "People Also Ask"

---

## Technical SEO Checks

### Core Web Vitals

**Largest Contentful Paint (LCP):** < 2.5 seconds
- Optimize images (compress, lazy load)
- Minimize render-blocking resources
- Use CDN for faster delivery

**Interaction to Next Paint (INP):** < 200 milliseconds
- Minimize JavaScript execution
- Avoid long tasks
- Optimize event handlers

**Cumulative Layout Shift (CLS):** < 0.1
- Set image dimensions
- Reserve space for ads/embeds
- Avoid inserting content above existing content

### Page Speed

- Compress images (WebP format)
- Minify CSS and JavaScript
- Enable browser caching
- Use CDN
- Eliminate unused code

### Mobile Optimization

- Responsive design (not separate mobile site)
- Viewport meta tag
- Touch targets at least 44x44px
- Readable font sizes (16px minimum)
- No horizontal scrolling

---

## SEO Red Flags (Avoid These)

- **Keyword stuffing**: Repeating keywords unnaturally
- **Duplicate content**: Copying content from other pages
- **Thin content**: Pages with little value (<300 words with no substance)
- **Cloaking**: Showing different content to users vs search engines
- **Hidden text**: White text on white background
- **Link schemes**: Buying links or participating in link exchanges
- **Doorway pages**: Pages created only for search engines
- **Auto-generated content**: Low-quality content created by bots

---

## Validation Tools

**Before deploying SEO changes, validate:**

1. **Google Rich Results Test**
   - https://search.google.com/test/rich-results
   - Validates schema markup

2. **Schema Markup Validator**
   - https://validator.schema.org/
   - Checks JSON-LD syntax

3. **Google Mobile-Friendly Test**
   - https://search.google.com/test/mobile-friendly
   - Verifies mobile optimization

4. **PageSpeed Insights**
   - https://pagespeed.web.dev/
   - Tests Core Web Vitals

5. **Google Search Console**
   - Submit sitemap
   - Monitor indexing status
   - Check for crawl errors
   - Track search performance

---

## SEO Reporting

Document SEO improvements:

```markdown
# SEO Audit Report

## Summary
- **Critical Issues Fixed:** X
- **Warnings Addressed:** Y
- **Pages Optimized:** Z

## Changes Made

### Title Tags
- Updated X pages with unique titles
- Optimized length (50-60 chars)
- Added target keywords

### Meta Descriptions
- Added missing descriptions (X pages)
- Optimized length (150-160 chars)

### Technical SEO
- [X] Added viewport meta tag
- [X] Implemented schema markup (Article, LocalBusiness)
- [X] Generated XML sitemap
- [X] Configured robots.txt
- [X] Fixed mobile responsiveness

### Content
- Improved heading hierarchy on X pages
- Added alt text to X images
- Added internal links

## Next Steps
1. Submit sitemap to Search Console
2. Monitor Core Web Vitals
3. Update content monthly
4. Build quality backlinks
```

---

## Quick Reference

| Task | Action |
|------|--------|
| Fix missing title | Add `<title>` with 50-60 chars, keyword at start |
| Fix missing description | Add `<meta name="description">` with 150-160 chars |
| Fix missing H1 | Add one H1 per page with main topic |
| Add mobile support | Add `<meta name="viewport">` tag |
| Add social tags | Add Open Graph and Twitter Card meta tags |
| Add schema | Add JSON-LD script with appropriate schema type |
| Create sitemap | Generate sitemap.xml with all page URLs |
| Configure robots | Create robots.txt with sitemap reference |

---

**Remember:** SEO is a long-term strategy. Focus on providing real value to users, and rankings will follow.
