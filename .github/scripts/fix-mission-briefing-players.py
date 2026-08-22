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
        'sha256': 'b19d54fe8c52a29039fb5f8c6c491bfd4fec75bbde21ffe4f47ea344c95046ec',
        'size': 682153,
    },
    {
        'page': 'AdExposed-Ramp3-Expose-Briefing.dc.html',
        'audio_id': 'AD-EXPOSE-R3-INTRO-EXPOSE-TRACK01',
        'player_id': 'mb03-transmission-audio',
        'title': 'MB-03 · RAMP 03 · EXPOSE · Ethics Division Reviewer — Mission Briefing',
        'src': './assets/ethics-division-reviewer-expose-briefing.mp3',
        'accent': '#6FC4B0',
        'sha256': '5dea6401b75f145edc545191c960918df1ca360467b33f5b92513b72d7384ddc',
        'size': 711828,
    },
    {
        'page': 'AdExposed-Ramp4-Create-Briefing.dc.html',
        'audio_id': 'AD-EXPOSE-R4-INTRO-CREATE-TRACK01',
        'player_id': 'mb04-transmission-audio',
        'title': 'MB-04 · RAMP 04 · CREATE · The Client — Final Commission',
        'src': './assets/the-client-final-commission.mp3',
        'accent': '#F0996E',
        'sha256': '362fc4df4290734b5b275bd2f30d22a74dd8d525832b6d1e02203e60c80b270b',
        'size': 690512,
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

from mission_briefing_transcripts import apply_transcript_gates
apply_transcript_gates(root)

from mission_transcript_runtime_repair import repair_transcript_runtimes
repair_transcript_runtimes(root)
