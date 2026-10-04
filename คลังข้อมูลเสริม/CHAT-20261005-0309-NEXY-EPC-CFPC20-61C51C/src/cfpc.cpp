#include "nexy_cfpc/cfpc.hpp"
#include "nexy_cfpc/sha256.hpp"

#include <algorithm>
#include <limits>
#include <sstream>
#include <stdexcept>

namespace nexy::cfpc {
namespace {
constexpr std::uint8_t MAX_EXPONENT = 8U;
constexpr std::size_t MAX_TERMS = 256U;
constexpr std::size_t MAX_DIMENSIONS = 32U;
constexpr std::uint64_t MAX_DIMENSION_VALUE = 1'000'000'000ULL;

[[nodiscard]] bool is_hash64(const std::string& s) {
  if (s.size() != 64U) return false;
  return std::all_of(s.begin(), s.end(), [](char c) {
    return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f');
  });
}

[[nodiscard]] bool valid_identifier(const std::string& s) {
  if (s.empty() || s.size() > 128U) return false;
  return std::all_of(s.begin(), s.end(), [](char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
           (c >= '0' && c <= '9') || c == '_' || c == '-' || c == '.' || c == ':';
  });
}

[[nodiscard]] i128 checked_pow_u64(std::uint64_t base, std::uint8_t exp) {
  i256 result = 1;
  i256 factor = base;
  std::uint8_t e = exp;
  while (e > 0U) {
    if ((e & 1U) != 0U) {
      result *= factor;
      if (result > i256(i128_max_value())) throw std::overflow_error("CFPC_DIMENSION_POWER_OVERFLOW");
    }
    e = static_cast<std::uint8_t>(e >> 1U);
    if (e > 0U) {
      factor *= factor;
      if (factor > i256(i128_max_value())) throw std::overflow_error("CFPC_DIMENSION_POWER_OVERFLOW");
    }
  }
  return static_cast<i128>(result);
}

[[nodiscard]] Check resource_check_id(ResourceKind kind, bool passed, std::string reason) {
  std::string id;
  switch (kind) {
    case ResourceKind::CpuWork: id="CFPC-06"; break;
    case ResourceKind::PeakMemory: id="CFPC-07"; break;
    case ResourceKind::DurableState: id="CFPC-08"; break;
    case ResourceKind::EvidenceBytes: id="CFPC-09"; break;
    case ResourceKind::Fanout: id="CFPC-10"; break;
    case ResourceKind::RetryWork: id="CFPC-11"; break;
    case ResourceKind::QueuePressure: id="CFPC-12"; break;
    case ResourceKind::SerializationBytes: id="CFPC-13"; break;
    case ResourceKind::ExternalCalls: id="CFPC-14"; break;
    case ResourceKind::VerifierWork: id="CFPC-15"; break;
  }
  return {id, passed, std::move(reason)};
}

[[nodiscard]] std::string esc(const std::string& s) {
  std::ostringstream out;
  for (const char raw_c : s) {
    const auto c = static_cast<unsigned char>(raw_c);
    switch (c) {
      case '\\': out << "\\\\"; break;
      case '"': out << "\\\""; break;
      case '\n': out << "\\n"; break;
      case '\r': out << "\\r"; break;
      case '\t': out << "\\t"; break;
      default:
        if (c < 0x20U) throw std::invalid_argument("CFPC_CONTROL_CHARACTER_FORBIDDEN");
        out << static_cast<char>(c);
    }
  }
  return out.str();
}

[[nodiscard]] bool all_passed(const std::vector<Check>& checks) {
  return std::all_of(checks.begin(), checks.end(), [](const Check& c) { return c.passed; });
}


[[nodiscard]] std::string q64_raw_text(const Q64& value) {
  return value.raw().convert_to<std::string>();
}

[[nodiscard]] std::string canonical_expression(const BoundExpression& expression) {
  std::vector<std::string> terms;
  terms.reserve(expression.terms.size());
  for (const auto& term : expression.terms) {
    std::ostringstream token;
    token << "{\"coefficient_raw\":\"" << q64_raw_text(term.coefficient) << "\",\"exponents\":{";
    bool first = true;
    for (const auto& [name, exponent] : term.exponents) {
      if (!first) token << ',';
      first = false;
      token << '"' << esc(name) << "\":" << static_cast<unsigned>(exponent);
    }
    token << "}}";
    terms.push_back(token.str());
  }
  std::sort(terms.begin(), terms.end());
  std::ostringstream out;
  out << '[';
  for (std::size_t i = 0; i < terms.size(); ++i) {
    if (i != 0U) out << ',';
    out << terms[i];
  }
  out << ']';
  return out.str();
}
}  // namespace

std::string resource_name(ResourceKind kind) {
  switch (kind) {
    case ResourceKind::CpuWork: return "cpu_work";
    case ResourceKind::PeakMemory: return "peak_memory";
    case ResourceKind::DurableState: return "durable_state";
    case ResourceKind::EvidenceBytes: return "evidence_bytes";
    case ResourceKind::Fanout: return "fanout";
    case ResourceKind::RetryWork: return "retry_work";
    case ResourceKind::QueuePressure: return "queue_pressure";
    case ResourceKind::SerializationBytes: return "serialization_bytes";
    case ResourceKind::ExternalCalls: return "external_calls";
    case ResourceKind::VerifierWork: return "verifier_work";
  }
  throw std::logic_error("CFPC_UNKNOWN_RESOURCE_KIND");
}

Check validate_workload(const Workload& workload) {
  if (workload.dimensions.empty()) return {"CFPC-05", false, "WORKLOAD_EMPTY"};
  if (workload.dimensions.size() > MAX_DIMENSIONS) return {"CFPC-05", false, "TOO_MANY_DIMENSIONS"};
  for (const auto& [name, value] : workload.dimensions) {
    if (!valid_identifier(name)) return {"CFPC-05", false, "INVALID_DIMENSION_ID"};
    if (value > MAX_DIMENSION_VALUE) return {"CFPC-05", false, "DIMENSION_LIMIT_EXCEEDED"};
  }
  return {"CFPC-05", true, "WORKLOAD_BOUND"};
}

Check validate_expression(const BoundExpression& expression) {
  if (expression.terms.empty()) return {"CFPC-02", false, "EXPRESSION_EMPTY"};
  if (expression.terms.size() > MAX_TERMS) return {"CFPC-02", false, "TOO_MANY_TERMS"};
  for (const auto& term : expression.terms) {
    if (term.exponents.size() > MAX_DIMENSIONS) return {"CFPC-02", false, "TOO_MANY_TERM_DIMENSIONS"};
    for (const auto& [name, exp] : term.exponents) {
      if (!valid_identifier(name)) return {"CFPC-02", false, "INVALID_VARIABLE_ID"};
      if (exp > MAX_EXPONENT) return {"CFPC-02", false, "EXPONENT_LIMIT_EXCEEDED"};
    }
  }
  return {"CFPC-02", true, "SUPPORTED_NONNEGATIVE_POLYNOMIAL"};
}

Check validate_coefficients(const BoundExpression& expression) {
  for (const auto& term : expression.terms) {
    if (term.coefficient.raw() < 0) return {"CFPC-03", false, "NEGATIVE_COEFFICIENT_FORBIDDEN"};
  }
  return {"CFPC-03", true, "Q64_COEFFICIENTS_VALID"};
}

Check monotonicity_witness(const BoundExpression& expression) {
  const auto v = validate_expression(expression);
  if (!v.passed) return {"CFPC-04", false, v.reason};
  const auto c = validate_coefficients(expression);
  if (!c.passed) return {"CFPC-04", false, c.reason};
  return {"CFPC-04", true, "NONNEGATIVE_POLYNOMIAL_MONOTONE_ON_NONNEGATIVE_DOMAIN"};
}

Check bind_input_vector(const Workload& workload, const BoundExpression& expression) {
  const auto w = validate_workload(workload);
  if (!w.passed) return {"CFPC-01", false, w.reason};
  const auto e = validate_expression(expression);
  if (!e.passed) return {"CFPC-01", false, e.reason};
  for (const auto& term : expression.terms) {
    for (const auto& [name, exp] : term.exponents) {
      (void)exp;
      if (!workload.dimensions.contains(name)) return {"CFPC-01", false, "UNBOUND_INPUT_DIMENSION:" + name};
    }
  }
  return {"CFPC-01", true, "INPUT_VECTOR_COMPLETE"};
}

Q64 evaluate_bound(const BoundExpression& expression, const Workload& workload) {
  const auto expression_check = validate_expression(expression);
  const auto coefficient_check = validate_coefficients(expression);
  const auto workload_check = validate_workload(workload);
  const auto bind_check = bind_input_vector(workload, expression);
  if (!expression_check.passed || !coefficient_check.passed || !workload_check.passed || !bind_check.passed) {
    throw std::invalid_argument("CFPC_BOUND_PRECONDITION_FAILED");
  }
  Q64 total = Q64::from_integer(0);
  for (const auto& term : expression.terms) {
    i128 multiplier = 1;
    for (const auto& [name, exp] : term.exponents) {
      const auto it = workload.dimensions.find(name);
      if (it == workload.dimensions.end()) throw std::logic_error("CFPC_UNBOUND_DIMENSION_INTERNAL");
      const i128 power = checked_pow_u64(it->second, exp);
      const i256 combined = i256(multiplier) * i256(power);
      if (combined > i256(i128_max_value())) throw std::overflow_error("CFPC_MONOMIAL_MULTIPLIER_OVERFLOW");
      multiplier = static_cast<i128>(combined);
    }
    total = total.checked_add(term.coefficient.checked_mul_integer(multiplier));
  }
  return total;
}

BoundExpression add_bounds(const BoundExpression& a, const BoundExpression& b) {
  BoundExpression out;
  if (a.terms.size() + b.terms.size() > MAX_TERMS) throw std::length_error("CFPC_COMPOSED_BOUND_TOO_LARGE");
  out.terms.reserve(a.terms.size() + b.terms.size());
  out.terms.insert(out.terms.end(), a.terms.begin(), a.terms.end());
  out.terms.insert(out.terms.end(), b.terms.begin(), b.terms.end());
  return out;
}

Check verification_preservation(const ProposalBoundSpec& spec) {
  if (spec.required_verification_steps.empty()) return {"CFPC-15", false, "REQUIRED_VERIFICATION_SET_EMPTY"};
  for (const auto& step : spec.required_verification_steps) {
    if (!valid_identifier(step)) return {"CFPC-15", false, "INVALID_VERIFICATION_STEP_ID"};
    if (!spec.provided_verification_steps.contains(step)) {
      return {"CFPC-15", false, "REQUIRED_VERIFICATION_STEP_MISSING:" + step};
    }
  }
  return {"CFPC-15", true, "VERIFICATION_OBLIGATIONS_PRESERVED"};
}

Check budget_dominance(ResourceKind kind, const Q64& value, const Q64& budget) {
  if (budget.raw() < 0) return {"CFPC-16", false, "NEGATIVE_BUDGET"};
  return {"CFPC-16", value <= budget, value <= budget ? "BOUND_WITHIN_BUDGET:" + resource_name(kind)
                                                       : "BOUND_EXCEEDS_BUDGET:" + resource_name(kind)};
}

Check degradation_contract_gate(const DegradationContract& contract) {
  const bool pass = contract.preserves_authority
                 && contract.preserves_required_verification
                 && contract.emits_freeze_when_budget_exceeded
                 && !contract.silently_drops_evidence
                 && !contract.silently_skips_verification;
  return {"CFPC-18", pass, pass ? "FAIL_CLOSED_DEGRADATION" : "UNSAFE_DEGRADATION_CONTRACT"};
}

Check authority_non_interference(bool requests_canon_mutation,
                                 bool requests_core_state_mutation,
                                 bool requests_auto_promotion) {
  const bool pass = !requests_canon_mutation && !requests_core_state_mutation && !requests_auto_promotion;
  return {"CFPC-19", pass, pass ? "ADVISORY_ONLY" : "AUTHORITY_ESCALATION_FORBIDDEN"};
}

std::string canonicalize(const ProposalBoundSpec& spec,
                         const Workload& workload,
                         const std::map<ResourceKind, Q64>& values,
                         const std::vector<Check>& checks,
                         Verdict verdict) {
  std::ostringstream out;
  out << "{\"proposal_id\":\"" << esc(spec.proposal_id)
      << "\",\"spec_hash\":\"" << esc(spec.spec_hash)
      << "\",\"code_hash\":\"" << esc(spec.code_hash) << "\"";

  std::vector<std::string> assumptions = spec.assumptions;
  std::sort(assumptions.begin(), assumptions.end());
  out << ",\"assumptions\":[";
  for (std::size_t i = 0; i < assumptions.size(); ++i) {
    if (i != 0U) out << ',';
    out << '"' << esc(assumptions[i]) << '"';
  }
  out << ']';

  out << ",\"resource_policy\":[";
  std::vector<const ResourceClaim*> claims;
  claims.reserve(spec.resources.size());
  for (const auto& claim : spec.resources) claims.push_back(&claim);
  std::sort(claims.begin(), claims.end(), [](const ResourceClaim* a, const ResourceClaim* b) {
    return static_cast<unsigned>(a->kind) < static_cast<unsigned>(b->kind);
  });
  for (std::size_t i = 0; i < claims.size(); ++i) {
    if (i != 0U) out << ',';
    const auto& claim = *claims[i];
    out << "{\"kind\":\"" << resource_name(claim.kind)
        << "\",\"budget_raw\":\"" << q64_raw_text(claim.budget)
        << "\",\"upper_bound\":" << canonical_expression(claim.upper_bound) << '}';
  }
  out << ']';

  out << ",\"required_verification\":[";
  bool first = true;
  for (const auto& step : spec.required_verification_steps) {
    if (!first) out << ',';
    first = false;
    out << '"' << esc(step) << '"';
  }
  out << "],\"provided_verification\":[";
  first = true;
  for (const auto& step : spec.provided_verification_steps) {
    if (!first) out << ',';
    first = false;
    out << '"' << esc(step) << '"';
  }
  out << ']';

  out << ",\"degradation\":{"
      << "\"preserves_authority\":" << (spec.degradation.preserves_authority ? "true" : "false")
      << ",\"preserves_required_verification\":" << (spec.degradation.preserves_required_verification ? "true" : "false")
      << ",\"emits_freeze_when_budget_exceeded\":" << (spec.degradation.emits_freeze_when_budget_exceeded ? "true" : "false")
      << ",\"silently_drops_evidence\":" << (spec.degradation.silently_drops_evidence ? "true" : "false")
      << ",\"silently_skips_verification\":" << (spec.degradation.silently_skips_verification ? "true" : "false")
      << '}';

  out << ",\"workload\":{";
  first = true;
  for (const auto& [name, value] : workload.dimensions) {
    if (!first) out << ',';
    first = false;
    out << '"' << esc(name) << "\":" << value;
  }
  out << "},\"bounds_raw\":{";
  first = true;
  for (const auto& [kind, value] : values) {
    if (!first) out << ',';
    first = false;
    out << '"' << resource_name(kind) << "\":\"" << q64_raw_text(value) << "\"";
  }
  out << "},\"checks\":[";
  for (std::size_t i = 0; i < checks.size(); ++i) {
    if (i != 0U) out << ',';
    out << "{\"id\":\"" << esc(checks[i].mechanism_id)
        << "\",\"pass\":" << (checks[i].passed ? "true" : "false")
        << ",\"reason\":\"" << esc(checks[i].reason) << "\"}";
  }
  out << "],\"verdict\":\"" << (verdict == Verdict::Pass ? "PASS" : "FREEZE") << "\"}";
  return out.str();
}

Evaluation evaluate_proposal(const ProposalBoundSpec& spec,
                             const Workload& worst_case,
                             bool requests_canon_mutation,
                             bool requests_core_state_mutation,
                             bool requests_auto_promotion) {
  Evaluation result;
  result.checks.push_back({"CFPC-20", false, "CERTIFICATE_INCOMPLETE"});

  if (!valid_identifier(spec.proposal_id) || !is_hash64(spec.spec_hash) || !is_hash64(spec.code_hash)) {
    result.checks.push_back({"CFPC-20", false, "IDENTITY_OR_HASH_INVALID"});
    result.verdict = Verdict::Freeze;
    result.canonical_record = canonicalize(spec, worst_case, result.observed_bounds, result.checks, result.verdict);
    result.certificate_sha256 = sha256_hex(result.canonical_record);
    return result;
  }
  if (spec.resources.empty()) {
    result.checks.push_back({"CFPC-20", false, "RESOURCE_CLAIMS_EMPTY"});
    result.verdict = Verdict::Freeze;
    result.canonical_record = canonicalize(spec, worst_case, result.observed_bounds, result.checks, result.verdict);
    result.certificate_sha256 = sha256_hex(result.canonical_record);
    return result;
  }

  const auto workload_check = validate_workload(worst_case);
  result.checks.push_back(workload_check);
  result.checks.push_back(verification_preservation(spec));
  result.checks.push_back(degradation_contract_gate(spec.degradation));
  result.checks.push_back(authority_non_interference(requests_canon_mutation, requests_core_state_mutation, requests_auto_promotion));

  std::set<ResourceKind> seen;
  std::vector<const ResourceClaim*> ordered_claims;
  ordered_claims.reserve(spec.resources.size());
  for (const auto& claim : spec.resources) ordered_claims.push_back(&claim);
  std::sort(ordered_claims.begin(), ordered_claims.end(), [](const ResourceClaim* a, const ResourceClaim* b) {
    return static_cast<unsigned>(a->kind) < static_cast<unsigned>(b->kind);
  });
  for (const ResourceClaim* claim_ptr : ordered_claims) {
    const auto& claim = *claim_ptr;
    if (!seen.insert(claim.kind).second) {
      result.checks.push_back(resource_check_id(claim.kind, false, "DUPLICATE_RESOURCE_CLAIM"));
      continue;
    }
    const auto bind = bind_input_vector(worst_case, claim.upper_bound);
    result.checks.push_back(bind);
    result.checks.push_back(validate_expression(claim.upper_bound));
    result.checks.push_back(validate_coefficients(claim.upper_bound));
    result.checks.push_back(monotonicity_witness(claim.upper_bound));
    try {
      const Q64 value = evaluate_bound(claim.upper_bound, worst_case);
      result.observed_bounds.emplace(claim.kind, value);
      const auto budget = budget_dominance(claim.kind, value, claim.budget);
      result.checks.push_back(resource_check_id(claim.kind, budget.passed, budget.reason));
      result.checks.push_back(budget);
    } catch (const std::exception& ex) {
      result.checks.push_back(resource_check_id(claim.kind, false, std::string("BOUND_EVALUATION_FAILED:") + ex.what()));
    }
  }

  const std::set<ResourceKind> required = {
    ResourceKind::CpuWork, ResourceKind::PeakMemory, ResourceKind::DurableState,
    ResourceKind::EvidenceBytes, ResourceKind::Fanout, ResourceKind::RetryWork,
    ResourceKind::QueuePressure, ResourceKind::SerializationBytes,
    ResourceKind::ExternalCalls, ResourceKind::VerifierWork
  };
  for (const auto kind : required) {
    if (!seen.contains(kind)) result.checks.push_back(resource_check_id(kind, false, "REQUIRED_RESOURCE_CLAIM_MISSING"));
  }

  result.checks.erase(result.checks.begin()); // replace provisional CFPC-20 last
  const bool pass = all_passed(result.checks);
  result.checks.push_back({"CFPC-20", pass, pass ? "FEASIBILITY_CERTIFICATE_READY" : "FEASIBILITY_CERTIFICATE_FREEZE"});
  result.verdict = all_passed(result.checks) ? Verdict::Pass : Verdict::Freeze;
  result.canonical_record = canonicalize(spec, worst_case, result.observed_bounds, result.checks, result.verdict);
  result.certificate_sha256 = sha256_hex(result.canonical_record);
  return result;
}

}  // namespace nexy::cfpc
