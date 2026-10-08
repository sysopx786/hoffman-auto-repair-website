# Dave Hoffman Auto Repair website

Static website for Dave Hoffman Auto Repair, 42 Ridge Rd, Phoenixville, PA 19460.
16 pages: Home, Services, 9 service categories, About, Reviews, Contact, Privacy, 404.
Plain HTML, CSS and JS. No framework, cookies, analytics or forms.

**Status: draft. Do not promote it until `LAUNCH-BLOCKERS.md` is cleared with Dave.**

## Links

| | URL | Notes |
|---|---|---|
| Public site | https://sysopx786.github.io/hoffman-auto-repair-website/ | Needs GitHub Pages: Settings → Pages → branch `main`, folder `/ (root)`. |
| Private preview | https://claude.ai/artifact/JTFztkLL9nYaVxe5HMD2No | Owner only. Share from the page's Share menu. |
| Repository | https://github.com/sysopx786/hoffman-auto-repair-website | |

## Edit and rebuild

Requires Python 3. Pages are generated, so edit the sources, not the HTML.

| To change | Edit | Then |
|---|---|---|
| Services, descriptions, FAQs | `src/services.json` | `python3 src/build.py` |
| Phone, hours, address, domain, flags | `src/site.config.json` | `python3 src/build.py` |
| Layout, copy on Home/About/Contact | `src/build.py` | `python3 src/build.py` |
| Styling, behavior | `assets/css/site.css`, `assets/js/site.js` | none |

Preview locally: `python3 -m http.server 8000`, then open http://localhost:8000.

## Before launch

1. Clear `LAUNCH-BLOCKERS.md` with Dave (unconfirmed claims, 31 excluded FAQs, photos, vector logo).
2. Set `baseUrl` in `src/site.config.json` to the real domain. It currently reads `REPLACE-WITH-DOMAIN`, which feeds canonical tags, Open Graph, schema and `sitemap.xml`.
3. Set `basePath` in the same file: `/hoffman-auto-repair-website/` on the GitHub Pages URL, `/` on a custom domain. It only affects `404.html`.
4. Rebuild, commit, push.

## Rules baked into the content

- Phone: 484-921-0715 everywhere; (610) 935-1103 on Contact only.
- Inspections: "Official Pennsylvania inspection station (OIS #T480). OBD emissions testing and trailer inspections. Call to confirm we can inspect your vehicle type."
- No email, star rating, review count, prices, warranties, ASE or founding year until Dave confirms.
- FAQs tagged `[Dave to confirm]`, `[Dave to define]` or `[Likely]` are excluded from the page and the schema (`src/excluded.json`).
- FAQ schema text matches the visible text exactly.

## Layout

```
index.html, <category>/index.html   generated pages
404.html, sitemap.xml, robots.txt   generated
assets/css, assets/js               styles and behavior
assets/fonts                        Bricolage Grotesque, Inter (self-hosted, SIL OFL)
assets/img                          logo, favicon, Open Graph image
src/                                build.py, services.json, site.config.json, excluded.json
src/logo.py                         one-off logo script; reads a local source image path
LAUNCH-BLOCKERS.md                  open items for Dave
RELEASE-REPORT.md                   test results and what was not verified
```

## Test status

See `RELEASE-REPORT.md`. Chromium only. Not tested: Safari, Firefox, a physical Android device, production Lighthouse.
