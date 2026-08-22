from pathlib import Path
import re
import sys

root = Path(sys.argv[1])

RAMPS = {
    "r1": {
        "label": "RAMP 01 · RECRUIT",
        "practice": "AdExposed-Ramp1-Recruit-Practice.dc.html",
        "listening": "AdExposed-Ramp1-Recruit-Listening.dc.html",
        "accent": "#9C6B12",
        "audio_id": None,
        "order": None,
        "src": None,
        "empty": "No separate listening-practice recording is assigned to RECRUIT yet. Use the Director Webb audio in Mission Briefing.",
    },
    "r2": {
        "label": "RAMP 02 · DECODE",
        "practice": "AdExposed-Ramp2-Decode-Practice.dc.html",
        "listening": "AdExposed-Ramp2-Decode-Listening.dc.html",
        "accent": "#2F5F82",
        "audio_id": "AD-EXPOSE-R2-S9-CLEANSTEP-TRACK01",
        "order": "01 · S09 · D-S9-W02",
        "src": "./audio/ad-expose/decode/cleanstep-s9.mp3",
        "empty": None,
    },
    "r3": {
        "label": "RAMP 03 · EXPOSE",
        "practice": "AdExposed-Ramp3-Expose-Practice.dc.html",
        "listening": "AdExposed-Ramp3-Expose-Listening.dc.html",
        "accent": "#2A7864",
        "audio_id": "AD-EXPOSE-R3-S12-MEDIA-STANDARDS-TRACK01",
        "order": "01 · S12 · E-S12-W01",
        "src": "./audio/ad-expose/expose/media-standards-s12.mp3",
        "empty": None,
    },
    "r4": {
        "label": "RAMP 04 · CREATE",
        "practice": "AdExposed-Ramp4-Create-Practice.dc.html",
        "listening": "AdExposed-Ramp4-Create-Listening.dc.html",
        "accent": "#BD5A34",
        "audio_id": None,
        "order": None,
        "src": None,
        "empty": "No separate listening-practice recording is assigned to CREATE yet. Use The Client — Final Commission in Mission Briefing.",
    },
}


def load(name: str) -> tuple[Path, str]:
    path = root / name
    if not path.exists():
        raise SystemExit(f"Missing AD EXPOSE page: {name}")
    return path, path.read_text(encoding="utf-8")


def save(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def patch_shared_navigation() -> None:
    path, text = load("adexposed-shared.js")

    for ramp in ("r1", "r2", "r3", "r4"):
        briefing_token = f"{ramp}_briefing: 'visible',"
        if f"{ramp}_listening: 'visible'," not in text:
            text = text.replace(
                briefing_token,
                briefing_token + f" {ramp}_listening: 'visible',",
                1,
            )

    replacement = '''export function buildSubTabs({ rampKey, activeSection, config, colorDark, colorAccent, hrefs }) {
  const vis = (config && config.visibility) || {};
  const listeningHrefs = {
    r1: 'AdExposed-Ramp1-Recruit-Listening.dc.html',
    r2: 'AdExposed-Ramp2-Decode-Listening.dc.html',
    r3: 'AdExposed-Ramp3-Expose-Listening.dc.html',
    r4: 'AdExposed-Ramp4-Create-Listening.dc.html',
  };
  const sections = [
    { key: 'briefing', label: 'Mission Briefing', href: hrefs.briefing },
    { key: 'listening', label: 'Listening Practice', href: listeningHrefs[rampKey] },
    { key: 'practice', label: 'Extra Practice', href: hrefs.practice },
    { key: 'checkpoint', label: 'Checkpoint', href: hrefs.checkpoint },
  ];
  return sections
    .filter(s => (vis[`${rampKey}_${s.key}`] || 'visible') !== 'hidden')
    .map(s => {
      const state = vis[`${rampKey}_${s.key}`] || 'visible';
      const frozen = state === 'frozen';
      const active = s.key === activeSection;
      return {
        label: s.label,
        color: frozen ? '#B9B7AF' : (active ? colorDark : '#15171A'),
        borderColor: active && !frozen ? colorAccent : 'transparent',
        cursor: frozen ? 'not-allowed' : 'pointer',
        onClick: frozen
          ? () => window.alert('This section is frozen by your teacher.')
          : () => { window.location.href = s.href; },
      };
    });
}
'''
    text, count = re.subn(
        r"export function buildSubTabs\([\s\S]*\n}\s*$",
        replacement,
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit("Could not replace buildSubTabs in adexposed-shared.js")
    save(path, text)


def patch_subtab_hints() -> None:
    for path in root.glob("AdExposed-Ramp*.dc.html"):
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            '<sc-for list="{{ subTabs }}" as="tab" hint-placeholder-count="3">',
            '<sc-for list="{{ subTabs }}" as="tab" hint-placeholder-count="4">',
        )
        path.write_text(text, encoding="utf-8")


def patch_webb() -> None:
    path, text = load("AdExposed-Ramp1-Recruit-Briefing.dc.html")
    text = text.replace(
        "MB-01 · Incoming transmission",
        "MB-01 · RAMP 01 · RECRUIT · Director Webb — Mission Briefing",
        1,
    )
    text = text.replace(
        "MB-01 · Director Webb — RECRUIT Briefing",
        "MB-01 · RAMP 01 · RECRUIT · Director Webb — Mission Briefing",
        1,
    )

    webb_sources = [
        r'src="/api/audio/f4ccb9e2-f32d-493d-97fb-a138703f9d28/1"',
        r'src="https://fsxozhthibraurgvsxtw\.supabase\.co/storage/v1/object/public/audio/f4ccb9e2-f32d-493d-97fb-a138703f9d28/session_1_audio\.mp3"',
    ]
    for pattern in webb_sources:
        text = re.sub(
            pattern,
            'src="./assets/director-webb-recruit-briefing.mp3"',
            text,
        )

    text = re.sub(
        r'<div style="margin-top:14px;">\s*<button[^>]*onClick="\{\{ onOpenTranscript \}\}"[^>]*>View transcript</button>\s*</div>',
        "",
        text,
        flags=re.S,
    )
    text = re.sub(
        r'<sc-if value="\{\{ showTranscript \}\}"[^>]*>.*?</sc-if>',
        "",
        text,
        flags=re.S,
    )

    if 'src="./assets/director-webb-recruit-briefing.mp3"' not in text:
        raise SystemExit("Locked Webb player missing from RECRUIT Mission Briefing")
    save(path, text)


def insert_intro(name: str, audio_id: str, label: str, asset: str, accent: str) -> None:
    path, text = load(name)
    marker = '      <div style="display:grid;grid-template-columns:1.4fr 1fr;gap:40px;margin-top:26px;align-items:start;">'

    if f'data-audio-id="{audio_id}"' in text:
        text = re.sub(
            rf'(<div data-audio-id="{re.escape(audio_id)}"[\s\S]*?<div[^>]*>)(.*?)(</div>\s*<audio)',
            rf'\1{label}\3',
            text,
            count=1,
        )
        text = re.sub(
            rf'(<div data-audio-id="{re.escape(audio_id)}"[\s\S]*?<audio[^>]*src=")[^"]+(")',
            rf'\1{asset}\2',
            text,
            count=1,
        )
        save(path, text)
        return

    if marker not in text:
        raise SystemExit(f"Mission Briefing insertion marker missing in {name}")

    card = f'''      <div data-audio-id="{audio_id}" style="margin-top:22px;background:#15171A;border-radius:12px;padding:22px 26px;">
        <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:{accent};">{label}</div>
        <audio controls preload="metadata" src="{asset}" aria-label="{label}" style="width:100%;margin-top:14px;outline:none;"></audio>
      </div>'''
    text = text.replace(marker, card + "\n\n" + marker, 1)
    save(path, text)


def extract_canonical_practice_panel(text: str, audio_id: str) -> tuple[str, str]:
    block_re = re.compile(
        r'<!-- AD EXPOSE v2\.1 canonical audio binding: '
        + re.escape(audio_id)
        + r' -->\s*<section.*?</section>\s*<script>.*?</script>',
        re.S,
    )
    match = block_re.search(text)
    if not match:
        raise SystemExit(f"Canonical practice player missing for {audio_id}")
    panel = match.group(0)
    clean = text[: match.start()] + text[match.end() :]
    return clean, panel


def listening_block(ramp_label: str, accent: str, panel: str | None, order_label: str | None, expected_src: str | None, empty: str | None) -> str:
    header = f'''  <sc-if value="{{{{ shown }}}}" hint-placeholder-val="{{{{ true }}}}">
  <div style="max-width:1120px;margin:0 auto;padding:32px 48px 90px;">
    <div style="opacity:{{{{ opacity }}}};filter:{{{{ filter }}}};pointer-events:{{{{ pointerEvents }}}};">
      <div style="display:flex;align-items:center;gap:14px;">
        <div style="font-family:'IBM Plex Sans',sans-serif;font-weight:700;font-size:22px;letter-spacing:0.01em;text-transform:uppercase;color:#15171A;">Listening Practice</div>
        <sc-if value="{{{{ frozen }}}}" hint-placeholder-val="{{{{ false }}}}">
          <span style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:0.08em;text-transform:uppercase;color:#fff;background:#6B6A63;padding:3px 9px;border-radius:4px;">Frozen by your teacher</span>
        </sc-if>
        <div style="flex:1;height:1px;background:#15171A;opacity:0.15;margin-left:6px;"></div>
      </div>

      <div data-listening-practice="{ramp_label}" style="margin-top:28px;padding:18px 20px;border:1px solid rgba(21,23,26,.12);border-radius:12px;background:#fff;">
        <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:{accent};">{ramp_label} · LISTENING PRACTICE</div>
        <div style="font-family:'IBM Plex Sans',sans-serif;font-size:13px;line-height:1.55;color:#6B6A63;margin-top:7px;">Recordings are ordered by session and activity code so each file can be identified immediately.</div>
      </div>
'''

    if panel is not None:
        panel = re.sub(
            r'src="/audio/ad-expose/[^\"]+\.mp3"',
            f'src="{expected_src}"',
            panel,
            count=1,
        )
        panel = panel.replace(
            "SIGNAL AUDIO BRIEFING",
            f"{order_label} · {ramp_label}",
            1,
        )
        body = "\n" + panel + "\n"
    else:
        body = f'''
      <div style="margin-top:20px;border:1px dashed rgba(21,23,26,.22);border-radius:12px;padding:24px;background:#FBFAF7;">
        <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.10em;text-transform:uppercase;color:{accent};">NO SEPARATE LISTENING FILE YET</div>
        <div style="font-family:'IBM Plex Sans',sans-serif;font-size:13.5px;line-height:1.6;color:#444;margin-top:8px;">{empty}</div>
      </div>
'''

    return header + body + '''    </div>
  </div>
  </sc-if>
'''


def build_listening_page(ramp_key: str, source_text: str, panel: str | None) -> str:
    cfg = RAMPS[ramp_key]
    text = source_text

    text = text.replace("/ Extra Practice</span>", "/ Listening Practice</span>", 1)
    text = text.replace(f"visState('{ramp_key}_practice')", f"visState('{ramp_key}_listening')", 1)
    text = text.replace("activeSection: 'practice'", "activeSection: 'listening'", 1)
    text = text.replace("activeSection:'practice'", "activeSection:'listening'", 1)

    shown_marker = '  <sc-if value="{{ shown }}" hint-placeholder-val="{{ true }}">'
    hidden_marker = '  <sc-if value="{{ hidden }}" hint-placeholder-val="{{ false }}">'
    start = text.find(shown_marker)
    end = text.find(hidden_marker)
    if start < 0 or end < 0 or end <= start:
        raise SystemExit(f"Could not locate shown/hidden shell in {cfg['practice']}")

    new_shown = listening_block(
        cfg["label"],
        cfg["accent"],
        panel,
        cfg["order"],
        cfg["src"],
        cfg["empty"],
    )
    text = text[:start] + new_shown + text[end:]

    if panel is not None and f'src="{cfg["src"]}"' not in text:
        raise SystemExit(f"Project-relative audio source not installed in {cfg['listening']}")
    if re.search(r'<audio[^>]*\sautoplay(?:\s|=|>)', text, re.I):
        raise SystemExit(f"Autoplay detected in {cfg['listening']}")
    return text


def restore_extra_practice_and_create_listening_pages() -> None:
    for ramp_key, cfg in RAMPS.items():
        path, raw = load(cfg["practice"])
        panel = None
        clean = raw
        if cfg["audio_id"]:
            clean, panel = extract_canonical_practice_panel(raw, cfg["audio_id"])

        clean = clean.replace(">Listening Repository</div>", ">Extra Practice</div>", 1)
        save(path, clean)

        listening = build_listening_page(ramp_key, clean, panel)
        save(root / cfg["listening"], listening)


patch_shared_navigation()
patch_subtab_hints()
patch_webb()
insert_intro(
    "AdExposed-Ramp2-Decode-Briefing.dc.html",
    "AD-EXPOSE-R2-INTRO-DECODE-TRACK01",
    "MB-02 · RAMP 02 · DECODE · Dr. Lena Vasquez — Mission Briefing",
    "./assets/dr-lena-vasquez-decode-briefing.mp3",
    "#7EB6E8",
)
insert_intro(
    "AdExposed-Ramp3-Expose-Briefing.dc.html",
    "AD-EXPOSE-R3-INTRO-EXPOSE-TRACK01",
    "MB-03 · RAMP 03 · EXPOSE · Dr. Lena Vasquez — Ethics Briefing",
    "./assets/dr-lena-vasquez-expose-ethics-briefing.mp3",
    "#6FC4B0",
)
insert_intro(
    "AdExposed-Ramp4-Create-Briefing.dc.html",
    "AD-EXPOSE-R4-INTRO-CREATE-TRACK01",
    "MB-04 · RAMP 04 · CREATE · The Client — Final Commission",
    "./assets/the-client-final-commission.mp3",
    "#F0996E",
)
restore_extra_practice_and_create_listening_pages()

print("AD_EXPOSE_NAVIGATION_AND_LISTENING_PRACTICE=PASS")
