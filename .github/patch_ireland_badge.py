from pathlib import Path
import base64, hashlib, re

TARGETS = [
    "cricket.html",
    "charles-bannerman-belt.html",
    "myrtle-maclagan-medal.html",
    "john-edrich-jug.html",
    "tina-macpherson-trophy.html",
    "rebecca-rolls-ribbon.html",
    "ricky-ponting-ribbon.html",
    "yusuf-pathan-plate.html",
]
ASSET = Path("ireland-cricket.png")
EXPECTED_SHA256 = "83ef32525c8a0cfb2c42e419ab2339c40f9175fd1178f659d0a42e676ff42e2b"
BADGE_SVG = '<image href="ireland-cricket.png" x="0" y="0" width="60" height="36" preserveAspectRatio="xMidYMid meet"/>'
TRICOLOUR = re.compile(
    r'<rect\s+width=["\']20["\']\s+height=["\']36["\']\s+fill=["\']#169B62["\']\s*/>'
    r'\s*<rect\s+x=["\']20["\']\s+width=["\']20["\']\s+height=["\']36["\']\s+fill=["\']#(?:fff|ffffff)["\']\s*/>'
    r'\s*<rect\s+x=["\']40["\']\s+width=["\']20["\']\s+height=["\']36["\']\s+fill=["\']#FF883E["\']\s*/>',
    re.I,
)

payload_paths = [Path(f'.github/ireland-payload-{i:02d}') for i in range(11)] + [
    Path('.github/ireland-payload-11a'), Path('.github/ireland-payload-11b')
]
payload = ''.join(p.read_text(encoding='ascii').strip() for p in payload_paths)
if len(payload) != 47416:
    raise SystemExit(f"Approved Ireland badge payload length mismatch: {len(payload)}")
raw = base64.b64decode(payload, validate=True)
actual = hashlib.sha256(raw).hexdigest()
if actual != EXPECTED_SHA256:
    raise SystemExit(f"Approved Ireland badge hash mismatch: {actual}")
ASSET.write_bytes(raw)

summary = []
for name in TARGETS:
    p = Path(name)
    if not p.exists():
        raise SystemExit(f"Missing target: {name}")
    s = p.read_text(encoding="utf-8")
    before = s
    s, tri_count = TRICOLOUR.subn(BADGE_SVG, s)
    emoji_count = s.count("🇮🇪")
    s = s.replace("🇮🇪", "☘️")
    if tri_count < 1:
        raise SystemExit(f"No Ireland tricolour renderer found in {name}; refusing silent partial patch")
    if "Ireland" not in s or "ireland-cricket.png" not in s:
        raise SystemExit(f"Ireland badge reference missing after patch in {name}")
    p.write_text(s, encoding="utf-8")
    summary.append((name, tri_count, emoji_count, len(s) - len(before)))

for name in TARGETS:
    s = Path(name).read_text(encoding="utf-8")
    bad = [token for token in ("169B62", "FF883E", "🇮🇪") if token.lower() in s.lower()]
    if bad:
        raise SystemExit(f"Forbidden Ireland tricolour token(s) remain in {name}: {bad}")

print("Ireland badge patch complete")
for row in summary:
    print(f"{row[0]}: badge renderers={row[1]}, share emoji fallbacks={row[2]}, byte_delta={row[3]}")
print(f"Asset sha256={actual} bytes={len(raw)}")
