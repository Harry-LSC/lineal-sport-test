#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

PAGES=["index.html","tennis.html","mens-tennis.html","womens-tennis.html"]

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs=[]
        self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a and a["id"]:
            self.ids.add(a["id"])
        if tag=="a" and a.get("href") is not None:
            self.refs.append(("href",a["href"]))
        for attr in ("src","href"):
            if tag in ("script","img","link","source") and a.get(attr):
                self.refs.append((attr,a[attr]))

def parse(path):
    s=Scan()
    s.feed(Path(path).read_text(encoding="utf-8"))
    return s

scans={p:parse(p) for p in PAGES}
errors=[]
internal=0
anchors=0
external=0

for page,scan in scans.items():
    for kind,raw in scan.refs:
        ref=(raw or "").strip()
        if not ref or ref.startswith(("mailto:","tel:","javascript:","data:")):
            continue
        u=urlsplit(ref)
        if u.scheme in ("http","https") or ref.startswith("//"):
            external+=1
            continue
        internal+=1
        path=unquote(u.path)
        frag=unquote(u.fragment)
        if path in ("","./"):
            target=page
        elif path=="/":
            target="index.html"
        elif path.startswith("/"):
            target=path.lstrip("/")
        else:
            target=str((Path(page).parent / path).as_posix())
        target=target.split("?")[0]
        tp=Path(target)
        if not tp.exists():
            errors.append(f"{page}: missing local target {ref!r} -> {target!r}")
            continue
        if frag and tp.suffix.lower() in (".html",".htm"):
            anchors+=1
            target_scan=scans.get(target) or parse(target)
            if frag not in target_scan.ids:
                errors.append(f"{page}: missing anchor #{frag} in {target}")
if errors:
    raise SystemExit("\n".join(errors))
print(f"LINKS: PASS — checked {internal} static internal links/assets across {len(PAGES)} publication pages, including {anchors} fragment targets.")
print(f"EXTERNAL REFERENCES: {external} discovered; intentionally not treated as build dependencies.")
