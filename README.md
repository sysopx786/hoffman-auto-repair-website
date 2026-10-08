# Dave Hoffman Auto Repair: static site

Plain HTML/CSS/JS. No framework, no tracking, no build dependency beyond Python 3.

- `python3 src/build.py` regenerates every page, `sitemap.xml`, `robots.txt`, `404.html`.
- Content: `src/services.json` (categories, services, FAQs), `src/site.config.json` (name, phone, hours, domain, flags).
- Fonts: Bricolage Grotesque and Inter, self-hosted variable woff2 (SIL OFL).
- Deploy: push the folder to GitHub Pages (or any static host). `.nojekyll` included. All links are relative.
- Preview: `python3 -m http.server 8000`.
- Logo: `assets/img/logo-dimensional-*.webp` (original art), `logo-flat*.svg` (traced), `logo.py` approach in release report.
- Read `LAUNCH-BLOCKERS.md` before going live.
