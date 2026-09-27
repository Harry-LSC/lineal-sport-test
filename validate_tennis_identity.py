#!/usr/bin/env python3
import json,re
from pathlib import Path

A=json.loads(Path("data/tennis-player-aliases.json").read_text(encoding="utf-8"))["scopes"]
R=Path("tennis-identity-runtime.js").read_text(encoding="utf-8")
m=re.search(r"const ALIASES=(\{.*?\});\n const clone=",R,re.S)
if not m or json.loads(m.group(1)) != A:
    raise SystemExit("Identity runtime and alias registry are out of sync")

def c(t,n):
    m=re.search(rf"(?m)^const {re.escape(n)} = (.*);$",t)
    if not m:
        raise SystemExit("missing "+n)
    return json.loads(m.group(1))

expected_examples={
    "MEN":{
        "Ilie Năstase":{"reigns":20,"days":428,"defences":123},
        "Carlos Moyá":{"reigns":11,"days":34,"defences":8},
        "Marcelo Ríos":{"reigns":3,"days":13,"defences":5},
    }
}

for scope,path,tx,df,mt,rg in [
    ("MEN","mens-tennis.html",1610,4072,5682,1611),
    ("WOMEN","womens-tennis.html",1087,3381,4468,1088),
]:
    t=Path(path).read_text(encoding="utf-8")
    if "tennis-identity-runtime.js" not in t or f"LSC_applyCanonicalTennisIdentity('{scope}'" not in t:
        raise SystemExit(scope+" identity hook missing")
    ar=c(t,"FULL_ARCHIVE_DATA")
    ch=c(t,"CHAMPION_DATA")
    assert len(ar["transfers"])==tx
    assert len(ar["defences"])==df
    assert len(ar["transfers"])+len(ar["defences"])==mt
    assert sum(int(x.get("reigns",0)) for x in ch)==rg

    grouped={}
    for x in ch:
        p=A[scope].get(x["player"],x["player"])
        g=grouped.setdefault(p,{"reigns":0,"days":0,"defences":0})
        for k in g:
            g[k]+=int(x.get(k,0) or 0)
    assert sum(x["reigns"] for x in grouped.values())==rg
    for alias in A[scope]:
        assert alias not in grouped, f"{scope}: alias survived canonical holder grouping: {alias}"

    for player,exp in expected_examples.get(scope,{}).items():
        assert grouped.get(player)==exp, f"{scope}: aggregate mismatch for {player}: {grouped.get(player)} != {exp}"

    dates=[x.get("date","") for x in ar["transfers"] if x.get("date")]
    assert dates==sorted(dates), f"{scope}: transfer chronology is not ascending"

    print(f"{scope}: PASS — {tx} transfers, {df} defences, {mt} title matches, {rg} reigns, {len(grouped)} canonical holders")

print("COMBINED: PASS — 10,150 title-match records preserved.")
print("IDENTITY: PASS — approved alias registry, representative merged holder totals, and transfer chronology verified.")
