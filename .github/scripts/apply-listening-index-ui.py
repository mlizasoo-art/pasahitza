from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('ad-exposed-preview')
page = root / 'AdExposed-Ramp2-Decode-Listening.dc.html'
if not page.exists():
    raise SystemExit(f'Missing DECODE Listening Practice page: {page}')

text = page.read_text(encoding='utf-8')

ACTIVITIES = [
    {
        'id': 'D-S5-W01',
        'order': '01',
        'session': 'S05',
        'title': 'Jingle Lab',
        'subtitle': 'Mars Bar · Jacob’s Club · Chicken Tonight · WeBuyAnyCar.com',
        'badge': '4 external clips',
    },
    {
        'id': 'D-S7-01',
        'order': '02',
        'session': 'S07',
        'title': 'Save the Children · Most Shocking Second a Day',
        'subtitle': 'Gist, evidence and ethical-persuasion practice',
        'badge': 'Official film',
    },
    {
        'id': 'D-S8-01',
        'order': '03',
        'session': 'S08',
        'title': 'Dove · Real Beauty Sketches',
        'subtitle': 'Sequence, detail and evidence-comparison practice',
        'badge': 'Official film',
    },
    {
        'id': 'D-S9-W02',
        'order': '04',
        'session': 'S09',
        'title': 'CleanStep SIGNAL Briefing',
        'subtitle': 'Two-listen evidence practice · transcript after first complete listen',
        'badge': 'SIGNAL audio',
    },
]

# The Gold builder must have materialized every canonical public-practice item first.
for activity in ACTIVITIES:
    token = f'data-listening-item="{activity["id"]}"'
    if text.count(token) != 1:
        raise SystemExit(f'Expected exactly one Gold listening item for {activity["id"]}')

if 'data-listening-index="v1"' in text:
    raise SystemExit('Listening index already present before index pass')

cards = []
for activity in ACTIVITIES:
    cards.append(f'''        <button type="button" data-open-listening="{activity['id']}" style="appearance:none;text-align:left;border:1px solid rgba(47,95,130,.22);border-radius:12px;background:#fff;padding:18px;cursor:pointer;min-height:178px;display:flex;flex-direction:column;justify-content:space-between;font-family:'IBM Plex Sans',sans-serif;box-shadow:0 1px 0 rgba(21,23,26,.03);">
          <div>
            <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;">
              <span style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;color:#2F5F82;">{activity['order']} · {activity['session']} · {activity['id']}</span>
              <span style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:.06em;text-transform:uppercase;color:#2F5F82;background:#EEF5FA;border-radius:999px;padding:4px 7px;white-space:nowrap;">{activity['badge']}</span>
            </div>
            <div style="font-weight:700;font-size:18px;line-height:1.25;color:#15171A;margin-top:12px;">{activity['title']}</div>
            <div style="font-size:12.8px;line-height:1.5;color:#6B6A63;margin-top:8px;">{activity['subtitle']}</div>
          </div>
          <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.07em;text-transform:uppercase;color:#2F5F82;margin-top:14px;">Open activity →</div>
        </button>''')

index = '''
      <section data-listening-index="v1" aria-label="DECODE listening activity index" style="margin-top:24px;border:1px solid rgba(47,95,130,.18);border-radius:14px;background:#F7FAFC;padding:22px;">
        <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap;">
          <div>
            <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#2F5F82;">DECODE AUDIO & VIEWING LIBRARY</div>
            <div style="font-family:'IBM Plex Sans',sans-serif;font-weight:700;font-size:20px;color:#15171A;margin-top:5px;">Choose one activity</div>
            <div style="font-family:'IBM Plex Sans',sans-serif;font-size:13px;line-height:1.55;color:#6B6A63;margin-top:5px;">All four public practice activities are visible here. Open one to work with its media and exercise, then return to this library.</div>
          </div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:#6B6A63;">4 activities · 7 media clips</div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:18px;">
''' + '\n'.join(cards) + '''
        </div>
      </section>
'''

first_section = re.search(r'\n\s*<section\s+id="[^"]+"\s+data-listening-item="D-S5-W01"', text)
if not first_section:
    raise SystemExit('Could not locate first DECODE Gold listening section')
text = text[:first_section.start()] + '\n' + index + text[first_section.start():]

# Convert each long activity block into a hidden detail view with a durable back control.
for activity in ACTIVITIES:
    activity_id = re.escape(activity['id'])
    pattern = re.compile(
        rf'(<section\s+id="[^"]+"\s+data-listening-item="{activity_id}")(\s+style="[^"]*">)',
        re.M,
    )
    toolbar = '''
        <div data-listening-detail-toolbar style="padding:11px 18px;border-bottom:1px solid rgba(47,95,130,.12);background:#FBFCFD;">
          <button type="button" data-listening-back style="appearance:none;border:0;background:transparent;padding:4px 0;cursor:pointer;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.07em;text-transform:uppercase;color:#2F5F82;">← All listening activities</button>
        </div>'''
    replacement = rf'\1 data-listening-detail="{activity["id"]}" hidden\2{toolbar}'
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit(f'Could not convert {activity["id"]} to detail view')

runtime = r'''
<script data-listening-index-runtime="v1">
(() => {
  const allowed = ['D-S5-W01', 'D-S7-01', 'D-S8-01', 'D-S9-W02'];
  let active = null;
  let syncing = false;

  const allDetails = () => Array.from(document.querySelectorAll('[data-listening-detail]'));
  const indexNode = () => document.querySelector('[data-listening-index="v1"]');

  const sync = () => {
    if (syncing) return;
    syncing = true;
    const index = indexNode();
    const details = allDetails();
    if (index) {
      const shouldHide = Boolean(active);
      if (index.hidden !== shouldHide) index.hidden = shouldHide;
    }
    details.forEach(detail => {
      const shouldHide = detail.getAttribute('data-listening-detail') !== active;
      if (detail.hidden !== shouldHide) detail.hidden = shouldHide;
    });
    syncing = false;
  };

  const scrollToNode = node => {
    if (!node) return;
    setTimeout(() => node.scrollIntoView({ behavior: 'smooth', block: 'start' }), 0);
  };

  const openActivity = (id, updateUrl = true) => {
    if (!allowed.includes(id)) return;
    active = id;
    sync();
    if (updateUrl) history.replaceState(null, '', '#' + encodeURIComponent(id));
    const target = allDetails().find(detail => detail.getAttribute('data-listening-detail') === id);
    scrollToNode(target);
  };

  const openIndex = (updateUrl = true) => {
    active = null;
    sync();
    if (updateUrl) history.replaceState(null, '', location.pathname + location.search);
    scrollToNode(indexNode());
  };

  document.addEventListener('click', event => {
    const opener = event.target.closest && event.target.closest('[data-open-listening]');
    if (opener) {
      event.preventDefault();
      openActivity(opener.getAttribute('data-open-listening'));
      return;
    }
    const back = event.target.closest && event.target.closest('[data-listening-back]');
    if (back) {
      event.preventDefault();
      openIndex();
    }
  });

  const fromHash = () => {
    let id = '';
    try { id = decodeURIComponent(location.hash.replace(/^#/, '')); } catch (_) {}
    if (allowed.includes(id)) openActivity(id, false);
    else openIndex(false);
  };

  window.addEventListener('hashchange', fromHash);
  const observer = new MutationObserver(() => sync());
  observer.observe(document.documentElement, { childList: true, subtree: true });
  fromHash();
  setTimeout(fromHash, 120);
  setTimeout(fromHash, 500);
})();
</script>
'''

if '</body>' not in text:
    raise SystemExit('Could not locate </body> for Listening index runtime')
text = text.replace('</body>', runtime + '\n</body>', 1)

# Static contract checks.
for activity in ACTIVITIES:
    if f'data-open-listening="{activity["id"]}"' not in text:
        raise SystemExit(f'Missing index entry for {activity["id"]}')
    if f'data-listening-detail="{activity["id"]}" hidden' not in text:
        raise SystemExit(f'Missing hidden detail view for {activity["id"]}')
if text.count('data-listening-back') < 4:
    raise SystemExit('Each DECODE listening detail requires a back control')
if 'data-listening-index-runtime="v1"' not in text:
    raise SystemExit('Listening index runtime missing')
if 'D-S10' in text or 'SECURE-LISTENING' in text:
    raise SystemExit('Secure S10 material leaked into Listening Practice index')

page.write_text(text, encoding='utf-8')
print('DECODE_LISTENING_INDEX_UI=PASS')
