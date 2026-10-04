#include "nexy_lo4/concepts.hpp"

#include <array>
#include <iostream>

using namespace nexy::lo4;

int main() {
    const std::array weights{Q64::from_int(5), Q64::from_int(3), Q64::from_int(2)};
    const auto revenue = allocate_revenue(Q64::from_int(1'000), weights);
    const auto mint_gate = creator_value_mint_gate(Q64::from_int(1'000), Q64::from_int(1'000), Q64::zero(), true);
    const auto exposure = experimental_exposure_limit(Q64::from_int(10'000), Q64::one(), Q64::from_ratio(3,4), Q64::from_ratio(7,8), Q64::from_ratio(1,16));

    Q64 sum = Q64::zero();
    for (Q64 value : revenue.allocations) sum += value;

    std::cout << "concepts=" << concept_registry().size() << '\n';
    std::cout << "revenue_conserved=" << (sum == Q64::from_int(1'000) ? "true" : "false") << '\n';
    std::cout << "creator_no_mint=" << (mint_gate.allowed ? "true" : "false") << '\n';
    std::cout << "experimental_max_exposure=" << exposure.maximum_exposure.decimal(6) << '\n';
    std::cout << "authority=LO4_AI_PROPOSAL_ONLY\n";
    std::cout << "canon_authority=NONE\n";
    return 0;
}
