from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('ad-exposed-preview')

RAMPS = [
    {
        'page': 'AdExposed-Ramp1-Recruit-Briefing.dc.html',
        'number': '01',
        'src': './assets/ramp1-context.jpg',
        'alt': 'SIGNAL briefing room with case files and an investigation board',
    },
    {
        'page': 'AdExposed-Ramp2-Decode-Briefing.dc.html',
        'number': '02',
        'src': './assets/ramp2-context.jpg',
        'alt': 'Advertising analysis workspace with campaign evidence and persuasion clues',
    },
    {
        'page': 'AdExposed-Ramp3-Expose-Briefing.dc.html',
        'number': '03',
        'src': './assets/ramp3-context.jpg',
        'alt': 'Ethics review workspace examining advertising pressure and representation',
    },
    {
        'page': 'AdExposed-Ramp4-Create-Briefing.dc.html',
        'number': '04',
        'src': './assets/ramp4-context.jpg',
        'alt': 'Creative team developing an honest advertising campaign in a studio',
    },
]

IMAGE_STYLE = "width:100%;height:280px;object-fit:cover;border-radius:12px;border:1px solid rgba(21,23,26,0.18);display:block;"

for cfg in RAMPS:
    page = root / cfg['page']
    if not page.exists():
        raise SystemExit(f'Missing Mission Briefing page: {page}')
    text = page.read_text(encoding='utf-8')

    # Replace the single field-photo element immediately before the existing
    # caption. This removes the old embedded R1 artwork and the R2-R4
    # <image-slot> placeholders without changing the surrounding layout.
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
        # Source pages sometimes use title case for the caption; the regex is
        # case-insensitive, so reaching this point means the layout contract
        # really changed and we should fail rather than silently publish old art.
        raise SystemExit(f'Could not replace field photo in {cfg["page"]}')

    if f'src="{cfg["src"]}"' not in text:
        raise SystemExit(f'Context image source missing in {cfg["page"]}')
    if f'data-ramp-context="{cfg["number"]}"' not in text:
        raise SystemExit(f'Context image marker missing in {cfg["page"]}')
    page.write_text(text, encoding='utf-8')

print('RAMP_CONTEXT_IMAGES=PASS')
