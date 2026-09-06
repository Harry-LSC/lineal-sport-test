from pathlib import Path
for name in ['index.html','cricket.html']:
    p=Path(name)
    s=p.read_text(encoding='utf-8')
    s=s.replace('mailto:?subject=Lineal%20Sport%20Championship%20correction','mailto:linealsportchamp@gmail.com?subject=Lineal%20Sport%20Championship%20correction')
    p.write_text(s,encoding='utf-8')
