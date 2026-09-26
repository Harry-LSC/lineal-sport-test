#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(".tennis-page-src")
targets={
    ROOT/"mens":"mens-tennis.html",
    ROOT/"womens":"womens-tennis.html",
}

for src_dir,out_name in targets.items():
    parts=sorted(src_dir.glob("*.part"))
    if not parts:
        raise SystemExit(f"No source chunks found in {src_dir}")
    text="".join(p.read_text(encoding="utf-8") for p in parts)
    if "<!doctype html>" not in text.lower():
        raise SystemExit(f"{out_name}: missing doctype")
    if "workbook-driven live update overlay" not in text:
        raise SystemExit(f"{out_name}: live update overlay missing")
    if "PIPELINE TEST DATA · NOT LIVE" in text or "Test Challenger" in text:
        raise SystemExit(f"{out_name}: synthetic test data leaked into publication preview")
    Path(out_name).write_text(text,encoding="utf-8")
    print(f"Built {out_name}: {len(parts)} chunks, {len(text):,} characters")
