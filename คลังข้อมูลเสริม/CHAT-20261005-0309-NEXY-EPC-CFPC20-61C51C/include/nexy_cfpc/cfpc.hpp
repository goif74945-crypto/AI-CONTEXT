#pragma once

#include "nexy_cfpc/q64.hpp"

#include <cstdint>
#include <map>
#include <optional>
#include <set>
#include <string>
#include <vector>

namespace nexy::cfpc {

struct Monomial final {
  Q64 coefficient;
  std::map<std::string, std::uint8_t> exponents;
};

struct BoundExpression final {
  std::vector<Monomial> terms;
};

struct Workload final {
  std::map<std::string, std::uint64_t> dimensions;
};

enum class ResourceKind : std::uint8_t {
  CpuWork,
  PeakMemory,
  DurableState,
  EvidenceBytes,
  Fanout,
  RetryWork,
  QueuePressure,
  SerializationBytes,
  ExternalCalls,
  VerifierWork
};

[[nodiscard]] std::string resource_name(ResourceKind kind);

struct ResourceClaim final {
  ResourceKind kind;
  BoundExpression upper_bound;
  Q64 budget;
};

struct DegradationContract final {
  bool preserves_authority{true};
  bool preserves_required_verification{true};
  bool emits_freeze_when_budget_exceeded{true};
  bool silently_drops_evidence{false};
  bool silently_skips_verification{false};
};

struct ProposalBoundSpec final {
  std::string proposal_id;
  std::string spec_hash;
  std::string code_hash;
  std::vector<std::string> assumptions;
  std::vector<ResourceClaim> resources;
  std::set<std::string> required_verification_steps;
  std::set<std::string> provided_verification_steps;
  DegradationContract degradation;
};

enum class Verdict : std::uint8_t { Pass, Freeze };

struct Check final {
  std::string mechanism_id;
  bool passed{false};
  std::string reason;
};

struct Evaluation final {
  Verdict verdict{Verdict::Freeze};
  std::vector<Check> checks;
  std::map<ResourceKind, Q64> observed_bounds;
  std::string canonical_record;
  std::string certificate_sha256;
};

// 01 Input Size Vector Binder
[[nodiscard]] Check bind_input_vector(const Workload& workload, const BoundExpression& expression);
// 02 Complexity Expression Validator
[[nodiscard]] Check validate_expression(const BoundExpression& expression);
// 03 Q64 Coefficient Conformance Gate
[[nodiscard]] Check validate_coefficients(const BoundExpression& expression);
// 04 Monotonicity Witness for supported nonnegative polynomials
[[nodiscard]] Check monotonicity_witness(const BoundExpression& expression);
// 05 Worst-Case Workload Binder
[[nodiscard]] Check validate_workload(const Workload& workload);
// 06 CPU Work Upper-Bound Verifier
// 07 Peak Memory Upper-Bound Verifier
// 08 Durable State Growth Verifier
// 09 Evidence Growth Verifier
// 10 Fan-Out Amplification Verifier
// 11 Retry Multiplication Verifier
// 12 Queue Pressure Verifier
// 13 Serialization Growth Verifier
// 14 External Call Ceiling Verifier
// 15 Verification Work Preservation Verifier
[[nodiscard]] Check verification_preservation(const ProposalBoundSpec& spec);
// 16 Budget Dominance Analyzer
[[nodiscard]] Check budget_dominance(ResourceKind kind, const Q64& value, const Q64& budget);
// 17 Bound Composition Engine
[[nodiscard]] Q64 evaluate_bound(const BoundExpression& expression, const Workload& workload);
[[nodiscard]] BoundExpression add_bounds(const BoundExpression& a, const BoundExpression& b);
// 18 Fail-Closed Degradation Contract Verifier
[[nodiscard]] Check degradation_contract_gate(const DegradationContract& contract);
// 19 Canon/Authority Non-Interference Gate
[[nodiscard]] Check authority_non_interference(bool requests_canon_mutation,
                                               bool requests_core_state_mutation,
                                               bool requests_auto_promotion);
// 20 Feasibility Certificate Builder
[[nodiscard]] Evaluation evaluate_proposal(const ProposalBoundSpec& spec,
                                           const Workload& worst_case,
                                           bool requests_canon_mutation = false,
                                           bool requests_core_state_mutation = false,
                                           bool requests_auto_promotion = false);

[[nodiscard]] std::string canonicalize(const ProposalBoundSpec& spec,
                                       const Workload& workload,
                                       const std::map<ResourceKind, Q64>& values,
                                       const std::vector<Check>& checks,
                                       Verdict verdict);

}  // namespace nexy::cfpc
