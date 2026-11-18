#!/usr/bin/env python3
"""Split Typst's single-file HTML export of the whitepaper into Zensical pages.

    html2zensical.py WHITEPAPER.html OUT_DIR --css FILE [--nav zensical.toml]
                     [--expect FILE]

One Markdown page is written per chapter (each <h2> of the export), plus an
index page holding the abstract. Headings become Markdown headings, so the
table of contents, permalinks and search sections work as on any other page.
Everything between two headings is passed through as a raw HTML block.

A link whose target is in another chapter is rewritten to point at that
chapter's page. The stylesheet Typst embeds for its MathML output is written
to --css. With --nav, the pages listed under whitepaper/ in zensical.toml
must be exactly the pages written. With --expect, the element counts of the
export must equal the counts in FILE, which build-whitepaper.sh takes from
the PDF build of the same source.
"""

import argparse
import html
import json
import os
import re
import sys
import tomllib

PDF_NAME = "decred-whitepaper.pdf"

HEADING = re.compile(r'<h([2-6])(?: id="([^"]+)")?>(.*?)</h\1>', re.S)

MD_ACTIVE = re.compile(r"[\\`*_{}\[\]()#+\-.!|^~=:/<>]")


def fail(message):
    sys.exit(f"html2zensical: {message}")


def page_name(chapter):
    """File name stem and title of a chapter, from its <h2>.

    The stem is the chapter number (or appendix letter) and the name part of
    the heading's label: `<h2 id="ch:subsidy">11 Issuance ...` gives
    `11-subsidy`. Labels are stable, so the stems are too. The one heading
    without a label is the reference list.
    """
    m = re.match(r'<h2(?: id="([^"]+)")?>(.*?)</h2>', chapter, re.S)
    if m is None:
        fail("a chapter does not start with <h2>")
    label, title = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
    if label is None:
        return "references", title
    number = title.split(" ", 1)[0]
    prefix = f"{int(number):02d}" if number.isdigit() else number
    return f"{prefix}-{label.split(':', 1)[-1]}", title


def md_text(fragment):
    """Inline HTML that Markdown renders exactly as it is written.

    Every character Markdown or one of its extensions gives a meaning to is
    written as a character reference in the text between tags, so a heading
    such as `__init__` or `a -> b` is not restyled and keeps its id.
    """
    parts = re.split(r"(<[^>]+>|&#?\w+;)", fragment)
    return "".join(
        p if p.startswith(("<", "&")) and len(p) > 1
        else MD_ACTIVE.sub(lambda m: f"&#{ord(m.group(0))};", p)
        for p in parts
    )


def raw_block(segment):
    """Wrap a run of HTML so that Markdown leaves it alone.

    A blank line ends a raw HTML block in CommonMark-style parsers. The only
    ones in the export are inside <pre>; there the newline before an empty
    or whitespace-only line is written as a character reference instead,
    which renders the same.
    """
    segment = segment.strip()
    if not segment:
        return None
    segment = re.sub(
        r"<pre.*?</pre>",
        lambda m: re.sub(r"\n(?=[^\S\n]*\n)", "&#10;", m.group(0)),
        segment,
        flags=re.S,
    )
    segment = re.sub(r"\n\s*\n", "\n", segment)
    return f'<div class="dcr-wp" markdown="0">\n{segment}\n</div>\n'


def unlink_svg(chunk):
    """Turn the links inside the SVG diagrams into plain groups.

    Zensical's instant navigation assigns to `href` on every link of a page
    it loads. On an SVG <a> that property is read-only, the assignment
    throws, and no page loads from then on until the reader reloads.
    """

    def group(m):
        transform = re.search(r'\stransform="[^"]*"', m.group(1))
        return f"<g{transform.group(0) if transform else ''}>"

    def unlink(svg):
        svg = re.sub(r"<a\b([^>]*)>", group, svg.group(0))
        return svg.replace("</a>", "</g>")

    return re.sub(r"<svg\b.*?</svg>", unlink, chunk, flags=re.S)


def to_markdown(chapter):
    out, pos = [], 0
    for m in HEADING.finditer(chapter):
        block = raw_block(chapter[pos : m.start()])
        if block:
            out.append(block)
        # Typst's h2 is the chapter title, which is the page's h1.
        level = int(m.group(1)) - 1
        attr = f" {{ #{m.group(2)} }}" if m.group(2) else ""
        # A heading may hold inline HTML (code, math); its tags are kept.
        out.append("#" * level + " " + md_text(" ".join(m.group(3).split())) + attr + "\n")
        pos = m.end()
    block = raw_block(chapter[pos:])
    if block:
        out.append(block)
    return "\n".join(out)


def nav_pages(value):
    """Every whitepaper/*.md path in a zensical.toml nav value."""
    if isinstance(value, str):
        return [value] if value.startswith("whitepaper/") else []
    if isinstance(value, dict):
        value = list(value.values())
    return [p for item in value for p in nav_pages(item)]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source")
    ap.add_argument("outdir")
    ap.add_argument("--css", required=True)
    ap.add_argument("--nav")
    ap.add_argument("--expect")
    args = ap.parse_args()

    with open(args.source, encoding="utf-8") as f:
        doc = f.read()
    body = doc[doc.index("<body>") + len("<body>") : doc.rindex("</body>")]

    style = re.search(r"<style>(.*?)</style>", doc, re.S)
    if style is None:
        fail("the export has no <style> element")

    # Typst wraps the reference list, <h2> included, in a <section>. Unwrap
    # it, so the split does not leave its start tag on the page before.
    body = re.sub(
        r'<section role="doc-bibliography">(.*?)</section>', r"\1", body, flags=re.S
    )

    body = unlink_svg(body)

    front, *chapters = re.split(r"(?=<h2[ >])", body)
    if not chapters:
        fail("the export has no <h2>: was it built with --input web=1?")
    pages = [(*page_name(ch), ch) for ch in chapters]
    stems = [stem for stem, _, _ in pages]
    if len(set(stems)) != len(stems):
        fail(f"two chapters share a page name: {stems}")

    if args.expect:
        with open(args.expect, encoding="utf-8") as f:
            expected = json.load(f)
        found = {
            "rule": body.count('class="admonition dcr-rule"'),
            "algorithm": body.count('class="dcr-algorithm"'),
            "table": body.count('<figure class="dcr-table"'),
            "image": len(re.findall(r"<figure(?: id=\"[^\"]+\")?>", body)),
            "numbered equation": body.count('class="dcr-eq"'),
            "chapter": len([p for p in pages if p[0] != "references"]),
        }
        if found != expected:
            wrong = {k: (expected.get(k), found.get(k)) for k in expected | found
                     if expected.get(k) != found.get(k)}
            fail(f"the web build and the PDF build disagree (PDF, web): {wrong}")

    # Which page each id is on. Ids that Typst repeats (glyphs of the inline
    # SVG diagrams) are only ever linked to from their own page.
    ids = {stem: set(re.findall(r' id="([^"]+)"', ch)) for stem, _, ch in pages}
    front_ids = set(re.findall(r' id="([^"]+)"', front))
    owner = {}
    for stem, _, _ in pages:
        for i in ids[stem]:
            owner.setdefault(i, stem)

    unresolved = []

    def relink(stem, chunk):
        def sub(m):
            target = html.unescape(m.group(1))
            if target in ids.get(stem, front_ids):
                return m.group(0)
            page = owner.get(target)
            if page is None:
                unresolved.append(target)
                return m.group(0)
            # Like a Markdown link, this names the source file; Zensical
            # turns it into the page's URL and checks that the target exists.
            return f'href="{page}.md#{m.group(1)}"'

        # Not xlink:href, which the SVG diagrams repeat next to href.
        return re.sub(r'(?<![\w:-])href="#([^"]+)"', sub, chunk)

    os.makedirs(args.outdir, exist_ok=True)
    wanted = {f"{stem}.md" for stem in stems} | {"index.md"}
    for name in os.listdir(args.outdir):
        if name.endswith(".md") and name not in wanted:
            os.remove(os.path.join(args.outdir, name))

    for stem, _, chapter in pages:
        with open(os.path.join(args.outdir, f"{stem}.md"), "w", encoding="utf-8") as f:
            f.write(to_markdown(relink(stem, chapter)))

    index = ["# Decred Technical Whitepaper\n"]
    block = raw_block(relink(None, front))
    if block:
        index.append(block)
    index.append(f"[Download the PDF]({PDF_NAME}){{ .md-button }}\n")
    index.append("## Contents\n")
    index.append("".join(f"- [{title}]({stem}.md)\n" for stem, title, _ in pages))
    with open(os.path.join(args.outdir, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(index))

    os.makedirs(os.path.dirname(os.path.abspath(args.css)), exist_ok=True)
    with open(args.css, "w", encoding="utf-8") as f:
        f.write("/* Generated by scripts/html2zensical.py from Typst's HTML export. */\n")
        f.write(style.group(1).strip() + "\n")

    if unresolved:
        fail(f"{len(unresolved)} links have no target, e.g. {sorted(set(unresolved))[:5]}")

    if args.nav:
        with open(args.nav, "rb") as f:
            listed = nav_pages(tomllib.load(f)["project"].get("nav", []))
        written = ["whitepaper/index.md"] + [f"whitepaper/{stem}.md" for stem in stems]
        if listed != written:
            lines = "".join(f'    "{p}",\n' for p in written)
            fail(
                f"the whitepaper pages in {args.nav} are not the pages just written.\n"
                f'Set the "Whitepaper" entry of nav to:\n'
                f'  {{ "Whitepaper" = [\n{lines}  ] }},'
            )

    print(f"html2zensical: wrote {len(pages) + 1} pages to {args.outdir}")


if __name__ == "__main__":
    main()
