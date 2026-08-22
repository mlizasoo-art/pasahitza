from pathlib import Path
import re

from mission_briefing_transcripts import BRIEFINGS


def delegated_runtime(cfg):
    player = cfg['player_id']
    key = f"adex-mission-complete-plays::{cfg['audio_id']}"
    return f'''<!-- MISSION_TRANSCRIPT_RUNTIME:{cfg['audio_id']} -->
<script>
(function () {{
  const playerId = {player!r};
  const storageKey = {key!r};
  const requiredPlays = 2;
  let plays = 0;
  let eligible = false;
  let invalidated = false;

  function loadPlays() {{
    try {{
      plays = Math.max(0, Math.min(requiredPlays, Number(localStorage.getItem(storageKey) || 0)));
    }} catch (_) {{
      plays = Math.max(0, Math.min(requiredPlays, plays || 0));
    }}
  }}

  function savePlays() {{
    try {{ localStorage.setItem(storageKey, String(plays)); }} catch (_) {{}}
  }}

  function nodes() {{
    return {{
      button: document.getElementById(playerId + '-transcript-button'),
      status: document.getElementById(playerId + '-transcript-status'),
      panel: document.getElementById(playerId + '-transcript-panel')
    }};
  }}

  function render() {{
    const current = nodes();
    if (!current.button || !current.status || !current.panel) return;
    const unlocked = plays >= requiredPlays;
    const nextStatus = unlocked
      ? 'Unlocked · read the transcript and listen again.'
      : 'Locked · complete 2 full listens first (' + plays + '/2)';
    if (current.status.textContent !== nextStatus) current.status.textContent = nextStatus;
    current.button.disabled = !unlocked;
    current.button.style.cursor = unlocked ? 'pointer' : 'not-allowed';
    current.button.style.color = unlocked ? '#15171A' : '#8B8A84';
    current.button.style.borderColor = unlocked ? {cfg['accent']!r} : 'rgba(21,23,26,0.2)';
    if (!unlocked) current.panel.style.display = 'none';
  }}

  function isMainAudio(target) {{
    return target && target.id === playerId;
  }}

  document.addEventListener('play', function (event) {{
    const audio = event.target;
    if (!isMainAudio(audio)) return;
    if (Number(audio.currentTime || 0) <= 1.25) {{
      eligible = true;
      invalidated = false;
    }}
  }}, true);

  document.addEventListener('seeking', function (event) {{
    const audio = event.target;
    if (!isMainAudio(audio) || !eligible) return;
    if (Number(audio.currentTime || 0) > 3) invalidated = true;
  }}, true);

  document.addEventListener('ended', function (event) {{
    const audio = event.target;
    if (!isMainAudio(audio)) return;
    if (eligible && !invalidated && plays < requiredPlays) {{
      plays += 1;
      savePlays();
    }}
    eligible = false;
    invalidated = false;
    render();
  }}, true);

  document.addEventListener('click', function (event) {{
    const button = event.target && event.target.closest
      ? event.target.closest('#' + playerId + '-transcript-button')
      : null;
    if (!button || plays < requiredPlays) return;
    const current = nodes();
    if (!current.panel) return;
    const opening = current.panel.style.display === 'none' || !current.panel.style.display;
    current.panel.style.display = opening ? 'block' : 'none';
    button.textContent = opening ? 'Hide transcript' : 'Read transcript';
    if (opening) current.panel.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
  }}, true);

  window.addEventListener('storage', function (event) {{
    if (event.key !== storageKey) return;
    loadPlays();
    render();
  }});

  // The DC runtime replaces the original <x-dc> tree with a React-rendered
  // tree and may replace media nodes again after its source refresh. Event
  // delegation above survives those replacements; this lightweight refresh
  // keeps the visible 0/2, 1/2, 2/2 state in sync with the current DOM.
  loadPlays();
  render();
  window.setInterval(render, 400);
}})();
</script>
<!-- /MISSION_TRANSCRIPT_RUNTIME:{cfg['audio_id']} -->'''


def repair_transcript_runtimes(root: Path):
    for cfg in BRIEFINGS:
        page = root / cfg['page']
        if not page.exists():
            raise SystemExit(f"Missing Mission Briefing page: {page}")
        text = page.read_text(encoding='utf-8')
        marker = re.compile(
            rf'<!-- MISSION_TRANSCRIPT_RUNTIME:{re.escape(cfg["audio_id"])} -->[\s\S]*?<!-- /MISSION_TRANSCRIPT_RUNTIME:{re.escape(cfg["audio_id"])} -->',
            re.M,
        )
        text, count = marker.subn(delegated_runtime(cfg), text, count=1)
        if count != 1:
            raise SystemExit(f"Mission transcript runtime marker missing in {cfg['page']}")
        if "document.addEventListener('ended'" not in text:
            raise SystemExit(f"Delegated ended listener missing in {cfg['page']}")
        if 'window.setInterval(render, 400)' not in text:
            raise SystemExit(f"DOM refresh guard missing in {cfg['page']}")
        page.write_text(text, encoding='utf-8')
    print('MISSION_TRANSCRIPT_RUNTIME_REPAIR=PASS')
