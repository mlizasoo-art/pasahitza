# AD EXPOSE · RAMP 02 · DECODE · Listening Practice Gold v1.1

Status: **GOLD · LOCKED**  
Locked: 2026-08-22  
Supersedes: `AD-EXPOSE-R2-LISTENING-GOLD-v1.md` for D-S5-W01 source selection only.

## Public practice inventory

The complete public DECODE listening/viewing inventory remains four activities / seven media clips in canonical session order:

1. **S05 · D-S5-W01 · Jingle Lab**
   - Calgon
   - Autoglass
   - Chicken Tonight
   - WeBuyAnyCar.com
   - all external source-linked media; no reproduced lyrics.
2. **S07 · D-S7-01 · Save the Children — Most Shocking Second a Day**.
3. **S08 · D-S8-01 · Dove — Real Beauty Sketches**.
4. **S09 · D-S9-W02 · CleanStep SIGNAL Briefing** — SIGNAL-owned byte-locked learner audio.

## Jingle Lab source correction

The learner-facing distinction is now explicit: **a jingle is a short, simple, memorable advertising tune or sung phrase**, not merely an advertisement that contains memorable music.

- Mars Bar / Saxophonist is removed as Clip 1 because the selected source is not a sufficiently clean example of that construct.
- Jacob's Club is historically a real jingle, but it is removed as Clip 2 because its longer song-like execution is pedagogically less clean than the compact musical-phrase model intended here.
- Calgon and Autoglass replace them as clearer UK exemplars.

Canonical sources:

- Calgon: `https://www.youtube.com/watch?v=3FY0k3hLIAk`
- Autoglass: `https://www.youtube.com/watch?v=zvnvN2F1Rm4`
- Chicken Tonight: `https://www.youtube.com/watch?v=x1veMqaPOxo`
- WeBuyAnyCar.com: `https://www.youtube.com/watch?v=f-yEWZTBQ64`

The source/content wording amendment is recorded in `AD-EXPOSE-DECODE-STUDENT-MASTER-v2.1-JINGLE-LAB-AMENDMENT.md`.

## Interface and navigation

All Gold v1 interface rules remain unchanged:

- Level 1 library shows all four public activities.
- Level 2 shows one selected activity with its media and exercise.
- `← All listening activities` returns from detail to library.
- site-level parent routing follows Learner Navigation Gold v2.
- no autoplay.

## Security and media invariants

- Director Webb remains byte-locked and is never regenerated.
- DECODE Mission Briefing remains separate from Listening Practice.
- CleanStep remains byte-locked and keeps its canonical transcript policy.
- Jingle Lab / Save the Children / Dove external media remains external and is never TTS-generated.
- Secure D-S10 material never appears in public Listening Practice.

## Production durability

After the base R2 Gold builder, library/detail UI and navigation pass, `apply-jingle-lab-source-amendment.py` applies and validates the v1.1 source correction. Publication QA rejects the superseded Mars/Jacob's learner bindings and requires Calgon/Autoglass plus the unchanged Chicken Tonight and WeBuyAnyCar bindings.
