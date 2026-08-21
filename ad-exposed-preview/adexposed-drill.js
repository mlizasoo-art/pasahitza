// R1 RECRUIT reusable practice content pools + review/readiness storage primitives.

export const GRAMMAR_ITEMS = [
  { id: 'g1', skill: 'be', type: 'mc', prompt: "AURÉLIA ______ the brand behind Crème Lumière.", options: ['is', 'are', 'be', 'am'], correct: 0, hint: "Use 'is' with a singular brand name.", explain: "AURÉLIA is singular, so it takes 'is'." },
  { id: 'g2', skill: 'have got', type: 'gapfill', prompt: "AURÉLIA ______ (have got) a new slogan this year.", accept: ['has got'], hint: "Third person singular of 'have got' is 'has got'.", explain: "With he / she / it (or a singular brand), use 'has got'." },
  { id: 'g3', skill: 'there is / there are', type: 'mc', prompt: "There ______ three different media in the AURÉLIA campaign.", options: ['is', 'are'], correct: 1, hint: "Look at the plural noun after the gap.", explain: "'media' here is plural, so 'there are'." },
  { id: 'g4', skill: 'Present Simple', type: 'gapfill', prompt: "SIGNAL ______ (investigate) every campaign carefully.", accept: ['investigates'], hint: "Present Simple, third person singular.", explain: "Add -s: SIGNAL investigates." },
  { id: 'g5', skill: 'Present Continuous', type: 'mc', prompt: "Right now, SIGNAL ______ the AURÉLIA campaign.", options: ['investigates', 'is investigating', 'investigate', 'investigated'], correct: 1, hint: "'Right now' signals an action in progress.", explain: "Right now = happening now = Present Continuous: is investigating." },
  { id: 'g6', skill: 'Present Simple vs Present Continuous', type: 'mc', prompt: "AURÉLIA usually ______ on billboards, but this month it ______ on social media too.", options: ['advertises / is advertising', 'is advertising / advertises', 'advertise / advertising', 'advertises / advertise'], correct: 0, hint: "'usually' signals a habit; 'this month' signals something temporary.", explain: "Habit → Present Simple (advertises); temporary/current → Present Continuous (is advertising)." },
];

export const VOCAB_ITEMS = [
  { id: 'v1', skill: 'advertiser', type: 'mc', prompt: "The company that pays for an advertisement is the ______.", options: ['consumer', 'advertiser', 'audience', 'slogan'], correct: 1 },
  { id: 'v2', skill: 'brand', type: 'mc', prompt: "AURÉLIA is the ______ people recognise in the campaign.", options: ['brand', 'service', 'claim', 'medium'], correct: 0 },
  { id: 'v3', skill: 'product', type: 'mc', prompt: "Crème Lumière is a ______. A gym class is a service.", options: ['product', 'audience', 'logo', 'purpose'], correct: 0 },
  { id: 'v4', skill: 'campaign', type: 'gapfill', prompt: "The AURÉLIA ______ uses a billboard, a commercial and a social media ad.", accept: ['campaign'] },
  { id: 'v5', skill: 'target audience', type: 'mc', prompt: "The specific group an advertiser most wants to reach is the ______.", options: ['audience', 'target audience', 'consumer', 'brand'], correct: 1 },
  { id: 'v6', skill: 'audience', type: 'mc', prompt: "A billboard can have a very wide ______.", options: ['audience', 'claim', 'slogan', 'logo'], correct: 0 },
  { id: 'v7', skill: 'consumer', type: 'mc', prompt: "A person who buys or uses the cream is a ______.", options: ['advertiser', 'consumer', 'medium', 'purpose'], correct: 1 },
  { id: 'v8', skill: 'slogan', type: 'gapfill', prompt: "A short, memorable phrase linked to a brand is called a ______.", accept: ['slogan'] },
  { id: 'v9', skill: 'claim', type: 'mc', prompt: "\"9 out of 10 people preferred this cream\" is an example of a ______.", options: ['slogan', 'claim', 'logo', 'medium'], correct: 1 },
  { id: 'v10', skill: 'purpose', type: 'gapfill', prompt: "The ______ of an advertisement is usually to inform or persuade.", accept: ['purpose'] },
  { id: 'v11', skill: 'persuade', type: 'mc', prompt: "Advertisements try to ______ consumers to consider a product.", options: ['persuade', 'advertise', 'claim', 'medium'], correct: 0 },
  { id: 'v12', skill: 'medium / media', type: 'mc', prompt: "Billboard, commercial and social media ad are three different ______.", options: ['audiences', 'media', 'brands', 'claims'], correct: 1 },
];

export const ERROR_ITEMS = [
  { id: 'e1', skill: 'Present Simple', wrong: "SIGNAL investigate every campaign.", correct: "SIGNAL investigates every campaign." },
  { id: 'e2', skill: 'be', wrong: "They is the target audience.", correct: "They are the target audience." },
  { id: 'e3', skill: 'have got', wrong: "AURÉLIA have got a new slogan.", correct: "AURÉLIA has got a new slogan." },
  { id: 'e4', skill: 'there is / there are', wrong: "There is three media.", correct: "There are three media." },
  { id: 'e5', skill: 'Present Simple', wrong: "This product don't work.", correct: "This product doesn't work." },
  { id: 'e6', skill: 'Present Continuous', wrong: "Right now, SIGNAL investigate the campaign.", correct: "Right now, SIGNAL is investigating the campaign." },
  { id: 'e7', skill: 'audience', wrong: "The audience and target audience are always the same.", correct: "The audience can be wider than the target audience." },
  { id: 'e8', skill: 'advertiser', wrong: "Lumen Skincare is the advertisement.", correct: "Lumen Skincare is the advertiser; the ad is the advertisement." },
  { id: 'e9', skill: 'purpose', wrong: "The purpose is sell more cream.", correct: "The purpose is to sell more cream." },
];

export const MATCHING_SETS = [
  { id: 'm1', skill: 'vocabulary matching', terms: ['advertiser', 'brand', 'product', 'audience'], defs: ['The company that pays for an ad.', 'The name people recognise.', 'A thing a customer can buy.', 'The people who see or hear an ad.'] },
];

const REVIEW_KEY = 'adexposed_r1_review_queue';
const ATTEMPTS_KEY = 'adexposed_r1_skill_attempts';
const EP01_KEY = 'adexposed_r1_ep01_complete';
const OFFICIAL_KEY = 'adexposed_r1_official_test_result';

export function getReviewQueue() {
  try { const raw = localStorage.getItem(REVIEW_KEY); return raw ? JSON.parse(raw) : []; } catch (e) { return []; }
}
export function addToReviewQueue(skill) {
  const q = getReviewQueue();
  if (!q.includes(skill)) { q.push(skill); localStorage.setItem(REVIEW_KEY, JSON.stringify(q)); }
}
export function removeFromReviewQueue(skill) {
  localStorage.setItem(REVIEW_KEY, JSON.stringify(getReviewQueue().filter(s => s !== skill)));
}
export function getTopWeakSkills(n) { return getReviewQueue().slice(-n).reverse(); }

export function recordSkillResult(skill, correct) {
  const raw = localStorage.getItem(ATTEMPTS_KEY);
  const data = raw ? JSON.parse(raw) : {};
  if (!data[skill]) data[skill] = { correct: 0, wrong: 0 };
  data[skill][correct ? 'correct' : 'wrong']++;
  localStorage.setItem(ATTEMPTS_KEY, JSON.stringify(data));
  if (correct && data[skill].correct >= 2 && data[skill].correct > data[skill].wrong) removeFromReviewQueue(skill);
}
export function getSkillAttempts() {
  try { const raw = localStorage.getItem(ATTEMPTS_KEY); return raw ? JSON.parse(raw) : {}; } catch (e) { return {}; }
}

export function markEP01Complete() { localStorage.setItem(EP01_KEY, '1'); }
export function isEP01Complete() { return localStorage.getItem(EP01_KEY) === '1'; }

export function getReadiness() {
  const data = getSkillAttempts();
  const score = (skills) => {
    let correct = 0, total = 0;
    skills.forEach(s => { const d = data[s]; if (d) { correct += d.correct; total += d.correct + d.wrong; } });
    return total ? Math.round((correct / total) * 100) : null;
  };
  return {
    grammar: score(GRAMMAR_ITEMS.map(i => i.skill)),
    vocabulary: score(VOCAB_ITEMS.map(i => i.skill)),
    adAnalysis: isEP01Complete() ? 100 : null,
  };
}
export function readinessLabel(pct) {
  if (pct === null || pct === undefined) return 'Not started';
  if (pct >= 80) return 'Ready';
  if (pct >= 50) return 'Developing';
  return 'Building';
}

export function isOfficialTestTaken() { return !!localStorage.getItem(OFFICIAL_KEY); }
export function setOfficialTestResult(result) { localStorage.setItem(OFFICIAL_KEY, JSON.stringify(result)); }
export function getOfficialTestResult() {
  try { const raw = localStorage.getItem(OFFICIAL_KEY); return raw ? JSON.parse(raw) : null; } catch (e) { return null; }
}
