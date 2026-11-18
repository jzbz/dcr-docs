#!/usr/bin/env bash
#
# Generate the whitepaper section of the site from its Typst source.
#
#   scripts/build-whitepaper.sh
#
# Writes docs/whitepaper/*.md, docs/whitepaper/decred-whitepaper.pdf and
# docs/css/typst-math.css. All of it is generated and ignored by git;
# run this before `zensical build` or `zensical serve`.
#
# The source is a checkout of https://github.com/jzbz/dcr-whitepaper, looked
# for in this order: $WHITEPAPER_SRC, whitepaper/ in this repository (where
# CI checks it out), ../dcr-whitepaper next to this repository.
#
# The PDF is built from the source as it is. The web pages are built from a
# temporary copy with scripts/whitepaper-web.patch applied: the patch gives
# the template an HTML branch, switched on by `--input web=1`, that emits
# headings, admonitions and figures a web page can use. If the patch stops
# applying after a change to the whitepaper's template, it has to be
# refreshed against the new template.
#
# Needs typst (the version in .typst-version), patch and uv.

set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -n "${WHITEPAPER_SRC:-}" ]; then
	src="$WHITEPAPER_SRC"
elif [ -f "$repo/whitepaper/main.typ" ]; then
	src="$repo/whitepaper"
else
	src="$repo/../dcr-whitepaper"
fi
out="$repo/docs/whitepaper"
css="$repo/docs/css/typst-math.css"

die() {
	echo "build-whitepaper.sh: $*" >&2
	exit 1
}

[ -f "$src/main.typ" ] ||
	die "no whitepaper source at $src (clone https://github.com/jzbz/dcr-whitepaper there, or set WHITEPAPER_SRC)"
src="$(cd "$src" && pwd)"
for tool in typst patch uv; do
	command -v "$tool" >/dev/null 2>&1 || die "$tool is not installed or not on PATH"
done

want="$(cat "$repo/.typst-version")"
have="$(typst --version | awk '{print $2}')"
# The HTML export is experimental and changes between Typst releases.
[ "$have" = "$want" ] || die "typst $have found, but .typst-version says $want"

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

# System fonts are ignored, as in the whitepaper's own build.sh, so the
# result depends only on the fonts in the source tree and built into typst.
flags() { printf '%s\n' --root "$1" --font-path "$1/fonts" --ignore-system-fonts; }

mkdir -p "$out"

echo "whitepaper: $(git -C "$src" rev-parse --short HEAD 2>/dev/null || echo "$src")"

mapfile -t pdf_flags < <(flags "$src")
typst compile "${pdf_flags[@]}" "$src/main.typ" "$out/decred-whitepaper.pdf"

# What the PDF build contains, for html2zensical.py to hold the web build to.
typst eval "${pdf_flags[@]}" --in "$src/main.typ" '(
  rule: query(figure.where(kind: "rule")).len(),
  algorithm: query(figure.where(kind: "algorithm")).len(),
  table: query(figure.where(kind: table)).len(),
  image: query(figure.where(kind: image)).len(),
  "numbered equation": query(math.equation.where(block: true)).filter(e => e.numbering != none).len(),
  chapter: query(heading.where(level: 1)).filter(h => h.numbering != none).len(),
)' >"$work/expect.json"

mkdir "$work/web"
cp -R "$src/." "$work/web/"
rm -rf "$work/web/.git"
patch -d "$work/web" -p1 --quiet --batch --forward --fuzz=0 <"$repo/scripts/whitepaper-web.patch" ||
	die "scripts/whitepaper-web.patch does not apply to $src"

mapfile -t web_flags < <(flags "$work/web")
# Typst warns once for each page-only construct it drops, h() and align().
# The warnings are left visible: a new one is content the web pages may lack.
typst compile "${web_flags[@]}" --features html --format html --input web=1 \
	"$work/web/main.typ" "$work/whitepaper.html" ||
	die "the HTML export failed"

uv run --locked --project "$repo" python "$repo/scripts/html2zensical.py" "$work/whitepaper.html" "$out" \
	--css "$css" --nav "$repo/zensical.toml" --expect "$work/expect.json"
