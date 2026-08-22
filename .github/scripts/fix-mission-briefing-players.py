from pathlib import Path
import hashlib
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('ad-exposed-preview')

BRIEFINGS = [
    {
        'page': 'AdExposed-Ramp2-Decode-Briefing.dc.html',
        'audio_id': 'AD-EXPOSE-R2-INTRO-DECODE-TRACK01',
        'player_id': 'mb02-transmission-audio',
        'title': 'MB-02 · RAMP 02 · DECODE · Dr. Lena Vasquez — Mission Briefing',
        'src': './assets/dr-lena-vasquez-decode-briefing.mp3',
        'accent': '#7EB6E8',
        'sha256': 'efa58b1b3d699702cbe28e29f1bec0f5dbc103a69d476c4419e69dd8b2560cd2',
        'size': 698871,
    },
    {
        'page': 'AdExposed-Ramp3-Expose-Briefing.dc.html',
        'audio_id': 'AD-EXPOSE-R3-INTRO-EXPOSE-TRACK01',
        'player_id': 'mb03-transmission-audio',
        'title': 'MB-03 · RAMP 03 · EXPOSE · Dr. Lena Vasquez — Mission Briefing',
        'src': './assets/dr-lena-vasquez-expose-ethics-briefing.mp3',
        'accent': '#6FC4B0',
        'sha256': 'b5576a0deb5b3326d5115339459f236ccd98b58df18628bb7b5a8e08a9645d01',
        'size': 756132,
    },
    {
        'page': 'AdExposed-Ramp4-Create-Briefing.dc.html',
        'audio_id': 'AD-EXPOSE-R4-INTRO-CREATE-TRACK01',
        'player_id': 'mb04-transmission-audio',
        'title': 'MB-04 · RAMP 04 · CREATE · The Client — Final Commission',
        'src': './assets/the-client-final-commission.mp3',
        'accent': '#F0996E',
        'sha256': '704776e139803b2b1f48c5de300848725655febb7fd4de5a6cd216f7dd6c3e84',
        'size': 710992,
    },
]


def verify_asset(cfg):
    asset = root / cfg['src'].removeprefix('./')
    if not asset.exists():
        raise SystemExit(f"Missing Mission Briefing asset: {asset}")
    data = asset.read_bytes()
    if len(data) != cfg['size']:
        raise SystemExit(f"Wrong size for {asset}: {len(data)}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != cfg['sha256']:
        raise SystemExit(f"Wrong SHA-256 for {asset}: {digest}")


def webb_style_card(cfg):
    return f'''      <div data-audio-id="{cfg['audio_id']}" style="margin-top:22px;background:#15171A;border-radius:12px;padding:22px 26px;">
        <div style="display:flex;align-items:baseline;gap:10px;">
          <span style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:{cfg['accent']};">{cfg['title']}</span>
        </div>
        <audio id="{cfg['player_id']}" controls="{{{{ true }}}}" src="{cfg['src']}" style="width:100%;margin-top:14px;outline:none;"></audio>
      </div>'''


for cfg in BRIEFINGS:
    verify_asset(cfg)
    page = root / cfg['page']
    if not page.exists():
        raise SystemExit(f"Missing Mission Briefing page: {page}")
    text = page.read_text(encoding='utf-8')

    # Replace the entire generated intro card, not only the audio tag. This
    # deliberately mirrors the known-working Webb card structure, including
    # the DC boolean binding controls="{{ true }}".
    pattern = re.compile(
        rf'      <div data-audio-id="{re.escape(cfg["audio_id"])}"[\s\S]*?</audio>\s*</div>',
        re.M,
    )
    card = webb_style_card(cfg)
    text, count = pattern.subn(card, text, count=1)
    if count != 1:
        raise SystemExit(f"Could not replace Mission Briefing card in {cfg['page']}")

    if f'controls="{{{{ true }}}}"' not in text:
        raise SystemExit(f"DC controls binding missing in {cfg['page']}")
    if f'src="{cfg["src"]}"' not in text:
        raise SystemExit(f"Audio source missing in {cfg['page']}")
    if re.search(r'<audio[^>]*\sautoplay(?:\s|=|>)', text, re.I):
        raise SystemExit(f"Autoplay detected in {cfg['page']}")

    page.write_text(text, encoding='utf-8')

print('MISSION_BRIEFING_PLAYER_PARITY=PASS')
