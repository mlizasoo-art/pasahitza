from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('ad-exposed-preview')

RAMPS = {
    'Ramp1-Recruit': {
        'label': 'RAMP 01 · RECRUIT',
        'briefing': 'AdExposed-Ramp1-Recruit-Briefing.dc.html',
    },
    'Ramp2-Decode': {
        'label': 'RAMP 02 · DECODE',
        'briefing': 'AdExposed-Ramp2-Decode-Briefing.dc.html',
    },
    'Ramp3-Expose': {
        'label': 'RAMP 03 · EXPOSE',
        'briefing': 'AdExposed-Ramp3-Expose-Briefing.dc.html',
    },
    'Ramp4-Create': {
        'label': 'RAMP 04 · CREATE',
        'briefing': 'AdExposed-Ramp4-Create-Briefing.dc.html',
    },
}

# The four main learner sections in every ramp must always receive the navigation strip.
REQUIRED = []
for prefix in RAMPS:
    for suffix in ('Briefing', 'Listening', 'Practice', 'Checkpoint'):
        REQUIRED.append(f'AdExposed-{prefix}-{suffix}.dc.html')


def ramp_cfg(name: str):
    for prefix, cfg in RAMPS.items():
        if f'AdExposed-{prefix}-' in name:
            return cfg
    return None


def nav_block(label: str, fallback: str) -> str:
    return f'''  <div data-ramp-back-nav="v1" style="max-width:1120px;margin:0 auto;padding:14px 48px 0;display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;">
    <a href="{fallback}" data-ramp-back aria-label="Go back to the previous AD EXPOSE page" style="display:inline-flex;align-items:center;gap:7px;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;color:#15171A;border:1px solid rgba(21,23,26,.18);border-radius:999px;padding:8px 12px;background:#fff;">← Back</a>
    <div style="display:flex;align-items:center;gap:12px;">
      <span style="font-family:'IBM Plex Mono',monospace;font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:#6B6A63;">{label}</span>
      <a href="AdExposed-Hub.dc.html" data-ramp-hub-link style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.07em;text-transform:uppercase;color:#6B6A63;">All ramps</a>
    </div>
  </div>
'''


runtime = r'''
<script data-ramp-back-runtime="v1">
(() => {
  document.addEventListener('click', event => {
    const back = event.target.closest && event.target.closest('[data-ramp-back]');
    if (!back) return;

    let previous = null;
    try { previous = new URL(document.referrer); } catch (_) {}
    const current = new URL(window.location.href);
    const previousIsAdExposed = previous
      && previous.origin === current.origin
      && previous.pathname.includes('/ad-exposed-preview/')
      && previous.href !== current.href;

    if (previousIsAdExposed) {
      event.preventDefault();
      window.history.back();
    }
  });
})();
</script>
'''


# Insert immediately before the container that owns the four section tabs. We locate
# that container from the subTabs component rather than assuming one exact gap/flex style,
# because RECRUIT and the later ramps have slightly different tab-row CSS.
subtabs_token = '<sc-for list="{{ subTabs }}" as="tab"'
container_marker = '  <div style="max-width:1120px;margin:0 auto;padding:0 48px;">'

patched = []
for path in sorted(root.glob('AdExposed-Ramp*.dc.html')):
    cfg = ramp_cfg(path.name)
    if not cfg:
        continue
    text = path.read_text(encoding='utf-8')
    if 'data-ramp-back-nav="v1"' in text:
        raise SystemExit(f'Ramp back navigation already present before pass: {path.name}')

    tabs_index = text.find(subtabs_token)
    if tabs_index < 0:
        # Secondary R1 drill/language pages may not use the four-tab shell.
        continue
    insert_at = text.rfind(container_marker, 0, tabs_index)
    if insert_at < 0:
        continue

    fallback = 'AdExposed-Hub.dc.html' if path.name == cfg['briefing'] else cfg['briefing']
    block = nav_block(cfg['label'], fallback)
    text = text[:insert_at] + block + '\n' + text[insert_at:]

    if '</body>' not in text:
        raise SystemExit(f'Could not locate </body> in {path.name}')
    text = text.replace('</body>', runtime + '\n</body>', 1)

    if text.count('data-ramp-back-nav="v1"') != 1:
        raise SystemExit(f'Expected one back-navigation strip in {path.name}')
    if text.count('data-ramp-back-runtime="v1"') != 1:
        raise SystemExit(f'Expected one back-navigation runtime in {path.name}')
    if 'data-ramp-hub-link' not in text:
        raise SystemExit(f'Missing All ramps escape hatch in {path.name}')

    path.write_text(text, encoding='utf-8')
    patched.append(path.name)

for name in REQUIRED:
    path = root / name
    if not path.exists():
        raise SystemExit(f'Missing required ramp page: {name}')
    text = path.read_text(encoding='utf-8')
    if 'data-ramp-back-nav="v1"' not in text:
        raise SystemExit(f'Required ramp back navigation missing from {name}')
    if 'data-ramp-back-runtime="v1"' not in text:
        raise SystemExit(f'Required ramp back runtime missing from {name}')

# Preserve the inner Listening Practice hierarchy as a second navigation level.
r2 = (root / 'AdExposed-Ramp2-Decode-Listening.dc.html').read_text(encoding='utf-8')
if 'data-listening-index="v1"' not in r2:
    raise SystemExit('DECODE Gold listening library disappeared during navigation pass')
if r2.count('data-listening-back') < 4:
    raise SystemExit('DECODE detail-to-library back controls disappeared during navigation pass')

print(f'RAMP_NAVIGATION=PASS pages={len(patched)}')
