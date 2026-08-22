from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('ad-exposed-preview')
page = root / 'AdExposed-Ramp2-Decode-Listening.dc.html'
if not page.exists():
    raise SystemExit(f'Missing DECODE Listening Practice page: {page}')

text = page.read_text(encoding='utf-8')

# 2026-08-22 source/content amendment.
# Mars/Saxophonist is an advertisement built around music + a spoken slogan rather
# than a clean short sung brand phrase. Jacob's Club is historically defensible as
# a jingle, but its extended song-like execution is a weaker teaching exemplar for
# the specific distinction used in DECODE: a short, catchy advertising tune/phrase.
# Calgon and Autoglass make that distinction immediately audible.
replacements = {
    'data-listening-gold="v1"': 'data-listening-gold="v1.1"',
    'Mars Bar · Jacob’s Club · Chicken Tonight · WeBuyAnyCar.com':
        'Calgon · Autoglass · Chicken Tonight · WeBuyAnyCar.com',
    '>Mars Bar</div>': '>Calgon</div>',
    'https://www.hatads.org.uk/catalogue/record/e2c54d1f-40bc-479a-a3cc-aff7f46a3bee':
        'https://www.youtube.com/watch?v=3FY0k3hLIAk',
    'data-jingle-response="mars"': 'data-jingle-response="calgon"',
    '>Jacob\'s Club</div>': '>Autoglass</div>',
    'https://www.doyouremember.co.uk/memory/club-biscuits':
        'https://www.youtube.com/watch?v=zvnvN2F1Rm4',
    'data-jingle-response="club"': 'data-jingle-response="autoglass"',
}

for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f'Expected Jingle Lab token not found: {old}')
    text = text.replace(old, new)

# Give the two replacement clips a more precise service/product prompt while keeping
# the activity construct unchanged: identify category, notice memorability, compare.
text = text.replace(
    'data-jingle-response="calgon" placeholder="Product type"',
    'data-jingle-response="calgon" placeholder="Product type / purpose"',
    1,
)
text = text.replace(
    'data-jingle-response="autoglass" placeholder="Product type"',
    'data-jingle-response="autoglass" placeholder="Service type"',
    1,
)

required = [
    'data-listening-gold="v1.1"',
    'Calgon · Autoglass · Chicken Tonight · WeBuyAnyCar.com',
    '>Calgon</div>',
    'https://www.youtube.com/watch?v=3FY0k3hLIAk',
    '>Autoglass</div>',
    'https://www.youtube.com/watch?v=zvnvN2F1Rm4',
    '>Chicken Tonight</div>',
    'https://www.youtube.com/watch?v=x1veMqaPOxo',
    '>WeBuyAnyCar.com</div>',
    'https://www.youtube.com/watch?v=f-yEWZTBQ64',
]
for token in required:
    if token not in text:
        raise SystemExit(f'Amended Jingle Lab token missing: {token}')

for forbidden in [
    'Mars Bar · Jacob’s Club · Chicken Tonight · WeBuyAnyCar.com',
    '>Mars Bar</div>',
    '>Jacob\'s Club</div>',
    'https://www.hatads.org.uk/catalogue/record/e2c54d1f-40bc-479a-a3cc-aff7f46a3bee',
    'https://www.doyouremember.co.uk/memory/club-biscuits',
]:
    if forbidden in text:
        raise SystemExit(f'Superseded Jingle Lab source leaked into learner page: {forbidden}')

if 'D-S10' in text or 'SECURE-LISTENING' in text:
    raise SystemExit('Secure S10 material leaked during Jingle Lab amendment')

page.write_text(text, encoding='utf-8')
print('JINGLE_LAB_SOURCE_AMENDMENT=PASS gold=v1.1 clips=Calgon,Autoglass,ChickenTonight,WeBuyAnyCar')
