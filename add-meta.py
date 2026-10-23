#!/usr/bin/env python3
"""Add the page title and share-preview tags to a bundled index.html.

The design tool exports index.html with the title "Bundled Page" and no
Open Graph tags, so LinkedIn and other sites can't build a link preview.
Run this after every re-export:

    python3 add-meta.py index.html

It writes the tags in two places:
  - the outer <head>, which is what crawlers (LinkedIn, Slack, iMessage) read;
  - the bundled template's <head>, which replaces the outer document once the
    page unpacks, so the browser tab keeps the right title.

Running it twice is safe: the block between the markers is replaced.
"""
import html
import json
import re
import sys

URL = "https://psearc.github.io/Peter-Searcy-Portfolio/"
TITLE = "Peter Searcy — AI Automation Specialist"
DESCRIPTION = (
    "AI automation specialist building voice agents, chatbots, and n8n "
    "workflows. Seven years in paid social and lead generation. Open to "
    "remote, full-time roles."
)
IMAGE = URL + "og-image.png"

START, END = "<!-- share-meta:start -->", "<!-- share-meta:end -->"


def meta_block():
    t, d = html.escape(TITLE), html.escape(DESCRIPTION)
    return "\n".join([
        START,
        f"<title>{t}</title>",
        f'<meta name="description" content="{d}">',
        f'<link rel="canonical" href="{URL}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:url" content="{URL}">',
        f'<meta property="og:title" content="{t}">',
        f'<meta property="og:description" content="{d}">',
        f'<meta property="og:image" content="{IMAGE}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="627">',
        f'<meta property="og:image:alt" content="{t}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{t}">',
        f'<meta name="twitter:description" content="{d}">',
        f'<meta name="twitter:image" content="{IMAGE}">',
        END,
    ])


def strip_old(text, start, end):
    return re.sub(r"[ \t]*" + re.escape(start) + r".*?" + re.escape(end), "", text, flags=re.S)


def enc(s):
    # The bundled template is a JSON string inside <script type="__bundler/template">,
    # with "</" written as "</" so it can't close the script tag early.
    return json.dumps(s, ensure_ascii=False)[1:-1].replace("</", "<\\u002F")


def main(path):
    src = open(path, encoding="utf-8").read()
    block = meta_block()

    # Remove a previous run's blocks: the template copy first (anchored to the
    # template's <head> and ending in an escaped "\n"), then the outer one.
    head = r'(<script type="__bundler/template">\s*"<!DOCTYPE html>\\n<html><head>\\n)'
    out = re.sub(head + re.escape(enc(START)) + r".*?" + re.escape(enc(END + "\n")),
                 r"\1", src, count=1, flags=re.S)
    out = strip_old(out, START, END + "\n")

    # Outer document: drop the exporter's placeholder title, then insert after <meta charset>.
    out = re.sub(r"\s*<title>Bundled Page</title>", "", out, count=1)
    charset = re.search(r'<meta charset="utf-8">\n', out)
    if not charset:
        sys.exit("no <meta charset> in outer <head>")
    out = out[:charset.end()] + "  " + block.replace("\n", "\n  ") + "\n" + out[charset.end():]

    # Bundled template: insert right after its <head>.
    tpl = re.search(head, out)
    if not tpl:
        sys.exit("bundled template <head> not found")
    out = out[:tpl.end()] + enc(block + "\n") + out[tpl.end():]

    open(path, "w", encoding="utf-8").write(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "index.html")
