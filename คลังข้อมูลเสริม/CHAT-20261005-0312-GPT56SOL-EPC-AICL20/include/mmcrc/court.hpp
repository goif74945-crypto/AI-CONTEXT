#pragma once
#include "mmcrc/q64.hpp"
#include <array>
#include <cstdint>
#include <optional>
#include <set>
#include <string>
#include <string_view>
#include <vector>

namespace mmcrc {
using ModeSet = std::set<std::string>;
struct AdapterManifest {
  std::string id; std::string provider; std::string schema_version; ModeSet supported_modes;
  bool deterministic_capable{}; bool critical{}; std::int64_t timeout_ms{}; std::int64_t max_context{};
  bool has_execute{}; bool has_cancel{}; bool has_healthcheck{};
};
struct EvidenceRecord {
  std::string id; std::string source; std::string source_type; std::string hash; Q64 confidence{};
  bool verified{}; std::int64_t anchor_start{}; std::int64_t anchor_end{}; std::string normalization_version;
};
struct ProviderTrace {
  std::string provider; std::string model_identity; std::string schema_version; ModeSet supported_modes;
  std::int64_t timeout_ms{}; std::int64_t max_context{}; std::int64_t admitted_context{}; int http_status{};
  bool timed_out{}; bool cancelled{}; bool cancel_acknowledged{}; bool response_parse_ok{}; bool output_nonempty{};
  bool reasoning_present{}; bool evidence_parse_ok{}; std::optional<Q64> confidence;
  std::string semantic_digest; std::string response_digest;
};
struct GateResult { bool pass{}; std::string code; Q64 score{}; std::vector<std::string> blockers; };
struct DifferentialResult { bool equivalent{}; Q64 agreement{}; std::vector<std::string> divergent_fields; };
struct QualificationCapsule {
  std::string candidate_id; std::string baseline_commit; std::string spec_hash; std::string verdict;
  Q64 resilience_score{}; std::vector<std::string> blockers; std::string replay_hash;
  bool authority_mutation_allowed{}; bool promotion_allowed{};
};
GateResult adapter_contract_completeness(const AdapterManifest&);
GateResult provider_identity_integrity(const AdapterManifest&, std::string_view);
GateResult mode_set_equivalence(const ModeSet&, const ModeSet&);
GateResult context_ceiling_compatibility(std::int64_t,std::int64_t);
GateResult timeout_budget_compatibility(std::int64_t,std::int64_t);
GateResult criticality_consistency(bool,bool);
GateResult health_classification_parity(const std::vector<int>&,const std::vector<std::string>&);
GateResult cancellation_contract(bool,bool,bool);
GateResult structured_response_shape(const ProviderTrace&);
GateResult evidence_provenance_preservation(const std::vector<EvidenceRecord>&);
GateResult confidence_consistency(const std::vector<ProviderTrace>&);
DifferentialResult canonical_response_equivalence(const std::vector<ProviderTrace>&);
GateResult truncation_boundary_probe(std::int64_t,const std::vector<std::int64_t>&);
std::string normalize_provider_error(int,bool,bool);
GateResult retry_safety_classifier(const std::vector<std::string>&,bool);
GateResult failover_eligibility(const std::vector<ProviderTrace>&,const ModeSet&);
GateResult model_identity_drift(std::string_view,std::string_view,bool);
DifferentialResult cross_provider_behavioral_differential(const std::vector<ProviderTrace>&);
Q64 resilience_scorecard(const std::array<Q64,8>&,const std::array<Q64,8>&);
QualificationCapsule compile_qualification_capsule(std::string,std::string,std::string,const std::vector<GateResult>&,Q64,const std::vector<std::string>&);
std::string sha256_hex(std::string_view);
std::string canonical_join(const std::vector<std::string>&);
} // namespace mmcrc
