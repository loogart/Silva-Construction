# Silva Construction — Bootstrap 5 static website

This repository is the canonical working copy for all Silva website changes as of November 12, 2026. The current refactor is on `codex/bootstrap5-refactor`, uncommitted. No push, deployment, or domain change has been made.

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

For a change across every page, edit the relevant `maintenance/fr-header.partial`, `en-header.partial`, `fr-footer.partial`, or `en-footer.partial`. Preserve `{{root}}` at the start of internal paths. From the repository root run:

```sh
python3 .refactor/tools/shared-layout.py apply
```

This writes complete headers and footers into the existing HTML pages while preserving each page's language-switch destination. Alternatively, edit a page's own header/footer directly. Run `python3 .refactor/tools/shared-layout.py export` only when intentionally refreshing the shared templates from the two homepages.

## Layout and galleries

Use Bootstrap `row g-0` and `col-md-6`, `col-md-4`, or `col-md-12` for new columns. `md` matches the original 768px stacking threshold. Preserve existing descriptive section classes to retain their spacing and background treatments. The `surface-*` classes correspond to existing page-local background styles in each page's `<head>`.

To add a gallery photo, duplicate a `.single-realisation-image` block, set the link to the full-size source file, and set its image source and meaningful `alt` text. Keep `data-lightbox` on the anchor. The gallery provides next/previous, keyboard arrows, Escape, swipe, a slideshow, and an original-file link. For a model carousel duplicate a `.carousel-item`; only the initial item gets `active`.

## Local comparison

From the repository root:

```sh
python3 .refactor/tools/preview.py
```

Open `http://localhost:8765/review/`. Select any existing page and compare at desktop, tablet, or phone width. The comparison's original snapshot is unchanged. Its server blocks external scripts so reviewing does not trigger analytics, chat, or CAPTCHA requests. Google Fonts and embedded maps still require internet access.

## Contact forms and external services

The exported site's 22 forms point to a WordPress REST API absent from a static host. The refactor preserves all visible fields, labels, options, and validation, and clearly indicates that preview submissions cannot send. It never displays a false success message.

Before launch, connect an approved static-compatible form endpoint and test delivery for both languages. This is the outstanding functional dependency; GitHub Pages itself cannot receive form submissions. No third-party service or recipient has been selected on the user's behalf.

The original Tawk chat embed is retained, restricted to `silvaconstruction.ca` and `www.silvaconstruction.ca`. Its account availability has not been verified and it stays off during local review. The source's obsolete Universal Analytics and WordPress/CAPTCHA runtime code are removed. Choosing a replacement analytics property is outside this refactor.

## GitHub Pages

The repository root is the static site root. All runtime files and page links are relative, including deep routes, so it supports a domain root or a project subpath. Keep `.nojekyll`, `CNAME`, icons, and original routes. Comparison snapshots, screenshots and review tools are in the ignored `.refactor/` folder and must never be committed or published. No hosting workflow, deployment trigger, or Git remote has been added. Publishing requires explicit user approval.

## Verification

The local `.refactor/review/audit.json` records page counts, content parity, original media integrity, and local link checks. `.refactor/review/pages.json` lists every page. The migration utility is a one-time tool; do not rerun it after editing pages because it regenerates from the original snapshot.

## Current visual exploration

The November refinement adds inset hero copy, a CSS crop that hides the photo’s baked-in white frame without altering its source file, 8–12px corner radii on selected surfaces, a consistent globe/language control, smaller utility navigation, and better mobile copy spacing. These adjustments live at the end of `assets/css/custom.css`. `.refactor/tools/refine-design.py` is a one-time migration aid; regular page edits remain build-free. The local `.refactor/first-refactor/` directory retains the initial refactor for comparison.

## Final bilingual polish and typography

`assets/css/polish.css` carries the common inner-page spacing, typography, surfaces, galleries, forms, and footer styling. Its shared rules apply to both languages. The hero headlines are real HTML text in the site's Nunito Sans typeface. The French `â` is an actual accented character; a clipped duplicate of its font glyph colours only the circumflex red. The period is an actual text character in a red span. Both headlines remain selectable, accessible, and editable in their homepage HTML.

Official Silva and accreditation logos and architectural plan/render artwork remain the supplied originals, as requested. Photo dimensions are declared to reduce layout shifts; gallery covers load eagerly, and subsequent photos load lazily. The full-size gallery images stay local and unchanged.

The final review checks every page at 1440px and 390px, with screenshots under the local `.refactor/review/final-desktop/` and `.refactor/review/final-mobile/` folders. The result manifest is `.refactor/review/final-checks.json`.

The source export contained 30 invalid image slots pointing to HTML instead of images (29 gallery slots and one carousel slide). Those non-images were removed, retaining all valid photos and original media files. Gallery covers were renumbered so the first valid photograph receives the same full-width treatment on every project page.

The 20 plan-download buttons also pointed back to their own pages, and no original PDFs were supplied. They now clearly indicate an unavailable download and provide the existing phone number to request the plan. Supply the original PDFs and replace the disabled buttons with real relative PDF links before enabling downloads. Forms still require an approved delivery service before publication. Language controls were completed on 10 source pages that omitted them: confirmed translated counterparts are used where available, otherwise the control explicitly identifies the other-language homepage.

The preview server injects a local screenshot-readiness helper. It is outside the publishable folder and is never included in a deployed page.

## Construction-focused corner and title system

The current corner scale is 8px for controls, 10px for cards and photography, and 12px for large sections. Primary page titles share the same 90% content grid. The title-to-rule gap is 20px on desktop and 16px on mobile, with 28px/24px before supporting copy. Title sections use 48px/32px of top spacing. These shared rules are at the end of `assets/css/polish.css`. The 262 page-size checks for this adjustment are in the local `.refactor/review/corners-spacing-checks.json`.

### Complete surface corner pass

All exposed section-fill panels share a 12px clipped outer surface. Homepage model cards use a three-column grid (one column on mobile), 16px gaps and 10px corners, avoiding clipping by the page frame. Editorial photos use 10px corners; supplied plans and official logos remain unchanged. The 131-page desktop/mobile surface audit is saved in `.refactor/review/surface-corners-audit.json` (262 checks, no uncovered surface or horizontal overflow findings).
