from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('ad-exposed-preview')
page = root / 'AdExposed-Ramp2-Decode-Listening.dc.html'
if not page.exists():
    raise SystemExit(f'Missing DECODE Listening Practice page: {page}')

text = page.read_text(encoding='utf-8')
shown_marker = '  <sc-if value="{{ shown }}" hint-placeholder-val="{{ true }}">'
hidden_marker = '  <sc-if value="{{ hidden }}" hint-placeholder-val="{{ false }}">'
start = text.find(shown_marker)
end = text.find(hidden_marker)
if start < 0 or end < 0 or end <= start:
    raise SystemExit('Could not locate DECODE Listening Practice shown shell')

cleanstep_transcript = (
    'Yesterday, SIGNAL received a new advertisement for CleanStep trainers. '
    'While I was checking the campaign, I noticed the claim “100% planet-friendly.” '
    'The company said that the upper fabric used 40% recycled polyester. '
    'However, the advertisement did not explain the sole, the packaging, the transport, or the other materials in the shoe. '
    'I am not saying that the product is environmentally harmful. '
    'The company also has a real recycling programme. '
    'My conclusion is simpler: one environmental benefit does not prove that the whole product is “100% planet-friendly.” '
    'The claim is broader than the evidence.'
)

shown = f'''  <sc-if value="{{{{ shown }}}}" hint-placeholder-val="{{{{ true }}}}">
  <div style="max-width:1120px;margin:0 auto;padding:32px 48px 90px;">
    <div style="opacity:{{{{ opacity }}}};filter:{{{{ filter }}}};pointer-events:{{{{ pointerEvents }}}};">
      <div style="display:flex;align-items:center;gap:14px;">
        <div style="font-family:'IBM Plex Sans',sans-serif;font-weight:700;font-size:22px;letter-spacing:0.01em;text-transform:uppercase;color:#15171A;">Listening Practice</div>
        <sc-if value="{{{{ frozen }}}}" hint-placeholder-val="{{{{ false }}}}">
          <span style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:0.08em;text-transform:uppercase;color:#fff;background:#6B6A63;padding:3px 9px;border-radius:4px;">Frozen by your teacher</span>
        </sc-if>
        <div style="flex:1;height:1px;background:#15171A;opacity:0.15;margin-left:6px;"></div>
      </div>

      <div data-listening-practice="RAMP 02 · DECODE" data-listening-gold="v1" style="margin-top:28px;padding:20px 22px;border:1px solid rgba(21,23,26,.12);border-radius:12px;background:#F7FAFC;">
        <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#2F5F82;">RAMP 02 · DECODE · LISTENING PRACTICE</div>
        <div style="font-family:'IBM Plex Sans',sans-serif;font-size:14px;line-height:1.6;color:#444;margin-top:8px;max-width:820px;">Work in session order. External campaign material opens at its original source; SIGNAL-owned audio plays here. Use the first viewing/listen for gist and the second for evidence. This is practice, not the secure checkpoint.</div>
      </div>

      <section id="decode-listening-s5" data-listening-item="D-S5-W01" style="margin-top:24px;border:1px solid rgba(47,95,130,.22);border-radius:14px;overflow:hidden;background:#fff;">
        <div style="padding:18px 22px;background:#EEF5FA;border-bottom:1px solid rgba(47,95,130,.15);">
          <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#2F5F82;">01 · S05 · D-S5-W01</div>
          <div style="font-family:'IBM Plex Sans',sans-serif;font-weight:700;font-size:22px;color:#15171A;margin-top:6px;">Jingle Lab</div>
          <div style="font-family:'IBM Plex Sans',sans-serif;font-size:13.5px;line-height:1.55;color:#555;margin-top:6px;">Listen to or watch the four campaign clips. Write the product or service type for each one, then choose the jingle you find most memorable. Do not copy song lyrics.</div>
        </div>
        <div style="padding:18px 22px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;">
          <div style="border:1px solid rgba(21,23,26,.12);border-radius:10px;padding:15px;">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:9.5px;color:#6B6A63;letter-spacing:.08em;text-transform:uppercase;">Clip 1</div>
            <div style="font-weight:700;margin-top:5px;">Mars Bar</div>
            <a href="https://www.hatads.org.uk/catalogue/record/e2c54d1f-40bc-479a-a3cc-aff7f46a3bee" target="_blank" rel="noopener noreferrer" style="display:inline-block;margin-top:10px;padding:8px 11px;border-radius:7px;background:#2F5F82;color:#fff;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;">Open archive clip ↗</a>
            <input data-jingle-response="mars" placeholder="Product type" style="display:block;width:100%;box-sizing:border-box;margin-top:11px;padding:8px 9px;border:1px solid rgba(21,23,26,.2);border-radius:6px;font-size:12.5px;" />
          </div>
          <div style="border:1px solid rgba(21,23,26,.12);border-radius:10px;padding:15px;">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:9.5px;color:#6B6A63;letter-spacing:.08em;text-transform:uppercase;">Clip 2</div>
            <div style="font-weight:700;margin-top:5px;">Jacob's Club</div>
            <a href="https://www.doyouremember.co.uk/memory/club-biscuits" target="_blank" rel="noopener noreferrer" style="display:inline-block;margin-top:10px;padding:8px 11px;border-radius:7px;background:#2F5F82;color:#fff;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;">Open archive clip ↗</a>
            <input data-jingle-response="club" placeholder="Product type" style="display:block;width:100%;box-sizing:border-box;margin-top:11px;padding:8px 9px;border:1px solid rgba(21,23,26,.2);border-radius:6px;font-size:12.5px;" />
          </div>
          <div style="border:1px solid rgba(21,23,26,.12);border-radius:10px;padding:15px;">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:9.5px;color:#6B6A63;letter-spacing:.08em;text-transform:uppercase;">Clip 3</div>
            <div style="font-weight:700;margin-top:5px;">Chicken Tonight</div>
            <a href="https://www.youtube.com/watch?v=x1veMqaPOxo" target="_blank" rel="noopener noreferrer" style="display:inline-block;margin-top:10px;padding:8px 11px;border-radius:7px;background:#2F5F82;color:#fff;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;">Open video ↗</a>
            <input data-jingle-response="chicken" placeholder="Product type" style="display:block;width:100%;box-sizing:border-box;margin-top:11px;padding:8px 9px;border:1px solid rgba(21,23,26,.2);border-radius:6px;font-size:12.5px;" />
          </div>
          <div style="border:1px solid rgba(21,23,26,.12);border-radius:10px;padding:15px;">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:9.5px;color:#6B6A63;letter-spacing:.08em;text-transform:uppercase;">Clip 4</div>
            <div style="font-weight:700;margin-top:5px;">WeBuyAnyCar.com</div>
            <a href="https://www.youtube.com/watch?v=f-yEWZTBQ64" target="_blank" rel="noopener noreferrer" style="display:inline-block;margin-top:10px;padding:8px 11px;border-radius:7px;background:#2F5F82;color:#fff;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;">Open video ↗</a>
            <input data-jingle-response="webuy" placeholder="Product / service type" style="display:block;width:100%;box-sizing:border-box;margin-top:11px;padding:8px 9px;border:1px solid rgba(21,23,26,.2);border-radius:6px;font-size:12.5px;" />
          </div>
        </div>
        <div style="padding:0 22px 20px;">
          <label style="display:block;font-size:13px;font-weight:600;color:#333;">Which jingle is most memorable for you? Why?</label>
          <textarea data-jingle-response="memorable" rows="2" style="width:100%;box-sizing:border-box;margin-top:7px;padding:9px;border:1px solid rgba(21,23,26,.2);border-radius:7px;font-family:'IBM Plex Sans',sans-serif;font-size:13px;"></textarea>
        </div>
      </section>

      <section id="decode-listening-s7" data-listening-item="D-S7-01" style="margin-top:24px;border:1px solid rgba(47,95,130,.22);border-radius:14px;overflow:hidden;background:#fff;">
        <div style="padding:18px 22px;background:#EEF5FA;border-bottom:1px solid rgba(47,95,130,.15);">
          <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#2F5F82;">02 · S07 · D-S7-01</div>
          <div style="font-family:'IBM Plex Sans',sans-serif;font-weight:700;font-size:22px;color:#15171A;margin-top:6px;">Save the Children · Most Shocking Second a Day</div>
          <div style="font-family:'IBM Plex Sans',sans-serif;font-size:13.5px;line-height:1.55;color:#555;margin-top:6px;">Official campaign source. Watch twice: first for gist, then for evidence.</div>
          <a href="https://www.youtube.com/watch?v=RBQ-IoHfimQ" target="_blank" rel="noopener noreferrer" style="display:inline-block;margin-top:11px;padding:9px 12px;border-radius:7px;background:#2F5F82;color:#fff;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;">Watch official film ↗</a>
        </div>
        <div data-practice-quiz="save-the-children" style="padding:20px 22px;">
          <div style="font-weight:700;font-size:14px;">Before viewing</div>
          <div style="font-size:13.5px;line-height:1.55;margin-top:5px;color:#444;">From the title <em>Most Shocking Second a Day</em>, predict the subject of the film in one short sentence.</div>
          <textarea rows="2" data-save-prediction style="width:100%;box-sizing:border-box;margin-top:8px;padding:9px;border:1px solid rgba(21,23,26,.2);border-radius:7px;font-family:'IBM Plex Sans',sans-serif;"></textarea>

          <div style="font-weight:700;font-size:14px;margin-top:18px;">First viewing · gist</div>
          <div style="font-size:13.5px;margin-top:7px;">Choose the best summary.</div>
          <label style="display:block;margin-top:7px;"><input type="radio" name="stc-gist" value="A"> A. A child learns how to make an advertisement.</label>
          <label style="display:block;margin-top:5px;"><input type="radio" name="stc-gist" value="B"> B. A child's ordinary life changes as conflict reaches her world.</label>
          <label style="display:block;margin-top:5px;"><input type="radio" name="stc-gist" value="C"> C. A company launches a new product.</label>
          <label style="display:block;margin-top:5px;"><input type="radio" name="stc-gist" value="D"> D. A family moves house for a holiday.</label>

          <div style="font-weight:700;font-size:14px;margin-top:18px;">Second viewing · evidence</div>
          <div data-q="stc1" data-key="A" style="margin-top:10px;font-size:13.5px;">1. What appeal does the campaign mainly use?<br><label><input type="radio" name="stc1" value="A"> A. Emotional</label> &nbsp; <label><input type="radio" name="stc1" value="B"> B. Rational</label> &nbsp; <label><input type="radio" name="stc1" value="C"> C. Social</label> &nbsp; <label><input type="radio" name="stc1" value="D"> D. No persuasive appeal</label></div>
          <div data-q="stc2" data-key="B" style="margin-top:12px;font-size:13.5px;">2. Who is the most likely target audience?<br><label><input type="radio" name="stc2" value="A"> A. Children living in Syria</label><br><label><input type="radio" name="stc2" value="B"> B. People in the UK who can notice, share or support the campaign</label><br><label><input type="radio" name="stc2" value="C"> C. Professional actors</label><br><label><input type="radio" name="stc2" value="D"> D. Advertising companies</label></div>
          <div data-q="stc3" data-key="A" style="margin-top:12px;font-size:13.5px;">3. Why does the film use a British child?<br><label><input type="radio" name="stc3" value="A"> A. To make a distant conflict feel closer to a UK audience</label><br><label><input type="radio" name="stc3" value="B"> B. To advertise a British product</label><br><label><input type="radio" name="stc3" value="C"> C. To claim the conflict happened in Britain</label><br><label><input type="radio" name="stc3" value="D"> D. To make the film longer</label></div>
          <div data-q="stc4" data-key="TRUE" style="margin-top:12px;font-size:13.5px;">4. The campaign uses shock to create an emotional reaction.<br><label><input type="radio" name="stc4" value="TRUE"> True</label> &nbsp; <label><input type="radio" name="stc4" value="FALSE"> False</label> &nbsp; <label><input type="radio" name="stc4" value="NOT STATED"> Not stated</label></div>
          <div data-q="stc5" data-key="FALSE" style="margin-top:12px;font-size:13.5px;">5. The film gives detailed statistics throughout.<br><label><input type="radio" name="stc5" value="TRUE"> True</label> &nbsp; <label><input type="radio" name="stc5" value="FALSE"> False</label> &nbsp; <label><input type="radio" name="stc5" value="NOT STATED"> Not stated</label></div>
          <div data-q="stc6" data-key="NOT STATED" style="margin-top:12px;font-size:13.5px;">6. Every viewer donated money after watching it.<br><label><input type="radio" name="stc6" value="TRUE"> True</label> &nbsp; <label><input type="radio" name="stc6" value="FALSE"> False</label> &nbsp; <label><input type="radio" name="stc6" value="NOT STATED"> Not stated</label></div>
          <button type="button" data-check-practice style="margin-top:16px;padding:9px 13px;border:0;border-radius:7px;background:#15171A;color:#fff;font-weight:700;cursor:pointer;">Check evidence questions</button>
          <span data-quiz-result style="margin-left:10px;font-size:13px;font-weight:700;color:#2F5F82;"></span>
        </div>
      </section>

      <section id="decode-listening-s8" data-listening-item="D-S8-01" style="margin-top:24px;border:1px solid rgba(47,95,130,.22);border-radius:14px;overflow:hidden;background:#fff;">
        <div style="padding:18px 22px;background:#EEF5FA;border-bottom:1px solid rgba(47,95,130,.15);">
          <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#2F5F82;">03 · S08 · D-S8-01</div>
          <div style="font-family:'IBM Plex Sans',sans-serif;font-weight:700;font-size:22px;color:#15171A;margin-top:6px;">Dove · Real Beauty Sketches</div>
          <div style="font-family:'IBM Plex Sans',sans-serif;font-size:13.5px;line-height:1.55;color:#555;margin-top:6px;">Official Dove campaign page. Watch the film, then compare the social message with its commercial purpose.</div>
          <a href="https://www.dove.com/us/en/campaigns/purpose/real-beauty-sketches.html" target="_blank" rel="noopener noreferrer" style="display:inline-block;margin-top:11px;padding:9px 12px;border-radius:7px;background:#2F5F82;color:#fff;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;">Open official campaign ↗</a>
        </div>
        <div data-practice-quiz="dove" style="padding:20px 22px;">
          <div style="font-weight:700;font-size:14px;">First viewing · sequence</div>
          <div style="font-size:13px;line-height:1.55;color:#555;margin-top:5px;">Number these events 1–4 in your workbook: a stranger describes the same woman; the woman describes herself; the woman compares the two finished sketches; the artist draws from descriptions without seeing the woman.</div>
          <div style="font-weight:700;font-size:14px;margin-top:18px;">Second viewing · detail</div>
          <div data-q="dove1" data-key="B" style="margin-top:10px;font-size:13.5px;">1. Why can the artist not see the women while he draws?<br><label><input type="radio" name="dove1" value="A"> A. He is in another city.</label><br><label><input type="radio" name="dove1" value="B"> B. He must work only from their descriptions.</label><br><label><input type="radio" name="dove1" value="C"> C. The women do not want a portrait.</label><br><label><input type="radio" name="dove1" value="D"> D. The campaign has no camera.</label></div>
          <div data-q="dove2" data-key="B" style="margin-top:12px;font-size:13.5px;">2. What is normally different about the stranger's description?<br><label><input type="radio" name="dove2" value="A"> A. More negative</label> &nbsp; <label><input type="radio" name="dove2" value="B"> B. More positive and less critical</label><br><label><input type="radio" name="dove2" value="C"> C. It contains product prices</label> &nbsp; <label><input type="radio" name="dove2" value="D"> D. It describes a different person</label></div>
          <div data-q="dove3" data-key="B" style="margin-top:12px;font-size:13.5px;">3. What is the main message of the film?<br><label><input type="radio" name="dove3" value="A"> A. Only professional models are beautiful</label><br><label><input type="radio" name="dove3" value="B"> B. People may judge their appearance more critically than other people do</label><br><label><input type="radio" name="dove3" value="C"> C. A forensic artist can sell more soap</label><br><label><input type="radio" name="dove3" value="D"> D. Every advertisement needs two portraits</label></div>
          <div data-q="dove4" data-key="A" style="margin-top:12px;font-size:13.5px;">4. Which appeal is strongest?<br><label><input type="radio" name="dove4" value="A"> A. Emotional</label> &nbsp; <label><input type="radio" name="dove4" value="B"> B. Rational</label> &nbsp; <label><input type="radio" name="dove4" value="C"> C. Price</label> &nbsp; <label><input type="radio" name="dove4" value="D"> D. No persuasive appeal</label></div>
          <button type="button" data-check-practice style="margin-top:16px;padding:9px 13px;border:0;border-radius:7px;background:#15171A;color:#fff;font-weight:700;cursor:pointer;">Check detail questions</button>
          <span data-quiz-result style="margin-left:10px;font-size:13px;font-weight:700;color:#2F5F82;"></span>
        </div>
      </section>

      <section id="decode-listening-s9" data-listening-item="D-S9-W02" data-audio-id="AD-EXPOSE-R2-S9-CLEANSTEP-TRACK01" style="margin-top:24px;border:2px solid #171717;border-radius:14px;overflow:hidden;background:#FFFDF4;">
        <div style="padding:18px 22px;background:#15171A;color:#fff;">
          <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#7EB6E8;">04 · S09 · D-S9-W02</div>
          <div style="font-family:'IBM Plex Sans',sans-serif;font-weight:700;font-size:22px;margin-top:6px;">CleanStep SIGNAL Briefing</div>
          <div style="font-family:'IBM Plex Sans',sans-serif;font-size:13.5px;line-height:1.55;color:#D8D8D5;margin-top:6px;">Listen twice. First identify the main problem; then locate the evidence. The practice transcript unlocks after your first complete attempt for error analysis.</div>
        </div>
        <div style="padding:20px 22px;">
          <audio id="cleanstep-practice-audio" data-cleanstep-main controls="{{{{ true }}}}" preload="metadata" src="./audio/ad-expose/decode/cleanstep-s9.mp3" style="width:100%;"></audio>
          <div data-cleanstep-status style="margin-top:8px;font-family:'IBM Plex Mono',monospace;font-size:10.5px;font-weight:600;color:#2F5F82;">Complete plays: 0/2</div>

          <div data-practice-quiz="cleanstep" style="margin-top:20px;">
            <div data-q="cs1" data-key="B" style="font-size:13.5px;">1. What problem does Vasquez identify?<br><label><input type="radio" name="cs1" value="A"> A. No brand name</label> &nbsp; <label><input type="radio" name="cs1" value="B"> B. The environmental claim is broader than the evidence</label><br><label><input type="radio" name="cs1" value="C"> C. The ad is too short</label> &nbsp; <label><input type="radio" name="cs1" value="D"> D. The trainers are too expensive</label></div>
            <div data-q="cs2" data-key="C" style="margin-top:12px;font-size:13.5px;">2. Which part contains recycled material?<br><label><input type="radio" name="cs2" value="A"> A. Sole</label> &nbsp; <label><input type="radio" name="cs2" value="B"> B. Box</label> &nbsp; <label><input type="radio" name="cs2" value="C"> C. Upper fabric</label> &nbsp; <label><input type="radio" name="cs2" value="D"> D. Laces</label></div>
            <div data-q="cs3" data-key="B" style="margin-top:12px;font-size:13.5px;">3. What information is not explained?<br><label><input type="radio" name="cs3" value="A"> A. Colour</label><br><label><input type="radio" name="cs3" value="B"> B. Remaining materials, transport and packaging</label><br><label><input type="radio" name="cs3" value="C"> C. Company name</label> &nbsp; <label><input type="radio" name="cs3" value="D"> D. Product size</label></div>
            <div data-q="cs4" data-key="B" style="margin-top:12px;font-size:13.5px;">4. What is Vasquez's conclusion?<br><label><input type="radio" name="cs4" value="A"> A. The product definitely harms the environment</label><br><label><input type="radio" name="cs4" value="B"> B. One environmental benefit does not prove that the whole product is “100% planet-friendly”</label><br><label><input type="radio" name="cs4" value="C"> C. Recycled material is always misleading</label><br><label><input type="radio" name="cs4" value="D"> D. The company has no recycling programme</label></div>
            <button type="button" data-check-practice style="margin-top:16px;padding:9px 13px;border:0;border-radius:7px;background:#15171A;color:#fff;font-weight:700;cursor:pointer;">Check listening questions</button>
            <span data-quiz-result style="margin-left:10px;font-size:13px;font-weight:700;color:#2F5F82;"></span>
          </div>

          <div data-cleanstep-transcript-shell style="margin-top:18px;border-top:1px solid rgba(21,23,26,.14);padding-top:16px;">
            <button type="button" data-cleanstep-transcript-button disabled style="padding:9px 12px;border:1px solid #171717;border-radius:8px;background:#fff;color:#8B8A84;font-weight:700;cursor:not-allowed;">Transcript locked · complete one full listen</button>
            <div data-cleanstep-transcript hidden style="margin-top:14px;padding:15px 16px;border-left:4px solid #2F5F82;background:#F4F1E7;line-height:1.62;font-size:13.5px;">
              <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#2F5F82;margin-bottom:8px;">Read + listen again</div>
              <div>{cleanstep_transcript}</div>
              <audio controls="{{{{ true }}}}" preload="metadata" src="./audio/ad-expose/decode/cleanstep-s9.mp3" style="width:100%;margin-top:12px;"></audio>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
  </sc-if>
'''

text = text[:start] + shown + text[end:]

runtime_marker = '<!-- DECODE LISTENING GOLD RUNTIME -->'
runtime = r'''
<!-- DECODE LISTENING GOLD RUNTIME -->
<script>
(() => {
  const PLAY_KEY = 'ad-expose:AD-EXPOSE-R2-S9-CLEANSTEP-TRACK01:complete-plays';
  const JINGLE_KEY = 'ad-expose:r2:jingle-lab:v1';
  const audioState = new WeakMap();

  function cleanstepMain() { return document.querySelector('[data-cleanstep-main]'); }
  function playCount() { return Math.max(0, Math.min(2, Number(localStorage.getItem(PLAY_KEY) || 0))); }
  function renderCleanstep() {
    const plays = playCount();
    const status = document.querySelector('[data-cleanstep-status]');
    const button = document.querySelector('[data-cleanstep-transcript-button]');
    const panel = document.querySelector('[data-cleanstep-transcript]');
    if (status) status.textContent = plays >= 2 ? 'Complete plays: 2/2 · practice complete' : ('Complete plays: ' + plays + '/2');
    if (button) {
      const unlocked = plays >= 1;
      button.disabled = !unlocked;
      button.style.cursor = unlocked ? 'pointer' : 'not-allowed';
      button.style.color = unlocked ? '#171717' : '#8B8A84';
      button.textContent = unlocked ? ((panel && !panel.hidden) ? 'Hide transcript' : 'Show transcript') : 'Transcript locked · complete one full listen';
    }
  }

  function saveJingles() {
    const data = {};
    document.querySelectorAll('[data-jingle-response]').forEach(el => data[el.dataset.jingleResponse] = el.value || '');
    localStorage.setItem(JINGLE_KEY, JSON.stringify(data));
  }
  function loadJingles() {
    let data = {};
    try { data = JSON.parse(localStorage.getItem(JINGLE_KEY) || '{}'); } catch (_) {}
    document.querySelectorAll('[data-jingle-response]').forEach(el => { if (!el.value && data[el.dataset.jingleResponse]) el.value = data[el.dataset.jingleResponse]; });
  }

  document.addEventListener('input', e => {
    if (e.target && e.target.matches('[data-jingle-response]')) saveJingles();
  }, true);

  document.addEventListener('play', e => {
    const a = e.target;
    if (!(a instanceof HTMLAudioElement) || !a.matches('[data-cleanstep-main]')) return;
    const state = { startedNearZero: a.currentTime <= 0.75, invalidForwardSeek: false, maxObserved: a.currentTime || 0 };
    audioState.set(a, state);
  }, true);

  document.addEventListener('timeupdate', e => {
    const a = e.target;
    if (!(a instanceof HTMLAudioElement) || !a.matches('[data-cleanstep-main]')) return;
    const state = audioState.get(a);
    if (state) state.maxObserved = Math.max(state.maxObserved, a.currentTime || 0);
  }, true);

  document.addEventListener('seeking', e => {
    const a = e.target;
    if (!(a instanceof HTMLAudioElement) || !a.matches('[data-cleanstep-main]')) return;
    const state = audioState.get(a);
    if (state && a.currentTime > state.maxObserved + 1.5) state.invalidForwardSeek = true;
  }, true);

  document.addEventListener('ended', e => {
    const a = e.target;
    if (!(a instanceof HTMLAudioElement) || !a.matches('[data-cleanstep-main]')) return;
    const state = audioState.get(a) || {};
    if (state.startedNearZero && !state.invalidForwardSeek) {
      localStorage.setItem(PLAY_KEY, String(Math.min(2, playCount() + 1)));
    }
    renderCleanstep();
  }, true);

  document.addEventListener('click', e => {
    const check = e.target.closest && e.target.closest('[data-check-practice]');
    if (check) {
      const quiz = check.closest('[data-practice-quiz]');
      if (!quiz) return;
      const questions = [...quiz.querySelectorAll('[data-q][data-key]')];
      let correct = 0, answered = 0;
      questions.forEach(q => {
        const name = q.dataset.q;
        const selected = quiz.querySelector('input[name="' + name + '"]:checked');
        if (selected) answered += 1;
        const ok = selected && selected.value === q.dataset.key;
        if (ok) correct += 1;
        q.style.borderLeft = selected ? ('4px solid ' + (ok ? '#2A7864' : '#BD5A34')) : '4px solid #B9B7AF';
        q.style.paddingLeft = '9px';
      });
      const result = quiz.querySelector('[data-quiz-result]');
      if (result) result.textContent = answered < questions.length ? ('Answered ' + answered + '/' + questions.length + ' · correct ' + correct) : ('Correct: ' + correct + '/' + questions.length);
      return;
    }

    const transcriptButton = e.target.closest && e.target.closest('[data-cleanstep-transcript-button]');
    if (transcriptButton) {
      if (playCount() < 1) return;
      const panel = document.querySelector('[data-cleanstep-transcript]');
      if (panel) panel.hidden = !panel.hidden;
      renderCleanstep();
    }
  }, true);

  const refresh = () => { loadJingles(); renderCleanstep(); };
  document.addEventListener('DOMContentLoaded', refresh, { once: true });
  setTimeout(refresh, 300);
  setTimeout(refresh, 1200);
})();
</script>
'''

if runtime_marker in text:
    text = re.sub(r'<!-- DECODE LISTENING GOLD RUNTIME -->[\s\S]*?</script>', runtime.strip(), text, count=1)
else:
    text = text.replace('</body>', runtime + '\n</body>', 1)

required_tokens = [
    'data-listening-gold="v1"',
    'D-S5-W01', 'Jingle Lab',
    'D-S7-01', 'Most Shocking Second a Day',
    'D-S8-01', 'Real Beauty Sketches',
    'D-S9-W02', 'CleanStep SIGNAL Briefing',
    'data-cleanstep-main',
    'Transcript locked · complete one full listen',
]
for token in required_tokens:
    if token not in text:
        raise SystemExit(f'Missing DECODE listening gold token: {token}')
if re.search(r'<audio[^>]*\sautoplay(?:\s|=|>)', text, re.I):
    raise SystemExit('Autoplay detected in DECODE Listening Practice')
if 'D-S10' in text or 'SECURE-LISTENING' in text:
    raise SystemExit('Secure checkpoint listening leaked into DECODE Listening Practice')

page.write_text(text, encoding='utf-8')
print('DECODE_LISTENING_GOLD=PASS')
