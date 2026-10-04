#include "nexy_lo4/concepts.hpp"

#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <utility>
#include <vector>

namespace nexy::lo4 {
namespace {

constexpr std::array<ConceptDescriptor, 20> kConcepts{{
    {1, "budget_balance", "Budget Balance Gate", "Fail closed when economic outflow exceeds authorized funding."},
    {2, "revenue_split", "Revenue Split Conservation Allocator", "Allocate Q64 value without creating or losing mass."},
    {3, "minor_unit_remainder", "Minor-Unit Remainder Allocator", "Conserve discrete currency units with deterministic remainder handling."},
    {4, "concentration_hhi", "Concentration HHI Meter", "Measure settlement or reward concentration."},
    {5, "gini_distribution", "Gini Distribution Meter", "Measure inequality of nonnegative economic outcomes."},
    {6, "sybil_split", "Sybil Split Sensitivity", "Measure sensitivity to identity splitting."},
    {7, "deviation_regret", "Incentive Deviation Regret Gate", "Reject mechanisms with profitable bounded deviations."},
    {8, "collusion_capture", "Collusion Capture Exposure", "Measure capture share of the strongest bounded coalition."},
    {9, "wash_activity", "Wash-Activity Suspicion Meter", "Combine deterministic wash-activity indicators."},
    {10, "reward_leakage", "Reward Leakage Meter", "Measure rewards disconnected from productive activity."},
    {11, "subsidy_runway", "Subsidy Runway Estimator", "Estimate deterministic treasury runway under net burn."},
    {12, "solvency_coverage", "Solvency Coverage Gate", "Gate liabilities against liquid assets plus reserve buffer."},
    {13, "dispute_reserve", "Dispute Reserve Sizer", "Size reserve from exposure, loss and uncertainty."},
    {14, "settlement_slippage", "Settlement Slippage Envelope", "Bound expected versus realized settlement deviation."},
    {15, "fee_hysteresis", "Fee Hysteresis Governor", "Limit fee churn with deadband and maximum step."},
    {16, "revenue_shock", "Creator Revenue Shock Guard", "Detect abrupt creator revenue changes."},
    {17, "cross_app_exposure", "Cross-App Settlement Exposure", "Bound economic exposure crossing app boundaries."},
    {18, "rounding_conservation", "Rounding Conservation Gate", "Detect value mass lost through rounding."},
    {19, "creator_no_mint", "Creator No-Mint Gate", "Prevent creator scope from minting constitutional value."},
    {20, "experimental_exposure", "Experimental Exposure Limit", "Cap Lo4 economic exposure by evidence and recoverability."}
}};

constexpr std::size_t kMaxVector = 4096;

[[nodiscard]] Q64::wide_type max_raw_wide() {
    return (Q64::wide_type{1} << 127) - 1;
}

[[nodiscard]] Q64 q64_from_nonnegative_wide(const Q64::wide_type& value, const char* message) {
    if (value < 0 || value > max_raw_wide()) throw std::overflow_error(message);
    return Q64::from_raw(value.convert_to<Q64::storage_type>());
}

void require_nonnegative_span(std::span<const Q64> values, const char* field) {
    if (values.empty()) throw std::invalid_argument(std::string(field) + " must not be empty");
    if (values.size() > kMaxVector) throw std::invalid_argument(std::string(field) + " too large");
    for (Q64 value : values) require_nonnegative(value, field);
}

void require_distribution(std::span<const Q64> shares) {
    require_nonnegative_span(shares, "normalized_shares");
    Q64::wide_type sum = 0;
    for (Q64 share : shares) {
        require_unit(share, "normalized_share");
        sum += share.raw();
    }
    if (sum != Q64::wide_type(Q64::one().raw())) {
        throw std::invalid_argument("normalized_shares must sum exactly to Q64 one");
    }
}

[[nodiscard]] Q64 weighted_unit(std::initializer_list<std::pair<Q64, std::uint32_t>> terms) {
    Q64::wide_type numerator = 0;
    std::uint64_t denominator = 0;
    for (const auto& [value, weight] : terms) {
        require_unit(value, "weighted_unit value");
        if (weight == 0U) throw std::invalid_argument("weighted_unit weight must be positive");
        numerator += Q64::wide_type(value.raw()) * weight;
        denominator += weight;
    }
    if (denominator == 0U) throw std::invalid_argument("weighted_unit has no terms");
    return Q64::clamp01(q64_from_nonnegative_wide(numerator / denominator, "weighted_unit overflow"));
}

struct QuotientWork final {
    std::size_t index;
    Q64::wide_type quotient;
    Q64::wide_type remainder;
};

[[nodiscard]] std::vector<QuotientWork> weighted_quotients(const Q64::wide_type& total_units,
                                                           std::span<const Q64> weights) {
    if (total_units < 0) throw std::invalid_argument("total units must be nonnegative");
    require_nonnegative_span(weights, "weights");
    Q64::wide_type weight_sum = 0;
    for (Q64 weight : weights) weight_sum += weight.raw();
    if (weight_sum <= 0) throw std::invalid_argument("weight sum must be positive");

    std::vector<QuotientWork> work;
    work.reserve(weights.size());
    for (std::size_t i = 0; i < weights.size(); ++i) {
        const Q64::wide_type numerator = total_units * Q64::wide_type(weights[i].raw());
        work.push_back({i, numerator / weight_sum, numerator % weight_sum});
    }
    return work;
}

void distribute_residual(std::vector<QuotientWork>& work, Q64::wide_type residual) {
    if (residual < 0) throw std::logic_error("negative residual");
    std::vector<std::size_t> order(work.size());
    for (std::size_t i = 0; i < order.size(); ++i) order[i] = i;
    std::sort(order.begin(), order.end(), [&](std::size_t lhs, std::size_t rhs) {
        if (work[lhs].remainder != work[rhs].remainder) return work[lhs].remainder > work[rhs].remainder;
        return work[lhs].index < work[rhs].index;
    });
    std::size_t cursor = 0;
    while (residual > 0) {
        if (order.empty()) throw std::logic_error("cannot distribute residual without weights");
        work[order[cursor]].quotient += 1;
        --residual;
        cursor = (cursor + 1U) % order.size();
    }
}

} // namespace

std::span<const ConceptDescriptor> concept_registry() noexcept { return kConcepts; }

BudgetBalanceResult budget_balance(Q64 inflow, Q64 mint, Q64 payouts, Q64 fees, Q64 tolerance) {
    require_nonnegative(inflow, "inflow");
    require_nonnegative(mint, "authorized_mint");
    require_nonnegative(payouts, "payouts");
    require_nonnegative(fees, "fees");
    require_nonnegative(tolerance, "tolerance");
    const Q64 funding = inflow + mint;
    const Q64 outflow = payouts + fees;
    const Q64 deficit = Q64::max(Q64::zero(), outflow - funding);
    return {funding, outflow, deficit, deficit <= tolerance};
}

RevenueSplitResult allocate_revenue(Q64 total, std::span<const Q64> weights) {
    require_nonnegative(total, "total");
    auto work = weighted_quotients(Q64::wide_type(total.raw()), weights);
    Q64::wide_type allocated = 0;
    for (const auto& entry : work) allocated += entry.quotient;
    distribute_residual(work, Q64::wide_type(total.raw()) - allocated);

    std::vector<Q64> output(weights.size(), Q64::zero());
    Q64::wide_type final_sum = 0;
    for (const auto& entry : work) {
        output[entry.index] = q64_from_nonnegative_wide(entry.quotient, "revenue allocation overflow");
        final_sum += entry.quotient;
    }
    return {std::move(output), q64_from_nonnegative_wide(Q64::wide_type(total.raw()) - final_sum, "revenue residual overflow")};
}

std::vector<std::uint64_t> apportion_minor_units(std::uint64_t total_units, std::span<const Q64> weights) {
    auto work = weighted_quotients(Q64::wide_type(total_units), weights);
    Q64::wide_type allocated = 0;
    for (const auto& entry : work) allocated += entry.quotient;
    distribute_residual(work, Q64::wide_type(total_units) - allocated);

    std::vector<std::uint64_t> output(weights.size(), 0U);
    for (const auto& entry : work) {
        if (entry.quotient < 0 || entry.quotient > Q64::wide_type(std::numeric_limits<std::uint64_t>::max())) {
            throw std::overflow_error("minor-unit allocation overflow");
        }
        output[entry.index] = entry.quotient.convert_to<std::uint64_t>();
    }
    return output;
}

Q64 concentration_hhi(std::span<const Q64> shares) {
    require_distribution(shares);
    Q64::wide_type sum_squares = 0;
    for (Q64 share : shares) {
        sum_squares += Q64::wide_type(share.raw()) * Q64::wide_type(share.raw());
    }
    const Q64::wide_type raw = sum_squares / (Q64::wide_type{1} << 64);
    return Q64::clamp01(q64_from_nonnegative_wide(raw, "HHI overflow"));
}

Q64 gini_index(std::span<const Q64> values) {
    require_nonnegative_span(values, "gini values");
    Q64::wide_type total = 0;
    for (Q64 value : values) total += value.raw();
    if (total == 0) return Q64::zero();

    Q64::wide_type pairwise = 0;
    for (std::size_t i = 0; i < values.size(); ++i) {
        for (std::size_t j = 0; j < values.size(); ++j) {
            const Q64::wide_type a = values[i].raw();
            const Q64::wide_type b = values[j].raw();
            pairwise += a >= b ? a - b : b - a;
        }
    }
    const Q64::wide_type denominator = Q64::wide_type{2} * Q64::wide_type(values.size()) * total;
    const Q64::wide_type raw = (pairwise << 64) / denominator;
    return Q64::clamp01(q64_from_nonnegative_wide(raw, "Gini overflow"));
}

Q64 sybil_split_sensitivity(Q64 original_share, std::uint32_t identities) {
    require_unit(original_share, "original_share");
    if (identities == 0U) throw std::invalid_argument("equal_identity_count must be positive");
    if (original_share == Q64::zero() || identities == 1U) return Q64::zero();
    return Q64::one() - Q64::from_ratio(1, static_cast<std::int64_t>(identities));
}

DeviationRegretResult deviation_regret(Q64 truthful, std::span<const Q64> deviations, Q64 tolerance) {
    require_unit(truthful, "truthful_utility");
    require_unit(tolerance, "tolerance");
    if (deviations.empty()) throw std::invalid_argument("deviation_utilities must not be empty");
    if (deviations.size() > kMaxVector) throw std::invalid_argument("deviation_utilities too large");
    Q64 best = Q64::zero();
    for (Q64 value : deviations) {
        require_unit(value, "deviation_utility");
        best = Q64::max(best, value);
    }
    const Q64 regret = Q64::max(Q64::zero(), best - truthful);
    return {regret, best, regret <= tolerance};
}

CollusionExposure collusion_exposure(std::span<const Q64> shares, std::uint32_t max_colluders, Q64 threshold) {
    require_distribution(shares);
    require_unit(threshold, "capture_threshold");
    if (max_colluders == 0U) return {Q64::zero(), threshold == Q64::zero()};
    std::vector<Q64> sorted(shares.begin(), shares.end());
    std::sort(sorted.begin(), sorted.end(), [](Q64 lhs, Q64 rhs) { return lhs > rhs; });
    const std::size_t count = std::min<std::size_t>(static_cast<std::size_t>(max_colluders), sorted.size());
    Q64::wide_type raw = 0;
    for (std::size_t i = 0; i < count; ++i) raw += sorted[i].raw();
    const Q64 sum = q64_from_nonnegative_wide(raw, "collusion exposure overflow");
    return {sum, sum >= threshold};
}

Q64 wash_activity_suspicion(Q64 self_volume, Q64 reciprocal, Q64 concentration) {
    return weighted_unit({{self_volume, 40U}, {reciprocal, 35U}, {concentration, 25U}});
}

Q64 reward_leakage_ratio(Q64 nonproductive, Q64 total) {
    require_nonnegative(nonproductive, "nonproductive_reward");
    require_nonnegative(total, "total_reward");
    if (total == Q64::zero()) {
        if (nonproductive != Q64::zero()) throw std::invalid_argument("nonproductive reward cannot exist with zero total reward");
        return Q64::zero();
    }
    if (nonproductive > total) throw std::invalid_argument("nonproductive reward exceeds total reward");
    return Q64::clamp01(nonproductive / total);
}

RunwayResult subsidy_runway(Q64 treasury, Q64 inflow, Q64 outflow) {
    require_nonnegative(treasury, "treasury");
    require_nonnegative(inflow, "inflow_per_epoch");
    require_nonnegative(outflow, "outflow_per_epoch");
    const Q64 net_burn = Q64::max(Q64::zero(), outflow - inflow);
    if (net_burn == Q64::zero()) return {Q64::from_int(1'000'000'000), Q64::zero(), true};
    return {treasury / net_burn, net_burn, false};
}

SolvencyResult solvency_coverage(Q64 assets, Q64 liabilities, Q64 buffer) {
    require_nonnegative(assets, "liquid_assets");
    require_nonnegative(liabilities, "liabilities");
    require_unit(buffer, "required_buffer_ratio");
    if (liabilities == Q64::zero()) return {Q64::from_int(1'000'000'000), Q64::zero(), true};
    const Q64 required = liabilities * (Q64::one() + buffer);
    return {assets / liabilities, required, assets >= required};
}

ReserveResult dispute_reserve(Q64 exposure, Q64 probability, Q64 loss, Q64 margin) {
    require_nonnegative(exposure, "exposure");
    require_unit(probability, "dispute_probability");
    require_unit(loss, "loss_given_dispute");
    require_unit(margin, "uncertainty_margin");
    const Q64 base = Q64::clamp01(probability * loss);
    const Q64 ratio = Q64::clamp01(base + (Q64::one() - base) * margin);
    return {ratio, exposure * ratio};
}

SlippageResult settlement_slippage(Q64 expected, Q64 actual, Q64 allowed) {
    require_nonnegative(expected, "expected_value");
    require_nonnegative(actual, "actual_value");
    require_unit(allowed, "allowed_ratio");
    if (expected == Q64::zero()) {
        if (actual == Q64::zero()) return {Q64::zero(), true};
        return {Q64::one(), false};
    }
    const Q64 ratio = Q64::abs(actual - expected) / expected;
    return {ratio, ratio <= allowed};
}

FeeUpdateResult fee_hysteresis_update(Q64 current, Q64 target, Q64 deadband, Q64 max_step) {
    require_unit(current, "current_fee");
    require_unit(target, "target_fee");
    require_unit(deadband, "deadband");
    require_unit(max_step, "max_step");
    const Q64 delta = target - current;
    const Q64 magnitude = Q64::abs(delta);
    if (magnitude <= deadband) return {current, delta, false};
    const Q64 applied = Q64::min(magnitude, max_step);
    const Q64 next = Q64::clamp01(current + (delta > Q64::zero() ? applied : -applied));
    return {next, delta, next != current};
}

RevenueShockResult revenue_shock_guard(Q64 previous, Q64 current, Q64 max_drop, Q64 max_gain) {
    require_nonnegative(previous, "previous_revenue");
    require_nonnegative(current, "current_revenue");
    require_unit(max_drop, "max_drop_ratio");
    require_unit(max_gain, "max_gain_ratio");
    if (previous == Q64::zero()) {
        if (current == Q64::zero()) return {Q64::zero(), false, false};
        return {Q64::one(), false, max_gain < Q64::one()};
    }
    if (current < previous) {
        const Q64 change = (previous - current) / previous;
        return {change, true, change > max_drop};
    }
    const Q64 change = (current - previous) / previous;
    return {change, false, change > max_gain};
}

CrossAppExposureResult cross_app_exposure(Q64 principal, Q64 counterparty, Q64 irreversibility, Q64 breadth) {
    require_nonnegative(principal, "principal");
    const Q64 risk = weighted_unit({{counterparty, 50U}, {irreversibility, 30U}, {breadth, 20U}});
    return {risk, principal * risk};
}

ConservationResult rounding_conservation(std::span<const Q64> allocations, Q64 expected, Q64 tolerance) {
    require_nonnegative_span(allocations, "allocations");
    require_nonnegative(expected, "expected_total");
    require_nonnegative(tolerance, "tolerance");
    Q64::wide_type raw = 0;
    for (Q64 allocation : allocations) raw += allocation.raw();
    const Q64 sum = q64_from_nonnegative_wide(raw, "allocation sum overflow");
    const Q64 error = Q64::abs(sum - expected);
    return {error, error <= tolerance};
}

MintGateResult creator_value_mint_gate(Q64 inflow, Q64 outflow, Q64 authorized_mint, bool creator_mode) {
    require_nonnegative(inflow, "inflow");
    require_nonnegative(outflow, "outflow");
    require_nonnegative(authorized_mint, "authorized_mint");
    if (creator_mode) return {inflow, authorized_mint == Q64::zero() && outflow <= inflow};
    const Q64 maximum = inflow + authorized_mint;
    return {maximum, outflow <= maximum};
}

ExposureLimitResult experimental_exposure_limit(Q64 reserves, Q64 isolation, Q64 rollback, Q64 evidence, Q64 max_fraction) {
    require_nonnegative(reserves, "reserves");
    require_unit(isolation, "isolation_strength");
    require_unit(rollback, "rollback_strength");
    require_unit(evidence, "evidence_strength");
    require_unit(max_fraction, "max_reserve_fraction");
    const Q64 confidence = Q64::min(isolation, Q64::min(rollback, evidence));
    return {confidence, reserves * max_fraction * confidence};
}

} // namespace nexy::lo4
