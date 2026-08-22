const TRACKS = {
  'AdExposed-Ramp2-Decode-Practice.dc.html': {
    audioId: 'AD-EXPOSE-R2-S9-CLEANSTEP-TRACK01',
    title: 'CleanStep SIGNAL Briefing',
    src: 'https://unidades-app.vercel.app/audio/ad-expose/decode/cleanstep-s9.mp3',
    accent: '#2F5F82',
    transcript: 'Yesterday, SIGNAL received a new advertisement for CleanStep trainers. While I was checking the campaign, I noticed the claim “100% planet-friendly.” The company said that the upper fabric used 40% recycled polyester. However, the advertisement did not explain the sole, the packaging, the transport, or the other materials in the shoe. I am not saying that the product is environmentally harmful. The company also has a real recycling programme. My conclusion is simpler: one environmental benefit does not prove that the whole product is “100% planet-friendly.” The claim is broader than the evidence.'
  },
  'AdExposed-Ramp3-Expose-Practice.dc.html': {
    audioId: 'AD-EXPOSE-R3-S12-MEDIA-STANDARDS-TRACK01',
    title: 'SIGNAL Media Standards Briefing',
    src: 'https://unidades-app.vercel.app/audio/ad-expose/expose/media-standards-s12.mp3',
    accent: '#2A7864',
    transcript: 'People raise concerns about advertising for many different reasons. First, some audiences need extra care. Children, for example, may find it difficult to recognise persuasive techniques, and adults sometimes complain when child celebrities are used to promote fast food or toys. Another common concern is representation. Some adverts have shown women mainly as objects used to sell products, while others repeat narrow ideas about what men or women should look like or do. Violence presented as funny can also cause complaints. Alcohol advertising near content for children is another sensitive issue. Beauty advertising creates a different problem when bodies are heavily edited or when one body type is repeatedly presented as the ideal. This can connect advertising with body image and social pressure. Remember: a complaint does not automatically prove that an advert is illegal or unethical. For SIGNAL, complaints are clues. Analysts still need to examine the actual message, audience, evidence and context before reaching a judgement.'
  }
};

function pageName() {
  return decodeURIComponent(location.pathname.split('/').pop() || '');
}

function safeId(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-');
}

function injectAudioPanel(track) {
  if (!track || document.querySelector(`[data-audio-id="${track.audioId}"]`)) return;

  const id = `signal-audio-${safeId(track.audioId)}`;
  const storageKey = `ad-expose:${track.audioId}:complete-plays`;
  const root = document.createElement('section');
  root.id = id;
  root.dataset.audioId = track.audioId;
  root.style.cssText = "max-width:980px;margin:24px auto 48px;padding:20px;border:1px solid rgba(21,23,26,.22);border-radius:14px;background:#FBFAF7;color:#15171A;font-family:'IBM Plex Sans',sans-serif;box-sizing:border-box";
  root.innerHTML = `
    <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:${track.accent};margin-bottom:7px">SIGNAL AUDIO BRIEFING</div>
    <h2 style="font-size:22px;line-height:1.15;margin:0 0 8px">${track.title}</h2>
    <p style="margin:0 0 14px;line-height:1.5;color:#555">Listen to the complete briefing twice. The transcript unlocks after your first complete play.</p>
    <audio controls preload="metadata" src="${track.src}" style="width:100%"></audio>
    <div data-play-status style="margin-top:9px;font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600">Complete plays: 0/2</div>
    <button type="button" data-transcript-button disabled style="margin-top:12px;padding:9px 12px;border:1px solid #15171A;border-radius:7px;background:#15171A;color:#fff;font-weight:700;cursor:pointer;opacity:.55">Transcript locked</button>
    <div data-transcript hidden style="margin-top:14px;padding:14px;border-left:4px solid ${track.accent};background:#fff;line-height:1.6"></div>
  `;

  const player = root.querySelector('audio');
  const status = root.querySelector('[data-play-status]');
  const button = root.querySelector('[data-transcript-button]');
  const transcriptPanel = root.querySelector('[data-transcript]');
  let plays = Math.max(0, Number(localStorage.getItem(storageKey) || 0));

  const render = () => {
    status.textContent = `Complete plays: ${Math.min(plays, 2)}/2`;
    if (plays >= 1) {
      button.disabled = false;
      button.style.opacity = '1';
      button.textContent = transcriptPanel.hidden ? 'Show transcript' : 'Hide transcript';
    }
  };

  player.addEventListener('ended', () => {
    plays = Math.min(2, plays + 1);
    localStorage.setItem(storageKey, String(plays));
    render();
  });

  button.addEventListener('click', () => {
    if (plays < 1) return;
    transcriptPanel.hidden = !transcriptPanel.hidden;
    if (!transcriptPanel.hidden && !transcriptPanel.textContent) transcriptPanel.textContent = track.transcript;
    button.textContent = transcriptPanel.hidden ? 'Show transcript' : 'Hide transcript';
  });

  const dcRoot = document.getElementById('dc-root');
  if (dcRoot?.parentNode) dcRoot.parentNode.insertBefore(root, dcRoot.nextSibling);
  else document.body.appendChild(root);
  render();
}

function boot() {
  const track = TRACKS[pageName()];
  if (!track) return;
  const tryInject = () => {
    injectAudioPanel(track);
    if (!document.querySelector(`[data-audio-id="${track.audioId}"]`)) setTimeout(tryInject, 100);
  };
  tryInject();
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, { once: true });
else boot();
