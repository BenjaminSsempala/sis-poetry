#!/usr/bin/env python3
"""Add a lesson to the Crane and Dove Poetry site, or update one that is already there.

    python3 add_lesson.py path/to/lesson.html --id sweep-it-clean --title "Sweep It Clean" \
        --week 8 --dates "26 to 30 Oct" --icon "🧹" \
        --about "One short line for the lesson card"

It copies the page to lessons/<id>/index.html, adds the home button and the offline helper,
keeps the page out of search engines, updates lessons.json and refreshes the offline cache.
Then commit and push (or upload) as usual.
"""
import argparse
import json
import pathlib
import re
import time

SITE = pathlib.Path(__file__).resolve().parent
START, END = "<!-- sis-poetry:home -->", "<!-- /sis-poetry:home -->"
SNIPPET = f"""{START}
<a href="../../" id="sisHome" title="All lessons" aria-label="All lessons" style="position:fixed;left:12px;top:12px;z-index:2147483647;width:54px;height:54px;border-radius:50%;background:rgba(255,255,255,.92);box-shadow:0 4px 0 rgba(0,0,0,.14);display:flex;align-items:center;justify-content:center;font-size:28px;line-height:1;text-decoration:none">🏠</a>
<script>if ("serviceWorker" in navigator) navigator.serviceWorker.register("../../sw.js", {{ scope: "../../" }}).catch(function () {{}});</script>
{END}"""
NOINDEX = '<meta name="robots" content="noindex">'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", type=pathlib.Path, help="the finished lesson HTML file")
    ap.add_argument("--id", required=True, help="short folder name, letters, numbers and hyphens")
    ap.add_argument("--title", required=True)
    ap.add_argument("--week", required=True, type=int)
    ap.add_argument("--dates", default="")
    ap.add_argument("--icon", default="📖")
    ap.add_argument("--about", default="")
    args = ap.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.id):
        ap.error("--id must be lowercase letters, numbers and hyphens")

    html = args.page.read_text(encoding="utf-8")
    html = re.sub(re.escape(START) + ".*?" + re.escape(END) + r"\n?", "", html, flags=re.S)
    if NOINDEX not in html:
        html = html.replace("<head>", "<head>\n" + NOINDEX, 1)
    cut = html.rfind("</body>")
    if cut < 0:
        ap.error("the page has no </body> tag")
    html = html[:cut] + SNIPPET + "\n" + html[cut:]

    dest = SITE / "lessons" / args.id / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")

    index = SITE / "lessons.json"
    lessons = json.loads(index.read_text(encoding="utf-8")) if index.exists() else []
    entry = {"id": args.id, "title": args.title, "week": args.week, "dates": args.dates,
             "icon": args.icon, "about": args.about, "path": f"lessons/{args.id}/"}
    lessons = [l for l in lessons if l["id"] != args.id] + [entry]
    lessons.sort(key=lambda l: (-l["week"], l["title"]))
    index.write_text(json.dumps(lessons, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sw = SITE / "sw.js"
    sw.write_text(re.sub(r'const VERSION = "[^"]*";', f'const VERSION = "{time.strftime("%Y-%m-%d-%H%M%S")}";', sw.read_text()))
    print(f"added {args.title} -> {dest.relative_to(SITE)} ({dest.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
