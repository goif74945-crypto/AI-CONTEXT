#pragma once

#include "nexy_lo4/q64.hpp"

#include <cstdint>
#include <span>
#include <string_view>
#include <vector>

namespace nexy::lo4 {

struct ConceptDescriptor final {
    std::uint8_t id;
    std::string_view key;
    std::string_view name;
    std::string_view purpose;
};

[[nodiscard]] std::span<const ConceptDescriptor> concept_registry() noexcept;

// 01 — Budget Balance Gate
struct BudgetBalanceResult final { Q64 funding; Q64 outflow; Q64 deficit; bool balanced; };
[[nodiscard]] BudgetBalanceResult budget_balance(Q64 inflow,
                                                 Q64 authorized_mint,
                                                 Q64 payouts,
                                                 Q64 fees,
                                                 Q64 tolerance);

// 02 — Revenue Split Conservation Allocator
struct RevenueSplitResult final { std::vector<Q64> allocations; Q64 residual; };
[[nodiscard]] RevenueSplitResult allocate_revenue(Q64 total,
                                                  std::span<const Q64> weights);

// 03 — Minor-Unit Remainder Allocator
[[nodiscard]] std::vector<std::uint64_t> apportion_minor_units(std::uint64_t total_units,
                                                              std::span<const Q64> weights);

// 04 — Concentration / HHI Meter
[[nodiscard]] Q64 concentration_hhi(std::span<const Q64> normalized_shares);

// 05 — Gini Distribution Meter
[[nodiscard]] Q64 gini_index(std::span<const Q64> nonnegative_values);

// 06 — Sybil Split Sensitivity
[[nodiscard]] Q64 sybil_split_sensitivity(Q64 original_share,
                                          std::uint32_t equal_identity_count);

// 07 — Incentive Deviation Regret Gate
struct DeviationRegretResult final { Q64 regret; Q64 best_deviation; bool incentive_compatible; };
[[nodiscard]] DeviationRegretResult deviation_regret(Q64 truthful_utility,
                                                     std::span<const Q64> deviation_utilities,
                                                     Q64 tolerance);

// 08 — Collusion Capture Exposure
struct CollusionExposure final { Q64 top_k_share; bool threshold_reached; };
[[nodiscard]] CollusionExposure collusion_exposure(std::span<const Q64> normalized_shares,
                                                   std::uint32_t max_colluders,
                                                   Q64 capture_threshold);

// 09 — Wash-Activity Suspicion Meter
[[nodiscard]] Q64 wash_activity_suspicion(Q64 self_volume_ratio,
                                          Q64 reciprocal_volume_ratio,
                                          Q64 counterparty_concentration);

// 10 — Reward Leakage Meter
[[nodiscard]] Q64 reward_leakage_ratio(Q64 nonproductive_reward,
                                       Q64 total_reward);

// 11 — Subsidy Runway Estimator
struct RunwayResult final { Q64 epochs; Q64 net_burn; bool self_sustaining; };
[[nodiscard]] RunwayResult subsidy_runway(Q64 treasury,
                                          Q64 inflow_per_epoch,
                                          Q64 outflow_per_epoch);

// 12 — Solvency Coverage Gate
struct SolvencyResult final { Q64 coverage_ratio; Q64 required_assets; bool solvent; };
[[nodiscard]] SolvencyResult solvency_coverage(Q64 liquid_assets,
                                              Q64 liabilities,
                                              Q64 required_buffer_ratio);

// 13 — Dispute Reserve Sizer
struct ReserveResult final { Q64 reserve_ratio; Q64 required_reserve; };
[[nodiscard]] ReserveResult dispute_reserve(Q64 exposure,
                                            Q64 dispute_probability,
                                            Q64 loss_given_dispute,
                                            Q64 uncertainty_margin);

// 14 — Settlement Slippage Envelope
struct SlippageResult final { Q64 deviation_ratio; bool within_limit; };
[[nodiscard]] SlippageResult settlement_slippage(Q64 expected_value,
                                                 Q64 actual_value,
                                                 Q64 allowed_ratio);

// 15 — Fee Hysteresis Governor
struct FeeUpdateResult final { Q64 next_fee; Q64 requested_delta; bool changed; };
[[nodiscard]] FeeUpdateResult fee_hysteresis_update(Q64 current_fee,
                                                    Q64 target_fee,
                                                    Q64 deadband,
                                                    Q64 max_step);

// 16 — Creator Revenue Shock Guard
struct RevenueShockResult final { Q64 relative_change; bool downward; bool shock; };
[[nodiscard]] RevenueShockResult revenue_shock_guard(Q64 previous_revenue,
                                                     Q64 current_revenue,
                                                     Q64 max_drop_ratio,
                                                     Q64 max_gain_ratio);

// 17 — Cross-App Settlement Exposure
struct CrossAppExposureResult final { Q64 risk_ratio; Q64 risk_amount; };
[[nodiscard]] CrossAppExposureResult cross_app_exposure(Q64 principal,
                                                        Q64 counterparty_risk,
                                                        Q64 irreversibility,
                                                        Q64 permission_breadth);

// 18 — Rounding Conservation Gate
struct ConservationResult final { Q64 absolute_error; bool conserved; };
[[nodiscard]] ConservationResult rounding_conservation(std::span<const Q64> allocations,
                                                       Q64 expected_total,
                                                       Q64 tolerance);

// 19 — Creator No-Mint Gate
struct MintGateResult final { Q64 maximum_legal_outflow; bool allowed; };
[[nodiscard]] MintGateResult creator_value_mint_gate(Q64 inflow,
                                                     Q64 outflow,
                                                     Q64 authorized_mint,
                                                     bool creator_mode);

// 20 — Experimental Exposure Limit
struct ExposureLimitResult final { Q64 confidence_factor; Q64 maximum_exposure; };
[[nodiscard]] ExposureLimitResult experimental_exposure_limit(Q64 reserves,
                                                              Q64 isolation_strength,
                                                              Q64 rollback_strength,
                                                              Q64 evidence_strength,
                                                              Q64 max_reserve_fraction);

} // namespace nexy::lo4
