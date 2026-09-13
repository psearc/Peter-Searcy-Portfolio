# Peter Searcy — Portfolio

Personal portfolio site. AI automations & marketing.

**Live:** https://<your-username>.github.io/peter-searcy-portfolio/

## Deploy on GitHub Pages (free)

1. Create a new **public** repo on GitHub (e.g. `peter-searcy-portfolio`).
2. Upload `index.html`, `.nojekyll`, and `README.md` to the repo root.
3. Go to **Settings → Pages**.
4. Under *Source*, choose **Deploy from a branch**; branch `main`, folder `/ (root)`. Save.
5. Wait ~1 minute. Your site is live at the URL above.

### Custom domain (optional)

Buy a domain, then in **Settings → Pages → Custom domain** enter it (e.g. `petersearcy.com`)
and add these DNS records at your registrar:

| Type  | Name | Value |
|-------|------|-------|
| A     | @    | 185.199.108.153 |
| A     | @    | 185.199.109.153 |
| A     | @    | 185.199.110.153 |
| A     | @    | 185.199.111.153 |
| CNAME | www  | `<your-username>.github.io` |

Then tick **Enforce HTTPS**.

## Files

- `index.html` — the entire site, self-contained. No build step, no dependencies, works offline.
- `.nojekyll` — tells GitHub Pages to serve the files as-is.

## Editing

`index.html` is compiled output — don't hand-edit it. Ask for changes to the source
and re-export.

## Contact

petersearcy7@gmail.com · (609) 481-5717 · linkedin.com/in/peter-searcy
