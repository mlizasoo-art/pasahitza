from pathlib import Path
import re
import sys

root = Path(sys.argv[1])


def load(name: str) -> tuple[Path, str]:
    path = root / name
    if not path.exists():
        raise SystemExit(f"Missing AD EXPOSE page: {name}")
    return path, path.read_text(encoding="utf-8")


def save(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def patch_webb() -> None:
    path, text = load("AdExposed-Ramp1-Recruit-Briefing.dc.html")
    text = text.replace(
        "MB-01 · Incoming transmission",
        "MB-01 · Director Webb — RECRUIT Briefing",
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

    # Preserve the locked website policy already established for Webb: player
    # only, no learner-facing transcript control.
    text = re.sub(
        r'<div style="margin-top:14px;">\s*<button[^>]*onClick="\{\{ onOpenTranscript \}\}"[^>]*>View transcript</button>\s*</div>',
        '',
        text,
        flags=re.S,
    )
    text = re.sub(
        r'<sc-if value="\{\{ showTranscript \}\}"[^>]*>.*?</sc-if>',
        '',
        text,
        flags=re.S,
    )

    if 'src="./assets/director-webb-recruit-briefing.mp3"' not in text:
        raise SystemExit("Locked Webb player missing from RECRUIT Mission Briefing")
    save(path, text)


def insert_intro(name: str, audio_id: str, label: str, asset: str, accent: str) -> None:
    path, text = load(name)
    if f'data-audio-id="{audio_id}"' in text:
        return

    marker = '      <div style="display:grid;grid-template-columns:1.4fr 1fr;gap:40px;margin-top:26px;align-items:start;">'
    if marker not in text:
        raise SystemExit(f"Mission Briefing insertion marker missing in {name}")

    card = f'''      <div data-audio-id="{audio_id}" style="margin-top:22px;background:#15171A;border-radius:12px;padding:22px 26px;">
        <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:{accent};">{label}</div>
        <audio controls preload="metadata" src="{asset}" aria-label="{label}" style="width:100%;margin-top:14px;outline:none;"></audio>
      </div>'''
    text = text.replace(marker, card + "\n\n" + marker, 1)
    save(path, text)


def move_practice_to_repository(
    name: str,
    audio_id: str,
    ramp_label: str,
    order_label: str,
    expected_src: str,
    accent: str,
) -> None:
    path, text = load(name)

    # The Vercel source route appends this canonical block at the end of the
    # document. The GitHub static site instead presents it inside the actual
    # ramp listening repository.
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
    text = text[: match.start()] + text[match.end() :]

    # GitHub Pages is project-scoped, so root-relative /audio URLs are wrong.
    panel = re.sub(
        r'src="/audio/ad-expose/[^\"]+\.mp3"',
        f'src="{expected_src}"',
        panel,
        count=1,
    )
    panel = panel.replace(
        "SIGNAL AUDIO BRIEFING",
        f"{order_label} · {ramp_label} LISTENING REPOSITORY",
        1,
    )

    # Keep the existing navigation contract, but make the learner-facing
    # content unmistakably a listening repository.
    text = text.replace(
        ">Extra Practice</div>",
        ">Listening Repository</div>",
        1,
    )

    coming_re = re.compile(
        r'      <div style="margin-top:28px;border:1px dashed rgba\(21,23,26,0\.25\);border-radius:14px;padding:56px 40px;text-align:center;background:#FBFAF7;">\s*'
        r'<div[^>]*>Coming soon</div>\s*'
        r'<div[^>]*>Guided practice for Ramp [^<]+</div>\s*'
        r'</div>',
        re.S,
    )
    if not coming_re.search(text):
        raise SystemExit(f"Listening repository placeholder missing in {name}")

    intro = f'''      <div data-listening-repository="{ramp_label}" style="margin-top:28px;padding:18px 20px;border:1px solid rgba(21,23,26,.12);border-radius:12px;background:#fff;">
        <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:{accent};">{ramp_label} · LISTENING REPOSITORY</div>
        <div style="font-family:'IBM Plex Sans',sans-serif;font-size:13px;line-height:1.55;color:#6B6A63;margin-top:7px;">Files are ordered by session. Start with the session label shown on each recording.</div>
      </div>

{panel}'''
    text = coming_re.sub(intro, text, count=1)

    if f'src="{expected_src}"' not in text:
        raise SystemExit(f"Project-relative audio source not installed for {audio_id}")
    if re.search(r'<audio[^>]*\sautoplay(?:\s|=|>)', text, re.I):
        raise SystemExit(f"Autoplay detected in {name}")
    save(path, text)


patch_webb()
insert_intro(
    "AdExposed-Ramp2-Decode-Briefing.dc.html",
    "AD-EXPOSE-R2-INTRO-DECODE-TRACK01",
    "MB-02 · Dr. Lena Vasquez — DECODE Briefing",
    "./assets/dr-lena-vasquez-decode-briefing.mp3",
    "#7EB6E8",
)
insert_intro(
    "AdExposed-Ramp3-Expose-Briefing.dc.html",
    "AD-EXPOSE-R3-INTRO-EXPOSE-TRACK01",
    "MB-03 · Dr. Lena Vasquez — EXPOSE Ethics Briefing",
    "./assets/dr-lena-vasquez-expose-ethics-briefing.mp3",
    "#6FC4B0",
)
insert_intro(
    "AdExposed-Ramp4-Create-Briefing.dc.html",
    "AD-EXPOSE-R4-INTRO-CREATE-TRACK01",
    "MB-04 · The Client — Final Commission",
    "./assets/the-client-final-commission.mp3",
    "#F0996E",
)
move_practice_to_repository(
    "AdExposed-Ramp2-Decode-Practice.dc.html",
    "AD-EXPOSE-R2-S9-CLEANSTEP-TRACK01",
    "RAMP 02 · DECODE",
    "01 · S09",
    "./audio/ad-expose/decode/cleanstep-s9.mp3",
    "#2F5F82",
)
move_practice_to_repository(
    "AdExposed-Ramp3-Expose-Practice.dc.html",
    "AD-EXPOSE-R3-S12-MEDIA-STANDARDS-TRACK01",
    "RAMP 03 · EXPOSE",
    "01 · S12",
    "./audio/ad-expose/expose/media-standards-s12.mp3",
    "#2A7864",
)

print("AD_EXPOSE_AUDIO_LAYOUT=PASS")
