# marcrleonard.com

My personal website. It's a small static site: `main.py` renders Jinja templates, Markdown posts and a few JSON files into `build/`, and Cloudflare Pages runs that on every push. Make a change here and poof! It's deployed!

## How it deploys

- **Production:** pushes to `master` build and deploy to https://marcrleonard.com.
- **Previews:** any other branch gets its own Cloudflare Pages preview URL, posted as a check on its pull request.
- **Build command:** `./build.sh`, output directory `build/`. It installs [uv](https://docs.astral.sh/uv/) if the image lacks it, then runs `uv run --locked main.py`. uv downloads a prebuilt Python (version from `requires-python` in `pyproject.toml`), so don't set `PYTHON_VERSION` in Cloudflare: that makes the image compile Python from source.
- **Daily rebuild:** `.github/workflows/touch-and-commit.yml` commits `timestamp.txt` once a day, which triggers a fresh build so the Letterboxd movies stay current.

## Building locally

```sh
CF_PAGES=1 uv run main.py           # build with site-relative links, like Cloudflare
python3 -m http.server 8000 -d build
```

Then open http://localhost:8000. Dependencies are in `pyproject.toml` and pinned in `uv.lock`; add one with `uv add <package>`. Without `CF_PAGES=1`, links are prefixed with the `full_url` in `main.py`, which is set up for PyCharm's built-in server at `localhost:63342`.

The build fetches the Letterboxd RSS feed. If it can't reach Letterboxd, the build still succeeds and the movies section shows a link to the profile instead.

## Where the content lives

| What | File |
| --- | --- |
| Blog posts ("odds & ends") | `source/blog/*.md`. Files starting with `_` are skipped. |
| Experience timeline | `source/data/experience.json` |
| Side project cards ("in the hopper") | `source/data/projects.json` |
| Professional skills | `source/data/skills.json` |
| About page bio | `source/_templates/pages/about.html` |
| Home page intro | `source/_templates/pages/home.html` |
| Movies | Letterboxd RSS at build time (`letterboxd.py`) |
| Résumé PDF | `source/assets/Marc_Leonard_SWE_2026.pdf` |

Every JSON file in `source/data/` is available in templates as `data.<file name>`, e.g. `data.experience`.

### Adding a blog post

Copy `source/blog/_template.md`, drop the leading underscore, and fill in the header. The URL becomes `/blog/<year>/<month>/<slug>`, where the slug comes from `Slug:` or, if that's missing, the title lowercased with spaces turned into hyphens.

### Updating the experience timeline

Each job in `experience.json` has a `start` and `end` year. Decimals are fine: `2024.6` is roughly August 2024. Use `"end": null` for a current role; it's drawn in red up to today, and the axis extends itself each year. `kind` is `work` or `school`.

### Updating side projects

Each project in `projects.json` has a name, URL, kind, start year and one-line description. `art` picks the small illustration on top of the card: `timecode`, `bins`, `plot`, or `none`.

## Layout

```
main.py                     build script: posts, pages, RSS, data, asset copy
letterboxd.py               fetches the Letterboxd feed
source/
  _templates/
    page_template.html      base layout: header, nav, footer
    _portrait.html          photo card shared by home and about
    _timeline.html          experience timeline (home and /experience)
    _macros.html            post list, project cards, profile links and icons
    _blog.html              a single blog post
    rss.xml                 the RSS feed
    pages/                  home, about, experience, odds & ends, résumé
  css/
    site.css                all site styles
    pygment.css             code highlighting colors, scoped to .highlight
  data/                     experience, projects, skills
  blog/                     Markdown posts
  img/, assets/             images and the résumé PDF
```

Nav items and their pages are listed in `pages_nav` in `main.py`.

## Design notes

- Swiss look: Inter, one red (`#da291c`), dotted red link underlines, lowercase nav. All colors are tokens at the top of `site.css`, with a dark-mode set.
- Pages switch with a plain crossfade (cross-document view transitions). The header stays put, and so does the photo card between home and about. Browsers without view transitions just navigate normally, and reduced-motion settings turn the animation off.

## Posts todo

- TimecodeTool
- Asset Veranda
