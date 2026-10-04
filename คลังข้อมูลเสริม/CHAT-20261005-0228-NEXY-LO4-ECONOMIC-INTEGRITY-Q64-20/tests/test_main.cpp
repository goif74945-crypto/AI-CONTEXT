#include "nexy_lo4/concepts.hpp"

#include <algorithm>
#include <array>
#include <cstdint>
#include <exception>
#include <functional>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

using nexy::lo4::Q64;
using namespace nexy::lo4;

namespace {

int passed = 0;
int failed = 0;

[[nodiscard]] Q64 qi(std::int64_t x) { return Q64::from_int(x); }
[[nodiscard]] Q64 qr(std::int64_t n, std::int64_t d) { return Q64::from_ratio(n, d); }

void require(bool condition, std::string_view message) {
    if (!condition) throw std::runtime_error(std::string(message));
}

template <class F>
void expect_throw(F&& fn, std::string_view message) {
    bool threw = false;
    try { fn(); } catch (const std::exception&) { threw = true; }
    require(threw, message);
}

void run(std::string_view name, const std::function<void()>& fn) {
    try {
        fn();
        ++passed;
        std::cout << "PASS " << name << '\n';
    } catch (const std::exception& e) {
        ++failed;
        std::cout << "FAIL " << name << ": " << e.what() << '\n';
    } catch (...) {
        ++failed;
        std::cout << "FAIL " << name << ": unknown exception\n";
    }
}

} // namespace

int main() {
    run("q64 arithmetic and failure bounds", [] {
        require(qi(3) + qi(4) == qi(7), "addition");
        require(qi(7) - qi(4) == qi(3), "subtraction");
        require(qr(3, 2) * qi(2) == qi(3), "multiplication");
        require(qi(3) / qi(2) == qr(3, 2), "division");
        expect_throw([] { (void)(qi(1) / Q64::zero()); }, "division by zero must throw");
        expect_throw([] { (void)Q64::from_ratio(1, 0); }, "ratio denominator zero must throw");
    });

    run("registry contains exactly twenty proposal systems", [] {
        const auto registry = concept_registry();
        require(registry.size() == 20, "registry size != 20");
        for (std::size_t i = 0; i < registry.size(); ++i) {
            require(registry[i].id == i + 1, "registry ids must be sequential");
            require(!registry[i].key.empty(), "registry key empty");
            require(!registry[i].name.empty(), "registry name empty");
        }
    });

    run("01 budget balance gates overspend", [] {
        const auto ok = budget_balance(qi(100), Q64::zero(), qi(90), qi(5), Q64::zero());
        require(ok.funding == qi(100) && ok.outflow == qi(95), "balance totals");
        require(ok.deficit == Q64::zero() && ok.balanced, "valid budget rejected");
        const auto bad = budget_balance(qi(100), Q64::zero(), qi(101), qi(0), Q64::zero());
        require(bad.deficit == qi(1) && !bad.balanced, "overspend must fail");
    });

    run("02 revenue split conserves exact Q64 total", [] {
        const std::array weights{qi(1), qi(1), qi(1)};
        const auto r = allocate_revenue(qi(100), weights);
        require(r.allocations.size() == 3, "allocation count");
        Q64 sum = Q64::zero();
        for (Q64 x : r.allocations) sum += x;
        require(sum == qi(100), "Q64 allocation mass not conserved");
        require(r.residual == Q64::zero(), "residual must be zero after deterministic distribution");
        require(r.allocations[0] >= r.allocations[1] && r.allocations[1] == r.allocations[2], "deterministic tie residual");
    });

    run("03 minor-unit allocator conserves integer currency units", [] {
        const std::array weights{qi(1), qi(1), qi(1)};
        const auto r = apportion_minor_units(100, weights);
        require((r == std::vector<std::uint64_t>{34, 33, 33}), "Hamilton-style deterministic remainder expected");
        require(std::accumulate(r.begin(), r.end(), std::uint64_t{0}) == 100, "minor units not conserved");
    });

    run("04 HHI concentration is exact for equal duopoly", [] {
        const std::array shares{qr(1, 2), qr(1, 2)};
        require(concentration_hhi(shares) == qr(1, 2), "HHI for 50/50 must equal 1/2");
        const std::array invalid{qr(1, 2), qr(1, 4)};
        expect_throw([&] { (void)concentration_hhi(invalid); }, "non-normalized shares must fail");
    });

    run("05 Gini meter matches two-point distribution", [] {
        const std::array values{Q64::zero(), qi(2)};
        require(gini_index(values) == qr(1, 2), "Gini([0,2]) must equal 1/2");
    });

    run("06 Sybil split sensitivity grows with identities", [] {
        require(sybil_split_sensitivity(qr(1, 2), 1) == Q64::zero(), "one identity should have zero split sensitivity");
        require(sybil_split_sensitivity(qr(1, 2), 4) == qr(3, 4), "four-way split sensitivity must be 3/4");
        expect_throw([] { (void)sybil_split_sensitivity(qr(1, 2), 0); }, "zero identity count must fail");
    });

    run("07 deviation regret detects profitable manipulation", [] {
        const std::array deviations{qr(1, 2), qr(3, 4)};
        const auto r = deviation_regret(qr(1, 2), deviations, qr(1, 8));
        require(r.best_deviation == qr(3, 4), "best deviation");
        require(r.regret == qr(1, 4), "regret");
        require(!r.incentive_compatible, "profitable deviation must fail tolerance");
    });

    run("08 collusion exposure sums largest k shares", [] {
        const std::array shares{qr(1, 2), qr(1, 4), qr(1, 4)};
        const auto r = collusion_exposure(shares, 2, qr(3, 4));
        require(r.top_k_share == qr(3, 4) && r.threshold_reached, "top-2 capture must be 3/4");
    });

    run("09 wash activity suspicion saturates at one", [] {
        require(wash_activity_suspicion(Q64::one(), Q64::one(), Q64::one()) == Q64::one(), "all-max signals should score one");
        expect_throw([] { (void)wash_activity_suspicion(qi(2), Q64::zero(), Q64::zero()); }, "out-of-unit signal must fail");
    });

    run("10 reward leakage ratio is bounded and validated", [] {
        require(reward_leakage_ratio(qi(1), qi(4)) == qr(1, 4), "leakage 1/4");
        expect_throw([] { (void)reward_leakage_ratio(qi(2), qi(1)); }, "leakage cannot exceed total reward");
    });

    run("11 subsidy runway handles burn and self-sustaining mode", [] {
        const auto burn = subsidy_runway(qi(100), qi(10), qi(20));
        require(!burn.self_sustaining && burn.net_burn == qi(10) && burn.epochs == qi(10), "runway burn case");
        const auto self = subsidy_runway(qi(5), qi(2), qi(2));
        require(self.self_sustaining && self.net_burn == Q64::zero(), "self sustaining");
    });

    run("12 solvency coverage enforces buffer", [] {
        const auto ok = solvency_coverage(qi(5), qi(4), qr(1, 4));
        require(ok.coverage_ratio == qr(5, 4), "coverage ratio");
        require(ok.required_assets == qi(5) && ok.solvent, "buffered solvency");
        const auto bad = solvency_coverage(qi(4), qi(4), qr(1, 4));
        require(!bad.solvent, "underbuffered assets must fail");
    });

    run("13 dispute reserve sizes base loss plus uncertainty", [] {
        const auto r = dispute_reserve(qi(100), qr(1, 2), qr(1, 2), qr(1, 2));
        require(r.reserve_ratio == qr(5, 8), "reserve ratio expected 5/8");
        require(r.required_reserve == qr(125, 2), "reserve amount expected 62.5");
    });

    run("14 settlement slippage has explicit envelope", [] {
        const auto ok = settlement_slippage(qi(8), qi(9), qr(1, 8));
        require(ok.deviation_ratio == qr(1, 8) && ok.within_limit, "boundary slippage should pass");
        const auto bad = settlement_slippage(qi(8), qi(10), qr(1, 8));
        require(bad.deviation_ratio == qr(1, 4) && !bad.within_limit, "excess slippage should fail");
    });

    run("15 fee hysteresis bounds update step", [] {
        const auto r = fee_hysteresis_update(qr(1, 2), qr(3, 4), qr(1, 16), qr(1, 8));
        require(r.changed && r.requested_delta == qr(1, 4), "fee change requested");
        require(r.next_fee == qr(5, 8), "fee step must be capped at 1/8");
        const auto held = fee_hysteresis_update(qr(1, 2), qr(17, 32), qr(1, 16), qr(1, 8));
        require(!held.changed && held.next_fee == qr(1, 2), "deadband must suppress churn");
    });

    run("16 creator revenue shock guard detects drop", [] {
        const auto r = revenue_shock_guard(qi(100), qi(75), qr(1, 8), qr(1, 4));
        require(r.downward && r.relative_change == qr(1, 4) && r.shock, "25 percent drop must trigger 1/8 limit");
    });

    run("17 cross-app exposure reaches principal at maximal risks", [] {
        const auto r = cross_app_exposure(qi(100), Q64::one(), Q64::one(), Q64::one());
        require(r.risk_ratio == Q64::one() && r.risk_amount == qi(100), "max risk exposure");
    });

    run("18 rounding conservation catches lost mass", [] {
        const std::array exact{qr(1, 2), qr(1, 4), qr(1, 4)};
        const auto ok = rounding_conservation(exact, Q64::one(), Q64::zero());
        require(ok.absolute_error == Q64::zero() && ok.conserved, "exact conservation");
        const std::array shortfall{qr(1, 2), qr(1, 4)};
        const auto bad = rounding_conservation(shortfall, Q64::one(), Q64::zero());
        require(bad.absolute_error == qr(1, 4) && !bad.conserved, "lost mass must fail");
    });

    run("19 creator no-mint gate blocks value creation", [] {
        const auto ok = creator_value_mint_gate(qi(10), qi(10), Q64::zero(), true);
        require(ok.maximum_legal_outflow == qi(10) && ok.allowed, "creator conserved value");
        const auto bad = creator_value_mint_gate(qi(10), qi(10), qi(1), true);
        require(!bad.allowed, "creator mode cannot use mint authority");
        const auto sovereign = creator_value_mint_gate(qi(10), qi(11), qi(1), false);
        require(sovereign.allowed && sovereign.maximum_legal_outflow == qi(11), "noncreator authorized mint path");
    });

    run("20 experimental exposure limit uses weakest confidence factor", [] {
        const auto r = experimental_exposure_limit(qi(100), Q64::one(), qr(1, 2), qr(3, 4), qr(1, 8));
        require(r.confidence_factor == qr(1, 2), "minimum confidence factor");
        require(r.maximum_exposure == qr(25, 4), "100 * 1/8 * 1/2 = 6.25");
    });

    run("negative values and empty weights fail closed", [] {
        const std::array<Q64, 0> empty{};
        expect_throw([&] { (void)allocate_revenue(qi(1), empty); }, "empty weights must fail");
        expect_throw([] { (void)budget_balance(qi(-1), Q64::zero(), Q64::zero(), Q64::zero(), Q64::zero()); }, "negative inflow must fail");
        const std::array bad_weights{qi(1), qi(-1)};
        expect_throw([&] { (void)apportion_minor_units(10, bad_weights); }, "negative weight must fail");
    });

    std::cout << "SUMMARY passed=" << passed << " failed=" << failed << "\n";
    return failed == 0 ? 0 : 1;
}
