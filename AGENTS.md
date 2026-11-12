# Silva website working instructions

- Canonical website root: `/Users/loogart/Documents/GitHub/Silva Construction`. Make all future site edits here.
- Continue on the separate `codex/bootstrap5-refactor` branch. Do not commit, push, deploy, merge, or change the live site without explicit user approval.
- Preserve all English/French content, original branding, official logos, plans, media, routes, galleries and GitHub Pages compatibility.
- Use live HTML text for website typography and Nunito Sans. Preserve the French hero’s red circumflex and red period. Official logos and plans stay supplied artwork.
- Corners: 8px controls, 10px cards/photos, 12px large panels. Clip backgrounds and all four exposed corners consistently. Maintain common page-title spacing.
- Use real vector icons, preferably inline SVG with currentColor. Do not use Unicode or emoji arrows for interface icons.
- `.refactor/` holds local comparison snapshots, review screenshots, audit reports and tools; it is ignored by Git and must never be published. One-time migration scripts must not be rerun over edited pages.
- Start comparison: `python3 .refactor/tools/preview.py`; preview `http://localhost:8765/bootstrap/index.html`, comparison `/review/`. The bootstrap preview alias serves the repository root.
- Forms still need an approved delivery endpoint; missing source PDFs are required before enabling plan downloads.
