#include "nexy_lo4/concepts.hpp"

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <random>
#include <stdexcept>
#include <vector>

using nexy::lo4::Q64;
using namespace nexy::lo4;

namespace {

[[nodiscard]] Q64 qraw(Q64::storage_type raw) { return Q64::from_raw(raw); }
[[nodiscard]] Q64 qi(std::int64_t x) { return Q64::from_int(x); }

void check(bool value, const char* message) {
    if (!value) throw std::runtime_error(message);
}

[[nodiscard]] std::array<Q64, 3> random_distribution(std::mt19937_64& rng) {
    const std::uint64_t a = rng();
    const std::uint64_t b = rng();
    const std::uint64_t lo = std::min(a, b);
    const std::uint64_t hi = std::max(a, b);
    const Q64::storage_type scale = Q64::one().raw();
    return {qraw(static_cast<Q64::storage_type>(lo)),
            qraw(static_cast<Q64::storage_type>(hi - lo)),
            qraw(scale - static_cast<Q64::storage_type>(hi))};
}

} // namespace

int main() {
    constexpr std::uint64_t iterations = 100'000;
    std::mt19937_64 rng(0x74945C0FFEEULL);

    try {
        for (std::uint64_t i = 0; i < iterations; ++i) {
            const auto shares = random_distribution(rng);
            check(shares[0] + shares[1] + shares[2] == Q64::one(), "distribution mass");

            const Q64 total = qi(static_cast<std::int64_t>(1 + (rng() % 1'000'000)));
            const auto split = allocate_revenue(total, shares);
            Q64 split_sum = Q64::zero();
            for (Q64 x : split.allocations) split_sum += x;
            check(split_sum == total, "revenue split conservation");
            check(split.residual == Q64::zero(), "revenue residual");

            const std::uint64_t units = rng() % 1'000'000;
            const auto minor = apportion_minor_units(units, shares);
            std::uint64_t unit_sum = 0;
            for (std::uint64_t x : minor) unit_sum += x;
            check(unit_sum == units, "minor-unit conservation");

            const Q64 hhi = concentration_hhi(shares);
            check(hhi >= Q64::from_ratio(1, 3) - Q64::from_raw(2) && hhi <= Q64::one(), "HHI range");

            const std::array values{shares[0] * total, shares[1] * total, shares[2] * total};
            const Q64 gini = gini_index(values);
            check(gini >= Q64::zero() && gini <= Q64::one(), "gini range");

            const std::uint32_t identities = 1U + static_cast<std::uint32_t>(rng() % 128U);
            const Q64 sybil = sybil_split_sensitivity(shares[0], identities);
            check(sybil >= Q64::zero() && sybil <= Q64::one(), "sybil range");

            const std::array deviations{shares[0], shares[1], shares[2]};
            const auto regret = deviation_regret(shares[0], deviations, shares[2]);
            check(regret.regret >= Q64::zero() && regret.regret <= Q64::one(), "regret range");

            const auto collusion = collusion_exposure(shares, 2, Q64::from_ratio(2, 3));
            check(collusion.top_k_share >= Q64::zero() && collusion.top_k_share <= Q64::one(), "collusion range");

            const Q64 wash = wash_activity_suspicion(shares[0], shares[1], shares[2]);
            check(wash >= Q64::zero() && wash <= Q64::one(), "wash range");

            const Q64 productive = Q64::min(shares[0], shares[1]);
            const Q64 leakage = reward_leakage_ratio(productive, Q64::one());
            check(leakage == productive, "leakage identity for denominator one");

            const Q64 current_fee = shares[0];
            const Q64 target_fee = shares[1];
            const Q64 max_step = Q64::from_ratio(1, 16);
            const auto fee = fee_hysteresis_update(current_fee, target_fee, Q64::zero(), max_step);
            check(Q64::abs(fee.next_fee - current_fee) <= max_step, "fee max step");

            const auto exposure = cross_app_exposure(total, shares[0], shares[1], shares[2]);
            check(exposure.risk_ratio >= Q64::zero() && exposure.risk_ratio <= Q64::one(), "risk ratio range");
            check(exposure.risk_amount >= Q64::zero() && exposure.risk_amount <= total, "risk amount range");

            const auto conservation = rounding_conservation(shares, Q64::one(), Q64::zero());
            check(conservation.conserved, "normalized shares conservation");

            const auto creator_ok = creator_value_mint_gate(total, total, Q64::zero(), true);
            const auto creator_bad = creator_value_mint_gate(total, total, qi(1), true);
            check(creator_ok.allowed && !creator_bad.allowed, "creator no-mint invariant");

            const auto limit = experimental_exposure_limit(total, shares[0], shares[1], shares[2], Q64::from_ratio(1, 8));
            check(limit.maximum_exposure >= Q64::zero(), "exposure nonnegative");
            check(limit.maximum_exposure <= total * Q64::from_ratio(1, 8), "exposure cap");

            const Q64 inflow = total;
            const Q64 payouts = total - Q64::from_raw(static_cast<Q64::storage_type>(rng() % 1024U));
            const auto budget = budget_balance(inflow, Q64::zero(), payouts, Q64::zero(), Q64::zero());
            check(budget.balanced, "non-overspend budget");
        }
    } catch (const std::exception& e) {
        std::cerr << "PROPERTY_FAIL: " << e.what() << '\n';
        return 1;
    }

    std::cout << "PROPERTY_PASS iterations=" << iterations << " seed=0x74945C0FFEE\n";
    return 0;
}
