# Silva Construction — Bootstrap 5 static website

This is an uncommitted local review copy. The repository in `/Users/loogart/Documents/GitHub/Silva Construction` is unchanged. No push, deployment, or domain change has been made.

## Edit a page

Open that page's `index.html` and edit its text, links, or image paths. The existing French and English addresses have been preserved: French starts at `index.html`; English starts at `en/index.html`. The site contains 66 French pages and 65 English pages, reflecting the source export. Existing translations and language-switch destinations are retained, including any source translation gaps.

Each page is complete static HTML. There is no CMS, database, installation, or build command required to publish or edit page content. Keep the corresponding other-language page updated when changing copy. The language links in the header identify its partner.

## Where things live

- `assets/css/custom.css`: small shared visual adjustments, responsive behavior, and SVG icons.
- `assets/css/silva-theme.css`: readable, reduced Silva styling extracted from the source. The original branding, breakpoints, spacing, and surfaces are retained.
- `assets/vendor/`: local Bootstrap 5.3.8 grid, modal/carousel/collapse CSS, and JavaScript bundle. The full vendor stylesheet is retained as a reference but not loaded, so its global typography reset does not change Silva's design.
- `assets/js/main.js`: menus, sticky header, Bootstrap lightbox, slideshow, keyboard and swipe controls, and form preview behavior.
- `wp-content/uploads/`: original photos, plans, logos, and other media; filenames stay unchanged to avoid broken links. Full-size source files are preserved without recompression or artificial upscaling.
- `maintenance/`: shared French/English headers and footers as `.partial` files; these are editing aids, not runtime dependencies.

## Shared navigation and footer

For a change across every page, edit the relevant `maintenance/fr-header.partial`, `en-header.partial`, `fr-footer.partial`, or `en-footer.partial`. Preserve `{{root}}` at the start of internal paths. From the parent `website-refactor` folder run:

```sh
python3 tools/shared-layout.py apply
```

This writes complete headers and footers into the existing HTML pages while preserving each page's language-switch destination. Alternatively, edit a page's own header/footer directly. Run `python3 tools/shared-layout.py export` only when intentionally refreshing the shared templates from the two homepages.

## Layout and galleries

Use Bootstrap `row g-0` and `col-md-6`, `col-md-4`, or `col-md-12` for new columns. `md` matches the original 768px stacking threshold. Preserve existing descriptive section classes to retain their spacing and background treatments. The `surface-*` classes correspond to existing page-local background styles in each page's `<head>`.

To add a gallery photo, duplicate a `.single-realisation-image` block, set the link to the full-size source file, and set its image source and meaningful `alt` text. Keep `data-lightbox` on the anchor. The gallery provides next/previous, keyboard arrows, Escape, swipe, a slideshow, and an original-file link. For a model carousel duplicate a `.carousel-item`; only the initial item gets `active`.

## Local comparison

From the parent `website-refactor` folder:

```sh
python3 tools/preview.py
```

Open `http://localhost:8765/review/`. Select any existing page and compare at desktop, tablet, or phone width. The comparison's original snapshot is unchanged. Its server blocks external scripts so reviewing does not trigger analytics, chat, or CAPTCHA requests. Google Fonts and embedded maps still require internet access.

## Contact forms and external services

The exported site's 22 forms point to a WordPress REST API absent from a static host. The refactor preserves all visible fields, labels, options, and validation, and clearly indicates that preview submissions cannot send. It never displays a false success message.

Before launch, connect an approved static-compatible form endpoint and test delivery for both languages. This is the outstanding functional dependency; GitHub Pages itself cannot receive form submissions. No third-party service or recipient has been selected on the user's behalf.

The original Tawk chat embed is retained, restricted to `silvaconstruction.ca` and `www.silvaconstruction.ca`. Its account availability has not been verified and it stays off during local review. The source's obsolete Universal Analytics and WordPress/CAPTCHA runtime code are removed. Choosing a replacement analytics property is outside this refactor.

## GitHub Pages

The contents of this `bootstrap` directory are the static site root. All runtime files and page links are relative, including deep routes, so it supports a domain root or a project subpath. Keep `.nojekyll`, `CNAME`, icons, and original routes. The comparison and tools sit outside the publishable folder. No hosting workflow, deployment trigger, or Git remote has been added. Publishing requires explicit user approval.

## Verification

The parent `review/audit.json` records page counts, content parity, original media integrity, and local link checks. `review/pages.json` lists every page. The migration utility is a one-time tool; do not rerun it after editing pages because it regenerates from the original snapshot.
