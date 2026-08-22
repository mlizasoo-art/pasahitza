from pathlib import Path
import re
import shutil
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('ad-exposed-preview')
source_dir = Path('site-assets/ad-exposed/ramp-context')

RAMPS = [
    {
        'page': 'AdExposed-Ramp1-Recruit-Briefing.dc.html',
        'number': '01',
        'file': 'ramp1-context.jpg',
        'src': './assets/ramp1-context.jpg',
        'alt': 'SIGNAL briefing room with case files and an investigation board',
    },
    {
        'page': 'AdExposed-Ramp2-Decode-Briefing.dc.html',
        'number': '02',
        'file': 'ramp2-context.jpg',
        'src': './assets/ramp2-context.jpg',
        'alt': 'Advertising analysis workspace with campaign evidence and persuasion clues',
    },
    {
        'page': 'AdExposed-Ramp3-Expose-Briefing.dc.html',
        'number': '03',
        'file': 'ramp3-context.jpg',
        'src': './assets/ramp3-context.jpg',
        'alt': 'Ethics review workspace examining advertising pressure and representation',
    },
    {
        'page': 'AdExposed-Ramp4-Create-Briefing.dc.html',
        'number': '04',
        'file': 'ramp4-context.jpg',
        'src': './assets/ramp4-context.jpg',
        'alt': 'Creative team developing an honest advertising campaign in a studio',
    },
]

IMAGE_STYLE = "width:100%;height:280px;object-fit:cover;border-radius:12px;border:1px solid rgba(21,23,26,0.18);display:block;"
(root / 'assets').mkdir(parents=True, exist_ok=True)

for cfg in RAMPS:
    source = source_dir / cfg['file']
    target = root / 'assets' / cfg['file']
    if not source.exists() or source.stat().st_size < 5000:
        raise SystemExit(f'Missing or invalid durable ramp asset: {source}')
    shutil.copy2(source, target)

    page = root / cfg['page']
    if not page.exists():
        raise SystemExit(f'Missing Mission Briefing page: {page}')
    text = page.read_text(encoding='utf-8')

    caption = rf'(<div[^>]*>\s*FIELD PHOTO\s*[—-]\s*RAMP\s*{cfg["number"]}\s*</div>)'
    pattern = re.compile(
        rf'(?:<image-slot\b[^>]*>\s*</image-slot>|<img\b[^>]*>)\s*{caption}',
        re.IGNORECASE | re.DOTALL,
    )
    image = (
        f'<img data-ramp-context="{cfg["number"]}" src="{cfg["src"]}" '
        f'alt="{cfg["alt"]}" style="{IMAGE_STYLE}" />\n          '
    )
    text, count = pattern.subn(image + r'\1', text, count=1)
    if count != 1:
        raise SystemExit(f'Could not replace field photo in {cfg["page"]}')

    if f'src="{cfg["src"]}"' not in text or f'data-ramp-context="{cfg["number"]}"' not in text:
        raise SystemExit(f'Context image binding missing in {cfg["page"]}')
    page.write_text(text, encoding='utf-8')

print('RAMP_CONTEXT_IMAGES=PASS')
