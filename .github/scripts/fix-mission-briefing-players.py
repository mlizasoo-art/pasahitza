from pathlib import Path
import hashlib
import html
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('ad-exposed-preview')

BRIEFINGS = [
    {
        'page': 'AdExposed-Ramp1-Recruit-Briefing.dc.html',
        'audio_id': 'AD-EXPOSE-R1-WEBB-BRIEFING-TRACK01',
        'player_id': 'mb01-transmission-audio',
        'title': 'MB-01 · RAMP 01 · RECRUIT · Director Webb — Mission Briefing',
        'src': './assets/director-webb-recruit-briefing.mp3',
        'accent': '#FFC340',
        'sha256': '657f76613b76444b538fd6b9371f66ce6ebc84c9fdc34a1d76d35eb2c8795532',
        'size': 955053,
        'transcript': [
            'Recruit, this is Director Webb from SIGNAL Intelligence Unit.',
            'Before you can work on a real case, we need to know your starting point. Your first task is the Initial Level Test. Complete all twenty questions on your own. Some will be easy. Some may not. That is the point. This test is diagnostic. It does not count towards your academic grade.',
            'Then RECRUIT begins.',
            'You will learn to ask the first questions of every advertisement: Who is advertising? What are they promoting? Whom are they trying to reach?',
            'You will investigate the AURÉLIA campaign, identify slogans, claims and media, and prepare for the Agency Entry Test.',
            'One rule: do not guess. Read the evidence.',
            'See through the noise.',
            'Webb out.',
        ],
    },
    {
        'page': 'AdExposed-Ramp2-Decode-Briefing.dc.html',
        'audio_id': 'AD-EXPOSE-R2-INTRO-DECODE-TRACK01',
        'player_id': 'mb02-transmission-audio',
        'title': 'MB-02 · RAMP 02 · DECODE · Dr. Lena Vasquez — Mission Briefing',
        'src': './assets/dr-lena-vasquez-decode-briefing.mp3',
        'accent': '#7EB6E8',
        'sha256': 'b19d54fe8c52a29039fb5f8c6c491bfd4fec75bbde21ffe4f47ea344c95046ec',
        'size': 682153,
        'transcript': [
            'Welcome to DECODE, Analyst. In RECRUIT, you learned the basic parts of an advert. Now you will learn how adverts persuade people.',
            'In this ramp, we will use three simple ideas: emotional, rational and social appeal. Emotional appeal uses feelings. Rational appeal uses facts and reasons.',
            'Social appeal uses groups and popularity. One advert can use more than one appeal. Your job is to find the strongest appeal and explain your answer with evidence.',
        ],
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
        'transcript': [
            'You already know how adverts attract attention and persuade people. Now SIGNAL wants you to ask a harder question. Is the advert fair and responsible?',
            'Some adverts are effective, but they can still cause problems. Other adverts can sell a product and also share a positive message. In EXPOSE, you will look at old adverts, stereotypes, pressure on audiences and one real campaign.',
            'You will ask what the advert shows, who it may affect and if the message is fair. Then you will write a balanced review and use evidence to explain your ideas.',
        ],
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
        'transcript': [
            'You have learned how adverts work. You have checked evidence and judged different campaigns. Now it is time to create.',
            'Your team will invent a product and make an advert for it. Your advert must persuade people, but it must also be honest. Every claim needs good support.',
            'Every important choice needs a reason. You will work as a team, but each person must explain their own work. Make something clear, creative and responsible.',
            'Make something SIGNAL can support.',
        ],
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


def transcript_html(cfg):
    paragraphs = ''.join(
        f'<p style="margin:0 0 12px;font-family:\'IBM Plex Sans\',sans-serif;font-size:14px;line-height:1.7;color:#15171A;">{html.escape(p)}</p>'
        for p in cfg['transcript']
    )
    return f'''      <div id="{cfg['player_id']}-transcript-shell" data-transcript-for="{cfg['audio_id']}" style="margin-top:12px;border:1px solid rgba(21,23,26,0.14);border-radius:10px;padding:14px 16px;background:#FAFAF8;">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;">
          <div>
            <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:#6B6A63;">Transcript</div>
            <div id="{cfg['player_id']}-transcript-status" style="font-family:'IBM Plex Sans',sans-serif;font-size:12.5px;color:#6B6A63;margin-top:4px;">Locked · complete 2 full listens first (0/2)</div>
          </div>
          <button id="{cfg['player_id']}-transcript-button" type="button" disabled style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10.5px;letter-spacing:0.08em;text-transform:uppercase;border:1px solid rgba(21,23,26,0.2);border-radius:6px;background:#fff;color:#8B8A84;padding:9px 13px;cursor:not-allowed;">Read transcript</button>
        </div>
        <div id="{cfg['player_id']}-transcript-panel" style="display:none;margin-top:16px;padding-top:16px;border-top:1px solid rgba(21,23,26,0.12);">
          <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:{cfg['accent']};margin-bottom:12px;">Read + listen again</div>
          {paragraphs}
          <audio id="{cfg['player_id']}-transcript-replay" controls="{{{{ true }}}}" src="{cfg['src']}" style="width:100%;margin-top:6px;outline:none;"></audio>
        </div>
      </div>'''


def briefing_card(cfg):
    return f'''      <div data-audio-id="{cfg['audio_id']}" style="margin-top:22px;background:#15171A;border-radius:12px;padding:22px 26px;">
        <div style="display:flex;align-items:baseline;gap:10px;">
          <span style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:{cfg['accent']};">{cfg['title']}</span>
        </div>
        <audio id="{cfg['player_id']}" controls="{{{{ true }}}}" src="{cfg['src']}" style="width:100%;margin-top:14px;outline:none;"></audio>
      </div>

{transcript_html(cfg)}'''


def runtime_script(cfg):
    player = cfg['player_id']
    storage_key = f"adex-mission-complete-plays::{cfg['audio_id']}"
    return f'''<!-- MISSION_TRANSCRIPT_RUNTIME:{cfg['audio_id']} -->
<script>
(function () {{
  const playerId = {player!r};
  const storageKey = {storage_key!r};
  const requiredPlays = 2;

  function boot() {{
    const audio = document.getElementById(playerId);
    const button = document.getElementById(playerId + '-transcript-button');
    const status = document.getElementById(playerId + '-transcript-status');
    const panel = document.getElementById(playerId + '-transcript-panel');
    const replay = document.getElementById(playerId + '-transcript-replay');
    if (!audio || !button || !status || !panel || !replay) {{
      window.setTimeout(boot, 120);
      return;
    }}

    let plays = 0;
    try {{ plays = Math.max(0, Math.min(requiredPlays, Number(localStorage.getItem(storageKey) || 0))); }} catch (_) {{}}
    let eligible = false;
    let invalidated = false;

    function save() {{
      try {{ localStorage.setItem(storageKey, String(plays)); }} catch (_) {{}}
    }}

    function render() {{
      const unlocked = plays >= requiredPlays;
      status.textContent = unlocked
        ? 'Unlocked · read the transcript and listen again.'
        : 'Locked · complete 2 full listens first (' + plays + '/2)';
      button.disabled = !unlocked;
      button.style.cursor = unlocked ? 'pointer' : 'not-allowed';
      button.style.color = unlocked ? '#15171A' : '#8B8A84';
      button.style.borderColor = unlocked ? {cfg['accent']!r} : 'rgba(21,23,26,0.2)';
      if (!unlocked) panel.style.display = 'none';
    }}

    audio.addEventListener('play', function () {{
      if (audio.currentTime <= 1.25) {{
        eligible = true;
        invalidated = false;
      }}
    }});

    audio.addEventListener('seeking', function () {{
      if (eligible && audio.currentTime > 3) invalidated = true;
    }});

    audio.addEventListener('ended', function () {{
      if (eligible && !invalidated && plays < requiredPlays) {{
        plays += 1;
        save();
      }}
      eligible = false;
      invalidated = false;
      render();
    }});

    button.addEventListener('click', function () {{
      if (plays < requiredPlays) return;
      const opening = panel.style.display === 'none' || !panel.style.display;
      panel.style.display = opening ? 'block' : 'none';
      button.textContent = opening ? 'Hide transcript' : 'Read transcript';
      if (opening) panel.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
    }});

    replay.controls = true;
    render();
  }}

  boot();
}})();
</script>
<!-- /MISSION_TRANSCRIPT_RUNTIME:{cfg['audio_id']} -->'''


def replace_card(text, cfg):
    player_id = re.escape(cfg['player_id'])
    # R1 was originally hand-authored without data-audio-id; R2-R4 use the
    # generated data-audio-id wrapper. In both cases anchor on the player id
    # and replace only the enclosing dark Mission Briefing audio card.
    patterns = [
        re.compile(
            rf'      <div data-audio-id="{re.escape(cfg["audio_id"])}"[\s\S]*?<audio id="{player_id}"[\s\S]*?</audio>\s*</div>(?:\s*<div id="{player_id}-transcript-shell"[\s\S]*?</div>\s*</div>)?',
            re.M,
        ),
        re.compile(
            rf'      <div style="margin-top:22px;background:#15171A;border-radius:12px;padding:22px 26px;">[\s\S]*?<audio id="{player_id}"[\s\S]*?</audio>\s*</div>(?:\s*<div id="{player_id}-transcript-shell"[\s\S]*?</div>\s*</div>)?',
            re.M,
        ),
    ]
    for pattern in patterns:
        new_text, count = pattern.subn(briefing_card(cfg), text, count=1)
        if count == 1:
            return new_text
    raise SystemExit(f"Could not replace Mission Briefing card in {cfg['page']}")


def inject_runtime(text, cfg):
    marker = re.compile(
        rf'<!-- MISSION_TRANSCRIPT_RUNTIME:{re.escape(cfg["audio_id"])} -->[\s\S]*?<!-- /MISSION_TRANSCRIPT_RUNTIME:{re.escape(cfg["audio_id"])} -->',
        re.M,
    )
    script = runtime_script(cfg)
    if marker.search(text):
        return marker.sub(script, text, count=1)
    if '</body>' not in text:
        raise SystemExit(f"Missing </body> in {cfg['page']}")
    return text.replace('</body>', f'{script}\n</body>', 1)


for cfg in BRIEFINGS:
    verify_asset(cfg)
    page = root / cfg['page']
    if not page.exists():
        raise SystemExit(f"Missing Mission Briefing page: {page}")
    text = page.read_text(encoding='utf-8')
    text = replace_card(text, cfg)
    text = inject_runtime(text, cfg)

    if f'controls="{{{{ true }}}}"' not in text:
        raise SystemExit(f"DC controls binding missing in {cfg['page']}")
    if f'src="{cfg["src"]}"' not in text:
        raise SystemExit(f"Audio source missing in {cfg['page']}")
    if 'complete 2 full listens first' not in text:
        raise SystemExit(f"Two-listen transcript gate missing in {cfg['page']}")
    if f'id="{cfg["player_id"]}-transcript-replay"' not in text:
        raise SystemExit(f"Transcript replay player missing in {cfg['page']}")
    if re.search(r'<audio[^>]*\sautoplay(?:\s|=|>)', text, re.I):
        raise SystemExit(f"Autoplay detected in {cfg['page']}")

    page.write_text(text, encoding='utf-8')

print('MISSION_BRIEFING_TRANSCRIPT_GATE=PASS')
