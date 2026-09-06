from pathlib import Path
p=Path('cricket.html')
s=p.read_text(encoding='utf-8')

s=s.replace('.section-note{max-width:420px;color:#9da8b0;font-size:12px;text-align:right}', '.section-note{max-width:520px;color:#9da8b0;font-size:12px;text-align:right}.section-note-below{margin-top:14px;color:#9da8b0;font-size:12px;text-align:right}')
s=s.replace('.context p{color:#aab4bb;font-size:14px;max-width:740px}', '.context p{color:#aab4bb;font-size:14px;max-width:740px;text-align:justify;text-justify:inter-word}')
s=s.replace('.method-list li{padding:12px 0;border-top:1px solid var(--line);font-size:13px;color:#aab4bb}', '.method-list li{padding:12px 0;border-top:1px solid var(--line);font-size:13px;color:#aab4bb;text-align:justify;text-justify:inter-word}')
s=s.replace('.source-panel p{font-size:12.5px;color:#aab4bb}', '.source-panel p{font-size:12.5px;color:#aab4bb;text-align:justify;text-justify:inter-word}')
s=s.replace('.disclaimer{border-top:1px solid var(--line);padding-top:15px;margin-top:18px;font-size:10.5px;color:#84919b}', '.disclaimer{border-top:1px solid var(--line);padding-top:15px;margin-top:18px;font-size:10.5px;color:#84919b;text-align:justify;text-justify:inter-word}')

s=s.replace('<div class="section-note" id="updatedNote">Days held are calculated automatically from the winning date.</div>', '')
s=s.replace('</div></section>\n<section class="method" id="method">', '<div class="section-note-below" id="updatedNote">Current holders and next defences update automatically from the live championship data.</div></div></section>\n<section class="method" id="method">')

old='<li><b>Dormancy:</b> inactivity does not strip the title. The championship remains with its holder until an eligible defeat transfers it.</li>'
new='<li><b>Dormancy:</b> inactivity does not strip the title. A championship remains with its holder until that holder is defeated in an official match. This can create very long dormant reigns, most notably when South Africa was banned from international cricket from 1970–1991.</li>'
s=s.replace(old,new)

p.write_text(s,encoding='utf-8')
