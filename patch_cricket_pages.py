from pathlib import Path

files = [
    'charles-bannerman-belt.html',
    'myrtle-maclagan-medal.html',
    'john-edrich-jug.html',
    'tina-macpherson-trophy.html',
    'rebecca-rolls-ribbon.html',
    'ricky-ponting-ribbon.html',
    'yusuf-pathan-plate.html',
]

plain = '<div class="wrap" style="padding-top:22px"><div style="font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:var(--cricket-bright)">Lineal Sport Championship / Cricket</div></div>'
linked = '<div class="wrap" style="padding-top:22px"><div style="font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:var(--cricket-bright)"><a href="index.html" style="color:inherit;text-decoration:none">Lineal Sport Championship</a> / <a href="cricket.html" style="color:inherit;text-decoration:none">Cricket</a></div></div>'

style = '''\n<style id="lsc-footer-copy-justify">\n.footer-text{\n  text-align:justify;\n  text-justify:inter-word;\n}\n</style>\n'''

for name in files:
    p = Path(name)
    s = p.read_text(encoding='utf-8')
    if plain in s:
        s = s.replace(plain, linked, 1)
    if 'id="lsc-footer-copy-justify"' not in s:
        s = s.replace('</head>', style + '</head>', 1)
    p.write_text(s, encoding='utf-8')
