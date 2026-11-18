# dcr-docs

The source of [docs.dcr.pw](https://docs.dcr.pw/): documentation for Decred
users and developers, and a web edition of the Decred technical whitepaper.
The site is built with [Zensical](https://zensical.org/).

## Layout

| Path | Contents |
| --- | --- |
| `docs/user/` | User docs |
| `docs/dev/` | Developer docs |
| `docs/whitepaper/` | The whitepaper pages. Generated, not in git |
| `scripts/` | The whitepaper build |
| `zensical.toml` | Site configuration and navigation |

## Building

The build needs [uv](https://docs.astral.sh/uv/),
[Typst](https://typst.app/) in the version named in `.typst-version`,
`patch`, and a checkout of the whitepaper next to this repository.

```bash
git clone https://github.com/jzbz/dcr-docs.git
git clone https://github.com/jzbz/dcr-whitepaper.git
cd dcr-docs
uv sync --locked
scripts/build-whitepaper.sh
uv run zensical serve
```

`zensical serve` previews the site at <http://localhost:8000/> and rebuilds
it when a file changes. `uv run zensical build --strict` writes the
site to `site/` and fails on a broken internal link, which is what CI runs.

The Zensical version is fixed by `uv.lock`. To move to a newer one:

```bash
uv lock --upgrade-package zensical
```

## The whitepaper

The whitepaper is written in Typst, in
[jzbz/dcr-whitepaper](https://github.com/jzbz/dcr-whitepaper), and is not
copied into this repository or converted to Markdown by hand.
`scripts/build-whitepaper.sh` builds two things from a checkout of it:

- the PDF, from the source exactly as it is;
- the web pages, from Typst's HTML export. The export is made from a
  temporary copy of the source with `scripts/whitepaper-web.patch` applied.
  The patch adds an HTML branch to the whitepaper's template, and
  `scripts/html2zensical.py` splits the export into one page per chapter.

The script stops if the web build does not contain the same number of
rules, algorithms, tables, figures, numbered equations and chapters as the
PDF build, if a cross-reference has no target, or if the pages it writes are
not the ones listed in the navigation in `zensical.toml`.

The script looks for the checkout in `$WHITEPAPER_SRC`, then in
`whitepaper/` inside this repository, then in `../dcr-whitepaper`.

CI builds from the tip of the whitepaper's default branch, so the site picks
up a whitepaper change the next time it is deployed: on the next push to
`master` here, or when the workflow is run by hand. A change to the
whitepaper's `template.typ` can stop `scripts/whitepaper-web.patch` from
applying, which fails the build until the patch is refreshed against the new
template.

Typst's HTML export is experimental and changes between releases, so a new
Typst version goes into `.typst-version` only after the pages have been
checked with it.

## Deployment

`.github/workflows/docs.yml` builds the site for every pull request and
deploys every push to `master` to GitHub Pages. The custom domain is set in
the repository's Pages settings; no `CNAME` file is used.
