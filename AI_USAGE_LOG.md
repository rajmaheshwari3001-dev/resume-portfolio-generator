<div align="center">
  <h1>🤖 AI Usage Log</h1>
  <p><em>Tracking the collaborative pair-programming journey with Artificial Intelligence.</em></p>
</div>

---

### 🧠 Core Development & Problem Solving

| Action | Details |
| :--- | :--- |
| **🛠 Primary Tool** | Google Gemini (via Agentic Coding Assistant) |
| **🗣 Key Prompts** | 1. "Assist in defining a strict JSON schema for the Google GenAI extraction prompt to prevent data hallucination."<br>2. "Provide logic for an exponential backoff loop to gracefully handle API 503 high-demand errors."<br>3. "Add a feature to select portfolio themes (Glassmorphism, Cyberpunk, Neobrutalism)."<br>4. "Implement a smart Resume Strength Meter to visually validate inputs before hitting the API, saving credits."<br>5. "Ensure the entire platform passes strict Lighthouse SEO and Accessibility audits."<br>6. "Fix text readability on the Neobrutalism theme, add a 'Proceed Anyway' option to validation, and increase generation speed by upgrading to gemini-1.5-flash-8b."<br>7. "Fix invisible text on light themes, resolve missing Lucide icons for GitHub and LinkedIn, and strictly enforce Name and Contact validation." |
| **✨ Generated Assets** | - **Architecture:** Baseline boilerplate for SDK integration and the exponential backoff try/except loop.<br>- **UI/UX Design:** Complete "Brighter Vibes" landing page redesign featuring frosty glassmorphism panels, CSS variables, and GSAP animations. Added advanced micro-animations for skills.<br>- **Smart Validation:** The heuristic client-side strength meter and strict validation modal logic with "Proceed Anyway" override.<br>- **Dynamic Themes:** 5 interactive, dynamically injected CSS themes with high-contrast text and ambient background gradients. |
| **🔧 Corrected Errors** | - **Dependency Conflicts:** Stripped official `google-generativeai` packages that crashed on Python 3.14 protobufs, pivoting successfully to robust raw REST API `requests`.<br>- **Vercel Limits:** Relocated the 503 retry logic deeply into the `generateContent` function so it protects Vercel serverless functions without hitting 10s timeouts.<br>- **Accessibility & SEO:** Patched missing iframe titles, canonical links, and `<meta robots>` tags to eliminate Lighthouse error rates.<br>- **UX & Contrast:** Fixed unreadable text in light themes, enhanced live validation status, and sped up API generation by switching to the `gemini-1.5-flash-8b` model.<br>- **Validation & Icons:** Fixed a bug where missing names generated empty portfolios by enforcing strict AND validation logic. Resolved disappearing SVG icons (GitHub/LinkedIn) by removing inline styles, using CSS classes, and delaying Lucide rendering to avoid race conditions. |

---
<div align="right">
  <i>Log finalized in compliance with strict UI/UX and project brief guidelines.</i>
</div>
