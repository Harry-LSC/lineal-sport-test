from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

s = s.replace('An archive of championships that can only change hands by defeating the reigning champion.','A championship archive that changes hands by defeating the reigning champion.')
s = s.replace('<a href="#rules">How it works</a><a href="cricket.html">Cricket</a>','<a href="#full-rules">How it works</a><a href="cricket.html">Cricket</a>')
s = s.replace('<p class="hero-copy">An archive of championships that can only change hands by <strong>defeating the reigning champion.</strong></p>','<p class="hero-copy">A championship archive that changes hands by defeating the reigning champion.</p>')
s = s.replace('<section aria-labelledby="rulesTitle" id="rules">','<section aria-labelledby="rulesTitle" id="quick-rules">')
s = s.replace('An independent historical project, not affiliated with any governing body, league or club.','An independent project, not affiliated with any governing body, league or club.')

css = '''
<style id="lsc-full-rules">
.full-rules-section{padding:4px 0 6px;scroll-margin-top:86px}
.full-rules-panel{border:1px solid var(--line);border-radius:7px;background:linear-gradient(180deg,rgba(14,29,41,.82),rgba(7,19,29,.92));padding:34px 38px 30px;margin-top:34px}
.full-rules-head{text-align:center;max-width:820px;margin:0 auto 26px}
.full-rules-eyebrow{font:600 13px/1.1 "Cormorant Garamond",serif;letter-spacing:.09em;text-transform:uppercase;color:var(--gold-bright);margin-bottom:7px}
.full-rules-title{font:600 34px/1.05 "Cormorant Garamond",serif;color:var(--cream);margin:0}
.full-rules-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 34px;border-top:1px solid var(--line-soft)}
.full-rule{display:grid;grid-template-columns:34px minmax(0,1fr);gap:13px;padding:19px 0;border-bottom:1px solid var(--line-soft)}
.full-rule-num{font:600 18px/1 "Cormorant Garamond",serif;color:var(--gold-bright);padding-top:2px}
.full-rule h3{font:600 18px/1.15 "Cormorant Garamond",serif;color:var(--cream);margin:0 0 5px}
.full-rule p{font-size:12.6px;line-height:1.55;color:#b7b2a8;margin:0;text-align:justify;text-justify:inter-word}
.full-rules-note{font-size:11.5px;line-height:1.55;color:#8f9497;margin:20px 0 0;text-align:center}
@media(max-width:760px){.full-rules-panel{padding:26px 20px 22px}.full-rules-grid{grid-template-columns:1fr}.full-rules-title{font-size:30px}.full-rule{grid-template-columns:30px minmax(0,1fr)}}
</style>
'''
if 'id="lsc-full-rules"' not in s:
    s = s.replace('</head>', css + '\n</head>')

rules = '''
<section class="full-rules-section" id="full-rules" aria-labelledby="fullRulesTitle">
<div class="full-rules-panel">
<div class="full-rules-head">
<div class="full-rules-eyebrow">How it works</div>
<h2 class="full-rules-title" id="fullRulesTitle">The complete rules</h2>
</div>
<div class="full-rules-grid">
<div class="full-rule"><div class="full-rule-num">01</div><div><h3>Seed</h3><p>Every lineage starts from a defined inaugural event. For international match formats, the winner of the first official match is the seed champion. For tournament or season-based competitions, the winner of the inaugural tournament or season is the seed.</p></div></div>
<div class="full-rule"><div class="full-rule-num">02</div><div><h3>Transfer</h3><p>The championship changes hands when the reigning holder is defeated in an official match. The winner becomes the new champion.</p></div></div>
<div class="full-rule"><div class="full-rule-num">03</div><div><h3>Defence</h3><p>A holder victory is a successful defence. A draw or tie also leaves the championship with the holder and counts as a defence.</p></div></div>
<div class="full-rule"><div class="full-rule-num">04</div><div><h3>No result and abandonment</h3><p>If a match produces no official winner and no completed draw or tie result, the holder keeps the championship but no successful defence is added.</p></div></div>
<div class="full-rule"><div class="full-rule-num">05</div><div><h3>Official tiebreaks</h3><p>If the competition uses an official tiebreak, such as a Super Over or penalty shoot-out, the official winner is treated as the match winner. The title transfers if the holder loses that tiebreak.</p></div></div>
<div class="full-rule"><div class="full-rule-num">06</div><div><h3>Dormancy</h3><p>Inactivity never strips the title. A championship can remain dormant for months or years and stays with its holder until that holder next loses an eligible match.</p></div></div>
</div>
<p class="full-rules-note">Individual championship pages may include a format-specific note where the sport requires an additional convention.</p>
</div>
</section>

'''
marker = '<a class="ring-easter-egg" href="one-ring.html"'
if 'id="full-rules"' not in s:
    s = s.replace(marker, rules + marker)

p.write_text(s, encoding='utf-8')
