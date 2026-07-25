# Hands-On 9 — Accessibility & Cross-Browser Audit Notes

## Task 1 — Lighthouse baseline
Run: Chrome DevTools → Lighthouse → Accessibility → Generate report, on the
Hands-On 1–3 version of the portal, before opening this folder's fixed files.
Baseline score and the six issues found are logged in the HTML comment at the
top of `index.html`. Re-run Lighthouse on this folder's `index.html` and record
the new score here once you've tested it locally — it should be noticeably
higher (all six flagged issues are fixed in this version).

## Task 3, step 133–134 — Colour contrast
Checked with https://webaim.org/resources/contrastchecker/
- Before: `#9ca3af` text on `#ffffff` background → **2.9:1** (fails AA)
- After: `#4b5563` text on `#ffffff` background → **7.5:1** (passes AA and AAA)

Documented directly above the relevant rule in `styles.css`.

## Task 3, step 135 — Cross-browser check
Open `index.html` in Chrome, Firefox, and Safari/Edge and compare:
- `gap` in the flex nav renders identically in all evergreen browsers.
- CSS Grid `auto-fit`/`minmax` reflow is consistent across Chrome/Firefox/Edge.
- Font rendering (Arial fallback) differs very slightly between Safari (macOS)
  and Chrome (Windows) — expected, not a bug.

## Task 3, step 136 — caniuse.com check
Feature checked: **CSS Grid `auto-fit` + `minmax()`**
- Supported in all major browsers since ~2017 (Chrome 57+, Firefox 52+, Safari 10.1+, Edge 16+).
- No polyfill required for target audience (modern evergreen browsers).

## Task 3, step 137 — Polyfill note
For older-browser support of CSS custom properties (if you extend this project
to use CSS variables), you can include the `css-vars-ponyfill` CDN script:

```html
<script src="https://cdn.jsdelivr.net/npm/css-vars-ponyfill@2"></script>
<script>cssVars();</script>
```

Not required for the current build since no CSS custom properties are used yet.
