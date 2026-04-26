# Skill: Image Generation & Visual Content Creation

**Purpose:** Analyze images and generate detailed prompts for AI image generation. Create visual content using Lovable.ai and other image tools.

**When to use:** Image analysis, prompt generation for image AI, visual content creation, screenshot analysis.

---

## Core Capabilities

1. **Image-to-Prompt**: Analyze existing images and generate reproduction-quality prompts
2. **Prompt Crafting**: Write detailed, effective prompts for image generation
3. **Visual Analysis**: Extract visual elements, styles, and composition details
4. **Category Detection**: Classify images (portrait, landscape, product, animal, illustration)

---

## Image Analysis Workflow

### Step 1: Category Detection

First, classify the image into one of these categories:

- **portrait** — People as main subject (photos, artwork, digital art)
- **landscape** — Natural scenery, cityscapes, architecture, outdoor environments
- **product** — Commercial product photos, merchandise
- **animal** — Animals as main subject
- **illustration** — Diagrams, infographics, UI mockups, technical drawings
- **other** — Images that don't fit above categories

### Step 2: Category-Specific Analysis

Generate a detailed prompt based on the detected category.

---

## Category-Specific Elements to Analyze

### Portrait Analysis

When analyzing portraits, extract these elements:

**Model/Style:**
- Photography type (photorealistic, digital art, oil painting, etc.)
- Quality level (ultra-high, professional, amateur)
- Visual style (cinematic, natural light, studio)

**Subject Details:**
- Gender, age range, ethnicity
- Skin tone and undertones
- Body type and build
- Distinctive features

**Facial Features:**
- Eye color, shape, gaze direction
- Lips (color, fullness, expression)
- Face shape (oval, round, square, heart)
- Expression (confident, serene, playful, serious)

**Hair:**
- Color (specific shades: honey blonde, auburn, jet black)
- Length and style
- Texture (straight, wavy, curly)
- Part (center, side, none)

**Pose & Positioning:**
- Body position (standing, sitting, lying)
- Orientation to camera (direct, three-quarter, profile)
- Leg and hand positions
- Gaze direction (camera, off-camera, downward)

**Clothing:**
- Type and style
- Color and patterns
- Material and texture
- Fit (loose, fitted, flowing)

**Accessories:**
- Jewelry, bags, hats, glasses
- Style and materials

**Environment:**
- Location type (studio, outdoor, urban, indoor)
- Background details
- Atmosphere and mood

**Lighting:**
- Type (natural, studio, golden hour, blue hour)
- Direction (front, side, back, rim)
- Quality (soft, hard, diffused)
- Shadows and highlights
- Color temperature

**Camera & Technical:**
- Angle (eye-level, low, high)
- Shot type (close-up, medium, full-body, wide)
- Lens characteristics (portrait 85mm, wide 24mm)
- Depth of field (shallow, deep)
- Perspective (straight-on, dynamic)

### Landscape Analysis

**Terrain Features:**
- Mountains, valleys, hills, plains
- Rock formations, cliffs, canyons
- Bodies of water (oceans, lakes, rivers, waterfalls)
- Vegetation type and density

**Sky & Atmosphere:**
- Cloud formations and coverage
- Time of day (sunrise, sunset, midday, night)
- Weather conditions (clear, stormy, foggy, snowy)
- Atmospheric effects (mist, haze, rays of light)

**Composition:**
- Foreground elements
- Middleground features
- Background layers
- Leading lines and visual flow

**Lighting:**
- Natural light direction and quality
- Time of day indicators
- Color palette (warm, cool, muted, vibrant)

**Photography Style:**
- Landscape photography
- Wide-angle perspective
- Long exposure effects
- HDR processing

### Product Analysis

**Product Features:**
- Shape and design
- Materials and textures
- Colors and finishes
- Size and proportions
- Brand elements and logos

**Staging:**
- Background type (white, gradient, lifestyle)
- Props and context elements
- Surface and placement

**Lighting:**
- Studio lighting setup
- Number of lights (key, fill, rim)
- Light modifiers (softbox, reflector)
- Reflections and highlights

**Photography Style:**
- Commercial product photography
- Catalog style
- Lifestyle integration
- E-commerce standard

### Animal Analysis

**Species & Characteristics:**
- Species identification
- Breed (if applicable)
- Markings and coloration
- Size and build

**Pose & Behavior:**
- Position and posture
- Action or activity
- Expression and mood
- Interaction with environment

**Setting:**
- Habitat type (wild, domestic, studio)
- Environmental context
- Background elements

**Photography Style:**
- Wildlife photography
- Pet portrait
- Documentary style
- Action/motion capture

### Illustration Analysis

**Diagram Type:**
- Flowchart, infographic, mind map
- UI mockup, wireframe
- Technical diagram, schematic
- Data visualization

**Visual Elements:**
- Icons and symbols
- Shapes and connectors
- Text and labels
- Charts and graphs

**Layout & Hierarchy:**
- Information flow
- Visual hierarchy
- Grouping and organization
- Alignment and spacing

**Design Style:**
- Flat design, isometric, 3D
- Hand-drawn, vector, digital
- Minimal, detailed, decorative

**Color Scheme:**
- Palette choice
- Color meaning and coding
- Contrast and readability

---

## Prompt Generation Strategies

### Natural Language Prompts

Write flowing, detailed descriptions (600-1000 words for portraits, 400-600 for others):

**Example Structure:**
```
A [quality level] [style] of [subject]. [Age/gender/ethnicity] with [distinctive features].
[Detailed facial features]. [Hair description]. [Pose and positioning]. Wearing [clothing details].
[Environment and setting]. [Lighting description]. [Camera angle and technical details].
[Mood and atmosphere]. [Additional visual effects].
```

### Structured Prompts

Use JSON or structured format for precise control:

```json
{
  "style": "photorealistic cinematic",
  "subject": "young woman, mid-20s, porcelain skin",
  "pose": "standing, three-quarter turn, direct gaze",
  "clothing": "flowing maxi dress, dusty rose",
  "environment": "golden hour beach, soft sand",
  "lighting": "natural backlight, warm glow, rim lighting",
  "camera": "85mm portrait lens, shallow depth of field",
  "mood": "serene, confident, romantic"
}
```

### Dimension Extraction

Tag phrases for each visual aspect:

**Backgrounds:** [beach at sunset], [modern studio], [urban rooftop]
**Objects:** [vintage camera], [floral arrangement], [geometric sculpture]
**Characters:** [confident businesswoman], [playful child], [wise elder]
**Styles:** [cinematic lighting], [minimalist composition], [vibrant colors]
**Actions:** [walking towards camera], [laughing], [contemplative pose]
**Colors:** [warm golden tones], [cool blue palette], [monochromatic]
**Moods:** [serene atmosphere], [energetic vibe], [melancholic feeling]
**Lighting:** [soft diffused], [dramatic shadows], [golden hour glow]
**Compositions:** [rule of thirds], [symmetrical], [dynamic diagonal]
**Themes:** [freedom], [connection], [isolation]

---

## Image Generation Best Practices

### Writing Effective Prompts

**Be Specific:**
- "A woman" → "A young woman in her mid-20s with porcelain skin and emerald green eyes"
- "Nice lighting" → "Soft natural window light from the left, creating gentle shadows"
- "Beautiful photo" → "Professional photorealistic portrait with cinematic composition"

**Use Quality Modifiers:**
- Photorealistic, ultra-high quality, professional photography
- 8K resolution, sharp focus, detailed textures
- Award-winning, masterpiece, stunning visual

**Describe Composition:**
- Camera angle: eye-level, low angle, bird's eye view
- Shot type: close-up, medium shot, full-body, wide shot
- Framing: centered, rule of thirds, off-center
- Depth of field: shallow bokeh, deep focus, selective focus

**Specify Lighting:**
- Type: natural light, studio lighting, golden hour, blue hour
- Direction: front-lit, side-lit, backlit, rim lighting
- Quality: soft, hard, diffused, dramatic
- Color temperature: warm, cool, neutral

**Set the Mood:**
- Atmosphere: serene, energetic, mysterious, playful
- Emotion: confident, joyful, contemplative, intense
- Visual tone: vibrant, muted, high-contrast, soft

### Negative Prompts (What to Avoid)

Include these to improve quality:

```
ugly, blurry, low quality, distorted, disfigured, bad anatomy,
extra limbs, missing fingers, cropped, watermark, text, logo,
cartoon, 3D render (if wanting photorealistic)
```

### Iterative Refinement

1. **Generate initial image** with base prompt
2. **Analyze results**: What worked? What didn't?
3. **Refine prompt**: Add more detail to weak areas
4. **Adjust parameters**: Change style, lighting, or composition
5. **Regenerate**: Test refined prompt
6. **Repeat** until desired result

---

## Technical Specifications

### Common Aspect Ratios

- **1:1** - Square (social media posts, profile pictures)
- **2:3** - Portrait (standard photo print, magazine cover)
- **3:2** - Landscape (standard photo format)
- **4:3** - Classic photo (traditional film ratio)
- **16:9** - Widescreen (desktop backgrounds, video thumbnails)
- **9:16** - Vertical video (Instagram Stories, TikTok)
- **21:9** - Ultrawide (cinematic, panoramic)

### Resolution Recommendations

- **Social Media:** 1080x1080 (Instagram), 1200x630 (Facebook)
- **Print:** 300 DPI (2400x3000 for 8x10 inch)
- **Web:** 72-150 DPI (1920x1080 for full HD)
- **Thumbnails:** 512x512 to 1024x1024

---

## Integration with Lovable.ai

When building websites with Lovable.ai, use image generation for:

**Hero Sections:**
- Generate custom hero images matching brand aesthetic
- Create unique backgrounds that stand out

**Product Showcases:**
- Visualize products in various settings
- Create lifestyle imagery

**Testimonials:**
- Generate portrait-style testimonial images
- Create consistent visual style across testimonials

**Icons & Graphics:**
- Generate custom icons and graphic elements
- Create unique visual assets

**Example Workflow:**
```
1. Analyze desired aesthetic from design mockup
2. Extract color palette, style, mood
3. Generate matching hero image with prompt
4. Download and upload to Lovable.ai project
5. Integrate into website design
```

---

## Quick Reference: Prompt Templates

### Portrait Photography
```
Professional photorealistic portrait of [subject description], [age/gender/ethnicity],
[facial features], [hair description], [pose]. Wearing [clothing]. [Environment].
[Lighting type] lighting. Shot with [camera/lens]. [Mood/atmosphere].
Ultra-high quality, sharp focus, 8K resolution.
```

### Landscape Photography
```
Breathtaking landscape photograph of [location/terrain], [time of day], [weather conditions].
[Foreground elements], [background features]. [Sky description]. [Lighting conditions].
Shot with [camera/lens], [composition style]. [Color palette]. Professional photography,
ultra-sharp, vivid colors.
```

### Product Photography
```
Professional product photography of [product], [product details], [materials/textures].
Placed on [surface/background]. [Lighting setup]. Commercial photography style,
clean composition, sharp focus, high resolution, studio quality.
```

### Illustration/Design
```
[Style] illustration of [subject/concept]. [Visual elements]. [Color scheme].
[Layout/composition]. [Design style]. Vector graphics, clean lines,
professional design, high quality.
```

---

## Validation & Quality Check

Before finalizing any generated image:

- [ ] Subject/content matches prompt intent
- [ ] Quality is sufficient for intended use
- [ ] Lighting and mood are appropriate
- [ ] Composition is balanced and effective
- [ ] No unwanted artifacts or distortions
- [ ] Resolution meets requirements
- [ ] Colors are accurate and appealing
- [ ] Style is consistent with brand/project

---

**Remember:** Great prompts are specific, detailed, and intentional. The more clarity you provide, the better the results.
