import './adexposed-audio-v21.js';

const CONFIG_KEY = 'adexposed_teacher_config';
const LOG_KEY = 'adexposed_activity_log';
const NAME_KEY = 'adexposed_student_name';

export const DEFAULT_VISIBILITY = {
  r1_briefing: 'visible', r1_practice: 'visible', r1_languagefile: 'visible', r1_checkpoint: 'visible',
  r2_briefing: 'visible', r2_practice: 'visible', r2_checkpoint: 'visible',
  r3_briefing: 'visible', r3_practice: 'visible', r3_checkpoint: 'visible',
  r4_briefing: 'visible', r4_practice: 'visible', r4_checkpoint: 'visible',
};
export const DEFAULT_WEIGHTS = { r1: 25, r2: 25, r3: 25, r4: 25 };

export function getConfig() {
  try {
    const raw = localStorage.getItem(CONFIG_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    return {
      visibility: { ...DEFAULT_VISIBILITY, ...(parsed.visibility || {}) },
      weights: { ...DEFAULT_WEIGHTS, ...(parsed.weights || {}) },
    };
  } catch (e) {
    return { visibility: { ...DEFAULT_VISIBILITY }, weights: { ...DEFAULT_WEIGHTS } };
  }
}

export function saveConfig(config) {
  localStorage.setItem(CONFIG_KEY, JSON.stringify(config));
}

export function getStudentName() {
  return localStorage.getItem(NAME_KEY) || '';
}

export function setStudentName(name) {
  localStorage.setItem(NAME_KEY, name);
}

export function getActivityLog() {
  try {
    const raw = localStorage.getItem(LOG_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    return [];
  }
}

export function logAttempt(entry) {
  const log = getActivityLog();
  log.push({ ...entry, timestamp: new Date().toISOString() });
  if (log.length > 300) log.splice(0, log.length - 300);
  localStorage.setItem(LOG_KEY, JSON.stringify(log));
}

export function buildSubTabs({ rampKey, activeSection, config, colorDark, colorAccent, hrefs, extraSections }) {
  const vis = (config && config.visibility) || {};
  const sections = [
    { key: 'briefing', label: 'Mission Briefing' },
    { key: 'practice', label: 'Extra Practice' },
    ...(extraSections || []),
    { key: 'checkpoint', label: 'Checkpoint' },
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
          : () => { window.location.href = hrefs[s.key]; },
      };
    });
}
