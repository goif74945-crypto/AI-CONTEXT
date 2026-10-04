import crypto from "node:crypto";
import {
  extractCanonicalTokens,
  extractEmails,
  extractIdentifiers,
  extractNumbers,
  extractUnits,
  extractPlaceholders,
  extractProtectedLiteralCounts,
  extractUrls,
  normalizeText
} from "./extract.js";
import { analyzeLanguageSemantics, compareNormativeSemantics } from "./language.js";
import { diffMultiset } from "./multiset.js";
import { loadDefaultPolicy, mergePolicy } from "./policy.js";

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonicalize(value[key])]));
  }
  return value;
}

function fingerprint(value) {
  const stable = JSON.stringify(canonicalize(value));
  return crypto.createHash("sha256").update(stable, "utf8").digest("hex");
}

function issue(code, severity, message, details = {}) {
  return { code, severity, message, details: canonicalize(details) };
}

function compareCollection({ code, severity, label, sourceValues, targetValues }) {
  const diff = diffMultiset(sourceValues, targetValues);
  if (diff.equal) return null;
  return issue(code, severity, `${label} changed across localization boundary.`, {
    missing: diff.missing,
    extra: diff.extra
  });
}


export function analyzeTranslation(contract, policyOverride = {}) {
  const defaultPolicy = loadDefaultPolicy();
  const policy = mergePolicy(defaultPolicy, policyOverride);
  const source = normalizeText(contract?.source ?? "");
  const target = normalizeText(contract?.target ?? "");
  const sourceLanguage = String(contract?.sourceLanguage ?? "").toLowerCase();
  const targetLanguage = String(contract?.targetLanguage ?? "").toLowerCase();
  const protectedLiterals = [...new Set([...(policy.protectedLiterals ?? []), ...(contract?.protectedLiterals ?? [])])].sort();
  const issues = [];

  if (source.trim().length === 0) {
    issues.push(issue("E_EMPTY_SOURCE", policy.severity.emptyInput, "Source text is empty."));
  }
  if (target.trim().length === 0) {
    issues.push(issue("E_EMPTY_TARGET", policy.severity.emptyInput, "Target text is empty."));
  }

  const sourceSemantics = analyzeLanguageSemantics(source, sourceLanguage);
  const targetSemantics = analyzeLanguageSemantics(target, targetLanguage);

  if (policy.freezeOnUnsupportedLanguage) {
    if (!sourceSemantics.supported) {
      issues.push(issue("E_UNSUPPORTED_SOURCE_LANGUAGE", policy.severity.unsupportedLanguage, "Source language is unsupported by the deterministic semantic gate.", { sourceLanguage }));
    }
    if (!targetSemantics.supported) {
      issues.push(issue("E_UNSUPPORTED_TARGET_LANGUAGE", policy.severity.unsupportedLanguage, "Target language is unsupported by the deterministic semantic gate.", { targetLanguage }));
    }
  }

  const comparisons = [];
  if (policy.preserve.numbers) {
    comparisons.push(compareCollection({
      code: "E_NUMBER_MISMATCH",
      severity: policy.severity.numberMismatch,
      label: "Numbers",
      sourceValues: extractNumbers(source),
      targetValues: extractNumbers(target)
    }));
  }
  if (policy.preserve.units) {
    comparisons.push(compareCollection({
      code: "E_UNIT_MISMATCH",
      severity: policy.severity.unitMismatch,
      label: "Semantic units",
      sourceValues: extractUnits(source),
      targetValues: extractUnits(target)
    }));
  }
  if (policy.preserve.placeholders) {
    comparisons.push(compareCollection({
      code: "E_PLACEHOLDER_MISMATCH",
      severity: policy.severity.placeholderMismatch,
      label: "Template placeholders",
      sourceValues: extractPlaceholders(source),
      targetValues: extractPlaceholders(target)
    }));
  }
  if (policy.preserve.urls) {
    comparisons.push(compareCollection({
      code: "E_URL_MISMATCH",
      severity: policy.severity.urlMismatch,
      label: "URLs",
      sourceValues: extractUrls(source),
      targetValues: extractUrls(target)
    }));
  }
  if (policy.preserve.emails) {
    comparisons.push(compareCollection({
      code: "E_EMAIL_MISMATCH",
      severity: policy.severity.emailMismatch,
      label: "Email addresses",
      sourceValues: extractEmails(source),
      targetValues: extractEmails(target)
    }));
  }
  if (policy.preserve.identifiers) {
    comparisons.push(compareCollection({
      code: "E_IDENTIFIER_MISMATCH",
      severity: policy.severity.identifierMismatch,
      label: "Protected identifiers",
      sourceValues: extractIdentifiers(source),
      targetValues: extractIdentifiers(target)
    }));
  }
  if (policy.preserve.canonicalTokens) {
    comparisons.push(compareCollection({
      code: "E_CANONICAL_TOKEN_MISMATCH",
      severity: policy.severity.canonicalTokenMismatch,
      label: "Canonical NEXY tokens",
      sourceValues: extractCanonicalTokens(source, policy.canonicalTokens),
      targetValues: extractCanonicalTokens(target, policy.canonicalTokens)
    }));
  }
  for (const comparison of comparisons) if (comparison) issues.push(comparison);

  const sourceLiteralCounts = extractProtectedLiteralCounts(source, protectedLiterals);
  const targetLiteralCounts = extractProtectedLiteralCounts(target, protectedLiterals);
  for (const literal of protectedLiterals) {
    if (sourceLiteralCounts[literal] !== targetLiteralCounts[literal]) {
      issues.push(issue("E_PROTECTED_LITERAL_MISMATCH", policy.severity.protectedLiteralMismatch, "A contract-protected literal changed across localization boundary.", {
        literal,
        sourceCount: sourceLiteralCounts[literal],
        targetCount: targetLiteralCounts[literal]
      }));
    }
  }

  if (policy.preserve.modality && sourceSemantics.supported && targetSemantics.supported) {
    const modalityMismatches = compareNormativeSemantics(sourceSemantics, targetSemantics);
    if (modalityMismatches.length > 0) {
      issues.push(issue("E_MODALITY_MISMATCH", policy.severity.modalityMismatch, "Normative modality class changed across localization boundary.", {
        mismatches: modalityMismatches
      }));
    }
  }

  if (policy.preserve.negation && sourceSemantics.supported && targetSemantics.supported) {
    const sourceHasNegation = sourceSemantics.negationCount > 0;
    const targetHasNegation = targetSemantics.negationCount > 0;
    if (sourceHasNegation !== targetHasNegation) {
      issues.push(issue("E_NEGATION_MISMATCH", policy.severity.negationMismatch, "Negation polarity changed across localization boundary.", {
        sourceHasNegation,
        targetHasNegation,
        sourceNegationCount: sourceSemantics.negationCount,
        targetNegationCount: targetSemantics.negationCount
      }));
    }
  }

  issues.sort((a, b) => a.code.localeCompare(b.code) || JSON.stringify(a.details).localeCompare(JSON.stringify(b.details)));
  const blockers = issues.filter((entry) => entry.severity === "BLOCK");
  const decision = blockers.length === 0 ? "PASS" : "FREEZE";

  const reportWithoutFingerprint = {
    proposalStatus: "AI_PROPOSED_CONCEPT_NOT_ADOPTED",
    policyVersion: policy.policyVersion,
    decision,
    sourceLanguage,
    targetLanguage,
    issueCount: issues.length,
    blockerCount: blockers.length,
    issues,
    extracted: {
      source: {
        numbers: extractNumbers(source),
        units: extractUnits(source),
        placeholders: extractPlaceholders(source),
        urls: extractUrls(source),
        emails: extractEmails(source),
        identifiers: extractIdentifiers(source),
        canonicalTokens: extractCanonicalTokens(source, policy.canonicalTokens),
        semantics: sourceSemantics
      },
      target: {
        numbers: extractNumbers(target),
        units: extractUnits(target),
        placeholders: extractPlaceholders(target),
        urls: extractUrls(target),
        emails: extractEmails(target),
        identifiers: extractIdentifiers(target),
        canonicalTokens: extractCanonicalTokens(target, policy.canonicalTokens),
        semantics: targetSemantics
      }
    }
  };

  return {
    ...reportWithoutFingerprint,
    fingerprint: fingerprint(reportWithoutFingerprint)
  };
}

export { loadDefaultPolicy, mergePolicy } from "./policy.js";
