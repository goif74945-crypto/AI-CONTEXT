#pragma once
#include "mmcrc/q64.hpp"
#include <array>
#include <cstdint>
#include <map>
#include <optional>
#include <set>
#include <string>
#include <string_view>
#include <vector>

namespace mmcrc {

using ModeSet = std::set<std::string>;

struct AdapterManifest {
  std::string id;
  std::string provider;
  std::string schema_version;
  ModeSet supported_modes;
  bool deterministic_capable{};
  bool critical{};
  std::int64_t timeout_ms{};
  std::int64_t max_context{};
  bool has_execute{};
  bool has_cancel{};
  bool has_healthcheck{};
};

struct EvidenceRecord {
  std::string id;
  std::string source;
  std::string source_type;
  std::string hash;
  Q64 confidence{};
  bool verified{};
  std::int64_t anchor_start{};
  std::int64_t anchor_end{};
  std::string normalization_version;
};

struct CanonicalResponse {
  std::string answer;
  std::string reasoning_hash;
  Q64 confidence{};
  std::vector<EvidenceRecord> evidence;
  std::vector<std::string> context_shard;
};

struct ProviderTrace {
  std::string provider;
  std::string model_identity;
  std::string schema_version;
  ModeSet supported_modes;
  std::int64_t timeout_ms{};
  std::int64_t max_context{};
  std::int64_t admitted_context{};
  int http_status{};
  bool timed_out{};
  bool cancelled{};
  bool cancel_acknowledged{};
  bool response_parse_ok{};
  bool output_nonempty{};
  bool reasoning_present{};
  bool evidence_parse_ok{};
  std::optional<Q64> confidence;
  std::string semantic_digest;
  std::string response_digest;
};

struct GateResult {
  bool pass{};
  std::string code;
  Q64 score{};
  std::vector<std::string> blockers;
};

struct DifferentialResult {
  bool equivalent{};
  Q64 agreement{};
  std::vector<std::string> divergent_fields;
};

struct QualificationCapsule {
  std::string candidate_id;
  std::string baseline_commit;
  std::string spec_hash;
  std::string verdict;
  Q64 resilience_score{};
  std::vector<std::string> blockers;
  std::string replay_hash;
  bool authority_mutation_allowed{};
  bool promotion_allowed{};
};

// 01
GateResult adapter_contract_completeness(const AdapterManifest& m);
// 02
GateResult provider_identity_integrity(const AdapterManifest& m, std::string_view expected_provider);
// 03
GateResult mode_set_equivalence(const ModeSet& required, const ModeSet& actual);
// 04
GateResult context_ceiling_compatibility(std::int64_t canonical_max, std::int64_t provider_max);
// 05
GateResult timeout_budget_compatibility(std::int64_t canonical_timeout, std::int64_t provider_timeout);
// 06
GateResult criticality_consistency(bool expected_critical, bool actual_critical);
// 07
GateResult health_classification_parity(const std::vector<int>& statuses, const std::vector<std::string>& classes);
// 08
GateResult cancellation_contract(bool cancel_requested, bool acknowledgement, bool side_effect_after_cancel);
// 09
GateResult structured_response_shape(const ProviderTrace& t);
// 10
GateResult evidence_provenance_preservation(const std::vector<EvidenceRecord>& evidence);
// 11
GateResult confidence_consistency(const std::vector<ProviderTrace>& traces);
// 12
DifferentialResult canonical_response_equivalence(const std::vector<ProviderTrace>& traces);
// 13
GateResult truncation_boundary_probe(std::int64_t max_context, const std::vector<std::int64_t>& attempts);
// 14
std::string normalize_provider_error(int http_status, bool timed_out, bool parse_error);
// 15
GateResult retry_safety_classifier(const std::vector<std::string>& normalized_errors, bool operation_idempotent);
// 16
GateResult failover_eligibility(const std::vector<ProviderTrace>& traces, const ModeSet& required_modes);
// 17
GateResult model_identity_drift(std::string_view pinned_identity, std::string_view observed_identity, bool explicit_approval);
// 18
DifferentialResult cross_provider_behavioral_differential(const std::vector<ProviderTrace>& traces);
// 19
Q64 resilience_scorecard(const std::array<Q64, 8>& dimensions, const std::array<Q64, 8>& weights);
// 20
QualificationCapsule compile_qualification_capsule(
    std::string candidate_id,
    std::string baseline_commit,
    std::string spec_hash,
    const std::vector<GateResult>& hard_gates,
    Q64 score,
    const std::vector<std::string>& replay_parts);

std::string sha256_hex(std::string_view input);
std::string canonical_join(const std::vector<std::string>& parts);

} // namespace mmcrc
