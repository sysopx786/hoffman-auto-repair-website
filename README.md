# Dave Hoffman Auto Repair: static site

Plain HTML/CSS/JS. No framework, no tracking, no build dependency beyond Python 3.

- `python3 src/build.py` regenerates every page, `sitemap.xml`, `robots.txt`, `404.html`.
- Content: `src/services.json` (categories, services, FAQs), `src/site.config.json` (name, phone, hours, domain, flags).
- Fonts: Bricolage Grotesque and Inter, self-hosted variable woff2 (SIL OFL).
- Deploy: push the folder to GitHub Pages (or any static host). `.nojekyll` included. All links are relative.
- Preview: `python3 -m http.server 8000`.
- Logo: `assets/img/logo-dimensional-*.webp` (original art), `logo-flat*.svg` (traced), `logo.py` approach in release report.
- Read `LAUNCH-BLOCKERS.md` before going live.

## Links

| Link | URL | Status |
|---|---|---|
| Private preview | https://claude.ai/artifact/JTFztkLL9nYaVxe5HMD2No | Opens for the owner only. Share from the page's Share menu. |
| Public site | https://sysopx786.github.io/hoffman-auto-repair-website/ | Live only after GitHub Pages is enabled (Settings → Pages → branch `main`, folder `/`). Not confirmed enabled. |
| Repository | https://github.com/sysopx786/hoffman-auto-repair-website | |

The public URL has a path prefix, so `404.html` (which uses `<base href="/">`) works only on a custom domain at the root.
