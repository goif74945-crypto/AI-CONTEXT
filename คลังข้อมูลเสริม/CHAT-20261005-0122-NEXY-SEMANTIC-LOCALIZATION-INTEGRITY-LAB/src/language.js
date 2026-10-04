const RULES = Object.freeze({
  en: Object.freeze({
    PROHIBITION: [
      /\bmust\s+not\b/giu,
      /\bshall\s+not\b/giu,
      /\bdo\s+not\b/giu,
      /\bnever\b/giu,
      /\bforbidden\b/giu,
      /\bprohibited\b/giu,
      /\bnot\s+allowed\b/giu
    ],
    OBLIGATION: [
      /\bmust\b/giu,
      /\bshall\b/giu,
      /\brequired\b/giu,
      /\bneeds?\s+to\b/giu,
      /\bis\s+required\s+to\b/giu
    ],
    PERMISSION: [
      /\bmay\b/giu,
      /\bpermitted\b/giu,
      /\ballowed\b/giu,
      /\bcan\b/giu
    ],
    RECOMMENDATION: [
      /\bshould\b/giu,
      /\brecommended\b/giu
    ],
    NEGATION: [
      /\bnot\b/giu,
      /\bno\b/giu,
      /\bnever\b/giu,
      /\bwithout\b/giu,
      /\bcannot\b/giu,
      /\bcan't\b/giu,
      /\bdoesn't\b/giu,
      /\bdon't\b/giu
    ]
  }),
  th: Object.freeze({
    PROHIBITION: [
      /ห้าม/gu,
      /ต้องไม่/gu,
      /อย่า/gu,
      /ไม่อนุญาต/gu
    ],
    OBLIGATION: [
      /ต้อง/gu,
      /จำเป็นต้อง/gu,
      /จำเป็น/gu
    ],
    PERMISSION: [
      /อาจ/gu,
      /สามารถ/gu,
      /อนุญาต/gu
    ],
    RECOMMENDATION: [
      /ควร/gu,
      /แนะนำ/gu
    ],
    NEGATION: [
      /ไม่/gu,
      /ห้าม/gu,
      /อย่า/gu,
      /ไม่มี/gu,
      /โดยไม่มี/gu
    ]
  })
});

const NORMATIVE_CLASSES = Object.freeze(["PROHIBITION", "OBLIGATION", "PERMISSION", "RECOMMENDATION"]);

function countMatches(text, regexes) {
  let count = 0;
  for (const regex of regexes) {
    regex.lastIndex = 0;
    count += [...text.matchAll(regex)].length;
  }
  return count;
}

export function analyzeLanguageSemantics(text, language) {
  const rules = RULES[language];
  if (!rules) {
    return {
      supported: false,
      language,
      normative: Object.fromEntries(NORMATIVE_CLASSES.map((name) => [name, 0])),
      negationCount: 0,
      hasNormativeSignal: false
    };
  }

  const normative = {};
  for (const name of NORMATIVE_CLASSES) normative[name] = countMatches(text, rules[name]);

  // PROHIBITION patterns often contain obligation words ("must not", "ต้องไม่").
  // The gate cares about semantic class presence, not naive token overlap, so suppress
  // one overlapping OBLIGATION signal per explicit prohibition occurrence.
  normative.OBLIGATION = Math.max(0, normative.OBLIGATION - normative.PROHIBITION);

  const negationCount = countMatches(text, rules.NEGATION);
  return {
    supported: true,
    language,
    normative,
    negationCount,
    hasNormativeSignal: Object.values(normative).some((count) => count > 0)
  };
}

export function compareNormativeSemantics(sourceAnalysis, targetAnalysis) {
  const mismatches = [];
  for (const name of NORMATIVE_CLASSES) {
    const sourcePresent = sourceAnalysis.normative[name] > 0;
    const targetPresent = targetAnalysis.normative[name] > 0;
    if (sourcePresent !== targetPresent) {
      mismatches.push({ class: name, sourcePresent, targetPresent });
    }
  }
  return mismatches;
}

export const SUPPORTED_LANGUAGES = Object.freeze(Object.keys(RULES));
