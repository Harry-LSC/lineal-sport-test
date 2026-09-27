#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
A=json.loads(Path('data/tennis-player-aliases.json').read_text(encoding='utf-8'))['scopes']
R=Path('tennis-identity-runtime.js').read_text(encoding='utf-8')
m=re.search(r'const ALIASES=(\\{.*?\\});\\n const clone=',R,re.S)
if not m or json.loads(m.group(1))!=A: raise SystemExit('Identity runtime and alias registry are out of sync')
def c(t,n):
 m=re.search(rf'(?m)^const {re.escape(n)} = (.*);$',t)
 if not m: raise SystemExit('missing '+n)
 return json.loads(m.group(1))
for scope,path,tx,df,mt,rg in [('MEN','mens-tennis.html',1610,4072,5682,1611),('WOMEN','womens-tennis.html',1087,3381,4468,1088)]:
 t=Path(path).read_text(encoding='utf-8')
 if 'tennis-identity-runtime.js' not in t or f"LSC_applyCanonicalTennisIdentity('{scope}'" not in t: raise SystemExit(scope+' identity hook missing')
 ar=c(t,'FULL_ARCHIVE_DATA'); ch=c(t,'CHAMPION_DATA')
 assert len(ar['transfers'])==tx and len(ar['defences'])==df and tx+df==mt
 assert sum(int(x.get('reigns',0)) for x in ch)==rg
 grouped={}
 for x in ch:
  p=A[scope].get(x['player'],x['player']); grouped[p]=grouped.get(p,0)+int(x.get('reigns',0))
 assert sum(grouped.values())==rg
 print(f'{scope}: PASS — {tx} transfers, {df} defences, {mt} title matches, {rg} reigns, {len(grouped)} canonical holders')
print('COMBINED: PASS — 10,150 title-match records preserved.')
