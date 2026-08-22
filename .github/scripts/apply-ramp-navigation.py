from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('ad-exposed-preview')

RAMPS = {
    'Ramp1-Recruit': {
        'label': 'RAMP 01 · RECRUIT',
        'overview_label': 'Ramp 01 overview',
        'briefing': 'AdExposed-Ramp1-Recruit-Briefing.dc.html',
    },
    'Ramp2-Decode': {
        'label': 'RAMP 02 · DECODE',
        'overview_label': 'Ramp 02 overview',
        'briefing': 'AdExposed-Ramp2-Decode-Briefing.dc.html',
    },
    'Ramp3-Expose': {
        'label': 'RAMP 03 · EXPOSE',
        'overview_label': 'Ramp 03 overview',
        'briefing': 'AdExposed-Ramp3-Expose-Briefing.dc.html',
    },
    'Ramp4-Create': {
        'label': 'RAMP 04 · CREATE',
        'overview_label': 'Ramp 04 overview',
        'briefing': 'AdExposed-Ramp4-Create-Briefing.dc.html',
    },
}

# The UI arrow is a hierarchical parent link, never browser history.
# This prevents cycles such as Listening -> Mission Briefing -> Listening.
SPECIAL_ROUTES = {
    'AdExposed-Ramp1-Recruit-LanguageFile.dc.html': {
        'parent': 'AdExposed-Ramp1-Recruit-Practice.dc.html',
        'back_label': 'Extra Practice',
        'ramp_label': 'RAMP 01 · RECRUIT',
    },
    'AdExposed-Ramp1-Recruit-WhoWhatWhom.dc.html': {
        'parent': 'AdExposed-Ramp1-Recruit-Practice.dc.html',
        'back_label': 'Extra Practice',
        'ramp_label': 'RAMP 01 · RECRUIT',
    },
    'AdExposed-Ramp1-Recruit-Drill.dc.html': {
        'parent': 'AdExposed-Ramp1-Recruit-LanguageFile.dc.html',
        'back_label': 'Language File',
        'ramp_label': 'RAMP 01 · RECRUIT',
    },
}

REQUIRED_MAIN = []
for prefix in RAMPS:
    for suffix in ('Briefing', 'Listening', 'Practice', 'Checkpoint'):
        REQUIRED_MAIN.append(f'AdExposed-{prefix}-{suffix}.dc.html')


def ramp_cfg(name: str):
    for prefix, cfg in RAMPS.items():
        if f'AdExposed-{prefix}-' in name:
            return cfg
    return None


def route_for(name: str):
    if name in SPECIAL_ROUTES:
        return SPECIAL_ROUTES[name]

    cfg = ramp_cfg(name)
    if not cfg:
        return None

    if name == cfg['briefing']:
        return {
            'parent': 'AdExposed-Hub.dc.html',
            'back_label': 'AD EXPOSE home',
            'ramp_label': cfg['label'],
        }

    if any(name.endswith(f'-{suffix}.dc.html') for suffix in ('Listening', 'Practice', 'Checkpoint')):
        return {
            'parent': cfg['briefing'],
            'back_label': cfg['overview_label'],
            'ramp_label': cfg['label'],
        }

    return None


def nav_block(route: dict) -> str:
    return f'''  <div data-ramp-back-nav="v2" style="max-width:1120px;margin:0 auto;padding:14px 48px 0;display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;">
    <a href="{route['parent']}" data-ramp-parent-link aria-label="Go to {route['back_label']}" style="display:inline-flex;align-items:center;gap:7px;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;color:#15171A;border:1px solid rgba(21,23,26,.18);border-radius:999px;padding:8px 12px;background:#fff;">← {route['back_label']}</a>
    <div style="display:flex;align-items:center;gap:12px;">
      <span style="font-family:'IBM Plex Mono',monospace;font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:#6B6A63;">{route['ramp_label']}</span>
      <a href="AdExposed-Hub.dc.html" data-ramp-hub-link style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.07em;text-transform:uppercase;color:#6B6A63;">All ramps</a>
    </div>
  </div>
'''


def insert_before_subtabs(text: str, block: str) -> tuple[str, bool]:
    subtabs_token = '<sc-for list="{{ subTabs }}" as="tab"'
    container_marker = '  <div style="max-width:1120px;margin:0 auto;padding:0 48px;">'
    tabs_index = text.find(subtabs_token)
    if tabs_index < 0:
        return text, False
    insert_at = text.rfind(container_marker, 0, tabs_index)
    if insert_at < 0:
        return text, False
    return text[:insert_at] + block + '\n' + text[insert_at:], True


def insert_secondary(text: str, block: str, name: str) -> tuple[str, bool]:
    # RECRUIT's nested exercise pages do not own the four section tabs. Their main
    # content starts at padding:22px; insert immediately before that content block.
    markers = {
        'AdExposed-Ramp1-Recruit-WhoWhatWhom.dc.html': '  <div style="max-width:900px;margin:0 auto;padding:22px 48px 90px;">',
        'AdExposed-Ramp1-Recruit-Drill.dc.html': '  <div style="max-width:760px;margin:0 auto;padding:22px 48px 90px;">',
    }
    marker = markers.get(name)
    if not marker:
        return text, False
    insert_at = text.find(marker)
    if insert_at < 0:
        return text, False
    return text[:insert_at] + block + '\n' + text[insert_at:], True


patched = []
for path in sorted(root.glob('AdExposed-Ramp*.dc.html')):
    route = route_for(path.name)
    if not route:
        continue

    text = path.read_text(encoding='utf-8')
    if 'data-ramp-back-nav="v1"' in text or 'data-ramp-back-nav="v2"' in text:
        raise SystemExit(f'Ramp navigation already present before deterministic pass: {path.name}')
    if 'document.referrer' in text or 'window.history.back()' in text:
        raise SystemExit(f'History-based back navigation leaked into source before pass: {path.name}')

    block = nav_block(route)
    text, inserted = insert_before_subtabs(text, block)
    if not inserted:
        text, inserted = insert_secondary(text, block, path.name)
    if not inserted:
        raise SystemExit(f'Could not place deterministic parent navigation in {path.name}')

    if text.count('data-ramp-back-nav="v2"') != 1:
        raise SystemExit(f'Expected one deterministic navigation strip in {path.name}')
    if f'href="{route["parent"]}" data-ramp-parent-link' not in text:
        raise SystemExit(f'Wrong parent route in {path.name}')
    if f'>← {route["back_label"]}</a>' not in text:
        raise SystemExit(f'Wrong parent label in {path.name}')
    if 'data-ramp-hub-link' not in text:
        raise SystemExit(f'Missing All ramps escape hatch in {path.name}')

    path.write_text(text, encoding='utf-8')
    patched.append(path.name)

# Core route contract: 4 ramps x 4 learner sections.
for name in REQUIRED_MAIN:
    path = root / name
    if not path.exists():
        raise SystemExit(f'Missing required ramp page: {name}')
    text = path.read_text(encoding='utf-8')
    route = route_for(name)
    if 'data-ramp-back-nav="v2"' not in text:
        raise SystemExit(f'Deterministic navigation missing from {name}')
    if f'href="{route["parent"]}" data-ramp-parent-link' not in text:
        raise SystemExit(f'Parent mismatch in {name}')

# Nested RECRUIT routes are also explicit and must never rely on browser history.
for name, route in SPECIAL_ROUTES.items():
    path = root / name
    if not path.exists():
        raise SystemExit(f'Missing nested learner page: {name}')
    text = path.read_text(encoding='utf-8')
    if 'data-ramp-back-nav="v2"' not in text:
        raise SystemExit(f'Nested deterministic navigation missing from {name}')
    if f'href="{route["parent"]}" data-ramp-parent-link' not in text:
        raise SystemExit(f'Nested parent mismatch in {name}')

# DECODE retains the second navigation level inside Listening Practice.
r2 = (root / 'AdExposed-Ramp2-Decode-Listening.dc.html').read_text(encoding='utf-8')
if 'data-listening-index="v1"' not in r2:
    raise SystemExit('DECODE Gold listening library disappeared during navigation pass')
if r2.count('data-listening-back') < 4:
    raise SystemExit('DECODE activity-to-library controls disappeared during navigation pass')

# The site-level arrow must never become browser-history navigation again.
for path in root.glob('AdExposed-Ramp*.dc.html'):
    text = path.read_text(encoding='utf-8')
    if 'data-ramp-back-runtime=' in text or 'document.referrer' in text or 'window.history.back()' in text:
        raise SystemExit(f'History-driven route detected after navigation pass: {path.name}')

print(f'RAMP_NAVIGATION_V2=PASS pages={len(patched)} deterministic_parent_routes={len(REQUIRED_MAIN) + len(SPECIAL_ROUTES)}')
