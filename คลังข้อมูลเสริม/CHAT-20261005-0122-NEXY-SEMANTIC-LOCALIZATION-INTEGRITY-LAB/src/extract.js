function allMatches(text, regex, mapper = (match) => match[0]) {
  regex.lastIndex = 0;
  return [...text.matchAll(regex)].map(mapper);
}

export function normalizeText(text) {
  return String(text).normalize("NFC");
}

export function extractNumbers(text) {
  return allMatches(text, /(?<![\p{L}\p{N}_])[-+]?\d+(?:[.,]\d+)*(?:%|‰)?/gu);
}

const UNIT_ALIASES = Object.freeze(new Map([
  ["ms", "MILLISECOND"], ["millisecond", "MILLISECOND"], ["milliseconds", "MILLISECOND"], ["มิลลิวินาที", "MILLISECOND"],
  ["s", "SECOND"], ["sec", "SECOND"], ["second", "SECOND"], ["seconds", "SECOND"], ["วินาที", "SECOND"],
  ["min", "MINUTE"], ["minute", "MINUTE"], ["minutes", "MINUTE"], ["นาที", "MINUTE"],
  ["h", "HOUR"], ["hr", "HOUR"], ["hour", "HOUR"], ["hours", "HOUR"], ["ชั่วโมง", "HOUR"],
  ["day", "DAY"], ["days", "DAY"], ["วัน", "DAY"],
  ["b", "BYTE"], ["kb", "KILOBYTE"], ["mb", "MEGABYTE"], ["gb", "GIGABYTE"], ["tb", "TERABYTE"],
  ["kib", "KIBIBYTE"], ["mib", "MEBIBYTE"], ["gib", "GIBIBYTE"],
  ["px", "PIXEL"], ["hz", "HERTZ"], ["khz", "KILOHERTZ"], ["mhz", "MEGAHERTZ"], ["ghz", "GIGAHERTZ"],
  ["v", "VOLT"], ["a", "AMPERE"], ["w", "WATT"], ["kw", "KILOWATT"], ["°c", "CELSIUS"], ["°f", "FAHRENHEIT"]
]));

export function extractUnits(text) {
  const pattern = /[-+]?\d+(?:[.,]\d+)*\s*(ms|milliseconds?|มิลลิวินาที|s|sec|seconds?|วินาที|min|minutes?|นาที|h|hr|hours?|ชั่วโมง|days?|วัน|KiB|MiB|GiB|KB|MB|GB|TB|px|Hz|kHz|MHz|GHz|V|A|W|kW|°C|°F)(?![\p{L}\p{N}_])/giu;
  return allMatches(text, pattern, (match) => UNIT_ALIASES.get(match[1].toLowerCase()) ?? match[1].toUpperCase());
}

export function extractPlaceholders(text) {
  const pattern = /\$\{[A-Za-z_][A-Za-z0-9_.-]*\}|\{\{[A-Za-z_][A-Za-z0-9_.-]*\}\}|\{[A-Za-z_][A-Za-z0-9_.-]*\}|%[sdif]/gu;
  return allMatches(text, pattern);
}

export function extractUrls(text) {
  return allMatches(text, /https?:\/\/[^\s<>()\[\]{}"']+/giu, (match) => match[0].replace(/[.,;:!?]+$/u, ""));
}

export function extractEmails(text) {
  return allMatches(text, /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/giu, (match) => match[0].toLowerCase());
}

export function extractIdentifiers(text) {
  const values = [];
  values.push(...allMatches(text, /\b[0-9a-f]{64}\b/giu, (match) => match[0].toLowerCase()));
  values.push(...allMatches(text, /\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b/giu, (match) => match[0].toLowerCase()));
  values.push(...allMatches(text, /`([^`\n]+)`/gu, (match) => `\`${match[1]}\``));
  values.push(...allMatches(text, /\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b/gu));
  return values;
}

export function extractCanonicalTokens(text, canonicalTokens) {
  const found = [];
  for (const token of canonicalTokens) {
    const escaped = token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(`(?<![A-Z0-9_])${escaped}(?![A-Z0-9_])`, "gu");
    found.push(...allMatches(text, regex, () => token));
  }
  return found;
}

export function extractProtectedLiteralCounts(text, literals) {
  const counts = {};
  for (const literal of literals) {
    if (!literal) continue;
    let index = 0;
    let count = 0;
    while (true) {
      const next = text.indexOf(literal, index);
      if (next === -1) break;
      count += 1;
      index = next + literal.length;
    }
    counts[literal] = count;
  }
  return counts;
}
