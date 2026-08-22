# AD EXPOSE · Learner Navigation Gold v2

Status: **GOLD · ROUTE CONTRACT**
Date: 2026-08-22
Supersedes: history-driven `← Back` behavior from navigation v1.

## Principle

The visible in-site back arrow represents **hierarchy**, not browser history. It must always point to a deterministic parent route. `document.referrer`, `history.back()` and equivalent history-dependent behavior are forbidden for the AD EXPOSE navigation control.

The browser's own Back button is not modified.

## Route graph

### Level 0 · AD EXPOSE

- `AdExposed-Hub.dc.html` = unit/ramp hub.

### Level 1 · Ramp overview

Each ramp overview is its Mission Briefing:

- R1 → `AdExposed-Ramp1-Recruit-Briefing.dc.html`
- R2 → `AdExposed-Ramp2-Decode-Briefing.dc.html`
- R3 → `AdExposed-Ramp3-Expose-Briefing.dc.html`
- R4 → `AdExposed-Ramp4-Create-Briefing.dc.html`

Visible parent arrow on every Mission Briefing:

- `← AD EXPOSE home` → Hub.

### Level 2 · Ramp sections

For every ramp:

- Listening Practice → that ramp's Mission Briefing.
- Extra Practice → that ramp's Mission Briefing.
- Checkpoint → that ramp's Mission Briefing.

Visible parent arrow:

- `← Ramp 01 overview`, `← Ramp 02 overview`, `← Ramp 03 overview` or `← Ramp 04 overview`.

The global ramp navigation always opens the selected ramp's Mission Briefing, never the last submenu visited in that ramp.

### Level 3 · Section detail

DECODE Listening Practice:

- Library → Ramp 02 overview through the site-level parent arrow.
- Individual listening/viewing activity → `← All listening activities` → DECODE Listening library.

RECRUIT nested practice routes:

- `Who / What / Whom` → `← Extra Practice` → RECRUIT Extra Practice.
- `Language File` → `← Extra Practice` → RECRUIT Extra Practice.
- `Drill` → `← Language File` → RECRUIT Language File.

## Always-available escape routes

- Global AD EXPOSE logo/breadcrumb → Hub.
- `All ramps` → Hub.
- Global ramp tabs → selected ramp Mission Briefing.
- Four ramp-section tabs → selected section inside the current ramp.

These escape routes do not change the deterministic parent of the current page.

## Anti-loop rules

The following route loops are explicitly forbidden:

- Listening → Mission Briefing → Listening through the visible parent arrow.
- Extra Practice → Mission Briefing → Extra Practice through the visible parent arrow.
- Checkpoint → Mission Briefing → Checkpoint through the visible parent arrow.
- Cross-ramp history return caused by `document.referrer`.

The publisher must fail if any learner ramp page contains `document.referrer`, `window.history.back()` or `data-ramp-back-runtime` as part of the site-level navigation.

## QA scope

Publication validates:

- 16 core routes: 4 ramps × Mission Briefing / Listening Practice / Extra Practice / Checkpoint;
- RECRUIT Language File;
- RECRUIT Who / What / Whom;
- RECRUIT Drill;
- DECODE library → detail → library hierarchy;
- `All ramps` escape hatch;
- no history-driven site-level Back behavior.

This route graph is the default navigation pattern for future AD EXPOSE descendants unless an explicit structural-change decision supersedes it.
