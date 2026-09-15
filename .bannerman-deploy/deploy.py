from pathlib import Path
import base64
import gzip

root = Path(__file__).resolve().parents[1]
chunkdir = root / ".bannerman-deploy"


def restore_html():
    sizes = [12000, 12000, 12000, 12000, 120]
    parts = []
    for i, size in enumerate(sizes, 1):
        p = chunkdir / f"html_{i:02d}.txt"
        text = p.read_text(encoding="utf-8").strip()
        if len(text) < size:
            raise RuntimeError(f"{p.name} too short: {len(text)} < {size}")
        parts.append(text[:size])
    raw = gzip.decompress(base64.b64decode("".join(parts)))
    dest = root / "charles-bannerman-belt.html"
    dest.write_bytes(raw)
    print(dest.name, len(raw))


def restore_xlsx():
    sizes = [12000, 11524]
    parts = []
    for i, size in enumerate(sizes, 1):
        p = chunkdir / f"xlsx_{i:02d}.txt"
        text = p.read_text(encoding="utf-8").strip()
        if len(text) < size:
            raise RuntimeError(f"{p.name} too short: {len(text)} < {size}")
        parts.append(text[:size])
    raw = gzip.decompress(base64.b64decode("".join(parts)))
    dest = root / "LSC_Update_System.xlsx"
    dest.write_bytes(raw)
    print(dest.name, len(raw))


restore_html()
restore_xlsx()
