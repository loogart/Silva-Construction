# Silva Construction — static mirror

A fully static copy of silvaconstruction.ca, processed to run with no server,
no database, and no callbacks to the original host. Ready for GitHub Pages,
Cloudflare Pages, or Netlify.

## What was fixed
- **Lazy-loaded images** rewritten to load directly (the original used a
  JavaScript loader that pointed every image back at the live server; those
  references are now local and the loader is neutralized).
- **All internal links** converted to relative paths — navigation works at any
  domain root or locally.
- **WordPress `?p=` shortlinks** remapped to their pretty-URL pages.
- **Accented filenames** duplicated in composed (NFC) form so they resolve on
  case/byte-sensitive Linux hosting like GitHub Pages.
- **Favicons** regenerated from the site's existing favicon source.
- **Dead WordPress cruft** removed (REST API, RSS feeds, oembed, emoji config).
- `.nojekyll` added so GitHub Pages serves all folders untouched.

The only remaining reference to the original domain is the contact email
address, which is intentional.

## Deploy to GitHub Pages
1. Create a new repository.
2. Copy the entire contents of this folder into the repo root (including the
   hidden `.nojekyll` file).
3. Commit and push.
4. Repo Settings -> Pages -> Source: deploy from branch, root.
5. It will publish at `https://USERNAME.github.io/REPONAME/`.

### Important: links are relative, so serve from a domain root
Internal links use relative paths, which work perfectly when the site is served
from the root of a domain (a custom domain, or a `USERNAME.github.io` user/org
repo). If you publish to a *project* repo it serves from
`USERNAME.github.io/REPONAME/` (a subpath) — relative links still resolve
because they're depth-aware, so this also works. Either is fine.

## Custom domain (silvaconstruction.ca)
When you're ready to point the real domain here:
1. Add a file named `CNAME` at the repo root containing one line:
   `www.silvaconstruction.ca`
2. At whoever controls the DNS, point the domain at GitHub Pages
   (CNAME to `USERNAME.github.io`, or the four A records GitHub documents).

Confirm who controls the domain registration BEFORE cancelling the old host —
losing the domain is worse than losing the server.

## Local preview
    python3 -m http.server 8080
then open http://localhost:8080

## Note on size
~350 MB, mostly full-resolution project photos. Within GitHub Pages limits, but
the images could be compressed substantially later to speed up load times.
