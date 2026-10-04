#include "nexy_cfpc/cfpc.hpp"
#include "nexy_cfpc/sha256.hpp"

#include <algorithm>
#include <cstdint>
#include <exception>
#include <functional>
#include <iostream>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

using namespace nexy::cfpc;

namespace {
int passed = 0;
int failed = 0;

void check(bool cond, const std::string& name) {
  if (cond) { ++passed; return; }
  ++failed;
  std::cerr << "FAIL: " << name << '\n';
}

template <typename E, typename F>
void expect_throw(F&& f, const std::string& name) {
  try { f(); check(false, name); }
  catch (const E&) { check(true, name); }
  catch (...) { check(false, name + "_WRONG_EXCEPTION"); }
}

BoundExpression linear(const std::string& dim, std::int64_t coefficient, std::int64_t c = 0) {
  BoundExpression e{{{Q64::from_integer(coefficient), {{dim, 1U}}}}};
  if (c != 0) e.terms.push_back({Q64::from_integer(c), {}});
  return e;
}
BoundExpression quadratic(const std::string& dim, std::int64_t coefficient) {
  return {{{Q64::from_integer(coefficient), {{dim, 2U}}}}};
}

std::vector<ResourceKind> all_kinds() {
  return {
    ResourceKind::CpuWork, ResourceKind::PeakMemory, ResourceKind::DurableState,
    ResourceKind::EvidenceBytes, ResourceKind::Fanout, ResourceKind::RetryWork,
    ResourceKind::QueuePressure, ResourceKind::SerializationBytes,
    ResourceKind::ExternalCalls, ResourceKind::VerifierWork
  };
}

ProposalBoundSpec valid_spec(std::uint64_t budget = 100000U) {
  ProposalBoundSpec spec;
  spec.proposal_id = "proposal.cfpc.valid";
  spec.spec_hash = std::string(64, 'a');
  spec.code_hash = std::string(64, 'b');
  spec.assumptions = {"input bounded", "no hidden retries"};
  spec.required_verification_steps = {"static", "unit", "integration"};
  spec.provided_verification_steps = spec.required_verification_steps;
  for (const auto kind : all_kinds()) {
    BoundExpression expr = kind == ResourceKind::CpuWork ? quadratic("n", 1) : linear("n", 2, 1);
    spec.resources.push_back({kind, expr, Q64::from_integer(static_cast<std::int64_t>(budget))});
  }
  return spec;
}

void q64_tests() {
  check(Q64::from_integer(2).to_decimal(3) == "2.000", "q64 integer roundtrip");
  check(Q64::parse_decimal("1.5").to_decimal(3) == "1.500", "q64 decimal parse");
  check(Q64::parse_decimal("-1.25").to_decimal(2) == "-1.25", "q64 negative decimal");
  check(Q64::from_ratio(1, 2) == Q64::parse_decimal("0.5"), "q64 ratio");
  check(Q64::parse_decimal("1.5").checked_mul(Q64::from_integer(2)) == Q64::from_integer(3), "q64 multiply");
  check(Q64::from_integer(3).checked_div(Q64::from_integer(2)) == Q64::parse_decimal("1.5"), "q64 divide");
  expect_throw<std::domain_error>([] { (void)Q64::from_integer(1).checked_div(Q64::from_integer(0)); }, "q64 div zero");
  expect_throw<std::invalid_argument>([] { (void)Q64::parse_decimal("1.1234567890123456789"); }, "q64 precision reject");
  expect_throw<std::overflow_error>([] { (void)Q64::from_raw(i128_max_value()).checked_add(Q64::from_raw(1)); }, "q64 add overflow");
  expect_throw<std::overflow_error>([] { (void)Q64::from_raw(i128_min_value()).checked_sub(Q64::from_raw(1)); }, "q64 sub overflow");
  expect_throw<std::overflow_error>([] { (void)Q64::from_raw(i128_max_value()).checked_mul_integer(2); }, "q64 int mul overflow");
}

void expression_tests() {
  Workload w{{{"n", 10U}, {"m", 3U}}};
  check(validate_workload(w).passed, "workload valid");
  check(!validate_workload(Workload{}).passed, "workload empty reject");
  Workload huge{{{"n", 1'000'000'001ULL}}};
  check(!validate_workload(huge).passed, "workload upper limit");

  const auto e = linear("n", 2, 3);
  check(validate_expression(e).passed, "expression valid");
  check(validate_coefficients(e).passed, "coefficients valid");
  check(monotonicity_witness(e).passed, "monotonicity valid");
  check(bind_input_vector(w, e).passed, "binding valid");
  check(evaluate_bound(e, w) == Q64::from_integer(23), "linear evaluate");
  check(evaluate_bound(quadratic("n", 2), w) == Q64::from_integer(200), "quadratic evaluate");

  BoundExpression missing = linear("x", 1);
  check(!bind_input_vector(w, missing).passed, "unbound dimension reject");
  BoundExpression negative{{{Q64::from_integer(-1), {{"n", 1U}}}}};
  check(!validate_coefficients(negative).passed, "negative coefficient reject");
  check(!monotonicity_witness(negative).passed, "negative monotonicity reject");
  BoundExpression expbad{{{Q64::from_integer(1), {{"n", 9U}}}}};
  check(!validate_expression(expbad).passed, "exponent cap reject");

  const auto composed = add_bounds(linear("n", 1), linear("n", 2));
  check(evaluate_bound(composed, w) == Q64::from_integer(30), "bound composition");

  BoundExpression huge_power{{{Q64::from_integer(1), {{"n", 8U}}}}};
  Workload max_input{{{"n", 1'000'000'000ULL}}};
  expect_throw<std::overflow_error>([&] { (void)evaluate_bound(huge_power, max_input); }, "dimension power overflow fail closed");
}

void mechanism_tests() {
  auto spec = valid_spec();
  check(verification_preservation(spec).passed, "verification preservation pass");
  spec.provided_verification_steps.erase("integration");
  check(!verification_preservation(spec).passed, "verification preservation fail");
  spec = valid_spec();
  check(degradation_contract_gate(spec.degradation).passed, "degradation pass");
  spec.degradation.silently_skips_verification = true;
  check(!degradation_contract_gate(spec.degradation).passed, "degradation unsafe reject");
  check(authority_non_interference(false,false,false).passed, "authority advisory pass");
  check(!authority_non_interference(true,false,false).passed, "canon mutation reject");
  check(!authority_non_interference(false,true,false).passed, "core mutation reject");
  check(!authority_non_interference(false,false,true).passed, "auto promotion reject");
  check(budget_dominance(ResourceKind::CpuWork, Q64::from_integer(10), Q64::from_integer(10)).passed, "budget equality pass");
  check(!budget_dominance(ResourceKind::CpuWork, Q64::from_integer(11), Q64::from_integer(10)).passed, "budget exceed reject");
}

void certificate_tests() {
  const Workload w{{{"n", 100U}}};
  const auto good = evaluate_proposal(valid_spec(), w);
  check(good.verdict == Verdict::Pass, "certificate pass");
  check(good.observed_bounds.size() == 10U, "all resource bounds observed");
  check(good.certificate_sha256.size() == 64U, "certificate hash length");
  check(good.certificate_sha256 == sha256_hex(good.canonical_record), "certificate hash binds record");

  auto budget_fail = valid_spec();
  for (auto& claim : budget_fail.resources) if (claim.kind == ResourceKind::CpuWork) claim.budget = Q64::from_integer(9999);
  check(evaluate_proposal(budget_fail, w).verdict == Verdict::Freeze, "cpu budget fail closed");

  auto missing_resource = valid_spec();
  missing_resource.resources.pop_back();
  check(evaluate_proposal(missing_resource, w).verdict == Verdict::Freeze, "missing resource claim freeze");

  auto duplicate_resource = valid_spec();
  duplicate_resource.resources.push_back(duplicate_resource.resources.front());
  check(evaluate_proposal(duplicate_resource, w).verdict == Verdict::Freeze, "duplicate resource claim freeze");

  auto missing_verification = valid_spec();
  missing_verification.provided_verification_steps.erase("unit");
  check(evaluate_proposal(missing_verification, w).verdict == Verdict::Freeze, "missing verification freeze");

  auto unsafe_deg = valid_spec();
  unsafe_deg.degradation.silently_drops_evidence = true;
  check(evaluate_proposal(unsafe_deg, w).verdict == Verdict::Freeze, "silent evidence drop freeze");

  auto bad_hash = valid_spec();
  bad_hash.spec_hash = "abc";
  check(evaluate_proposal(bad_hash, w).verdict == Verdict::Freeze, "bad identity hash freeze");

  check(evaluate_proposal(valid_spec(), w, true, false, false).verdict == Verdict::Freeze, "canon escalation freeze");
  check(evaluate_proposal(valid_spec(), w, false, true, false).verdict == Verdict::Freeze, "core escalation freeze");
  check(evaluate_proposal(valid_spec(), w, false, false, true).verdict == Verdict::Freeze, "promotion escalation freeze");
}

void determinism_tests() {
  const Workload w1{{{"m", 3U}, {"n", 100U}}};
  const Workload w2{{{"n", 100U}, {"m", 3U}}};
  auto a = valid_spec();
  auto b = valid_spec();
  const auto r1 = evaluate_proposal(a, w1);
  const auto r2 = evaluate_proposal(b, w2);
  check(r1.canonical_record == r2.canonical_record, "map insertion order independent");
  check(r1.certificate_sha256 == r2.certificate_sha256, "certificate deterministic");

  auto shuffled = valid_spec();
  std::reverse(shuffled.resources.begin(), shuffled.resources.end());
  for (auto& claim : shuffled.resources) std::reverse(claim.upper_bound.terms.begin(), claim.upper_bound.terms.end());
  const auto rs = evaluate_proposal(shuffled, w1);
  check(rs.canonical_record == r1.canonical_record, "resource and monomial order canonicalized");

  auto budget_variant = valid_spec();
  budget_variant.resources.front().budget = Q64::from_integer(100001);
  const auto rb = evaluate_proposal(budget_variant, w1);
  check(rb.verdict == Verdict::Pass && rb.certificate_sha256 != r1.certificate_sha256, "certificate binds budget policy");

  auto assumption_variant = valid_spec();
  assumption_variant.assumptions.push_back("different assumption");
  const auto ra = evaluate_proposal(assumption_variant, w1);
  check(ra.verdict == Verdict::Pass && ra.certificate_sha256 != r1.certificate_sha256, "certificate binds assumptions");

  auto verification_variant = valid_spec();
  verification_variant.provided_verification_steps.insert("extra_check");
  const auto rv = evaluate_proposal(verification_variant, w1);
  check(rv.verdict == Verdict::Pass && rv.certificate_sha256 != r1.certificate_sha256, "certificate binds verification set");

  for (int i=0;i<1000;++i) {
    const auto rx = evaluate_proposal(valid_spec(), w1);
    if (rx.certificate_sha256 != r1.certificate_sha256) { check(false, "1000 replay deterministic"); return; }
  }
  check(true, "1000 replay deterministic");
}

void property_tests() {
  std::mt19937_64 rng(0xC0FFEEULL);
  for (int i=0;i<25000;++i) {
    const std::uint64_t n = 1U + (rng() % 10000U);
    const std::int64_t c = static_cast<std::int64_t>(1U + (rng() % 10U));
    const std::int64_t k = static_cast<std::int64_t>(rng() % 100U);
    const Workload w{{{"n", n}}};
    const auto e = linear("n", c, k);
    const Q64 value = evaluate_bound(e, w);
    const i128 expected = i128(c) * i128(n) + i128(k);
    if (value != Q64::from_ratio(expected, 1)) { check(false, "25000 linear property"); return; }
  }
  check(true, "25000 linear property");

  for (std::uint64_t n=0;n<5000U;++n) {
    Workload a{{{"n", n}}};
    Workload b{{{"n", n+1U}}};
    const auto e = quadratic("n", 3);
    if (evaluate_bound(e, a) > evaluate_bound(e, b)) { check(false, "5000 monotonic property"); return; }
  }
  check(true, "5000 monotonic property");
}

void sha_tests() {
  check(sha256_hex("") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "sha empty vector");
  check(sha256_hex("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad", "sha abc vector");
}
}

int main() {
  q64_tests();
  expression_tests();
  mechanism_tests();
  certificate_tests();
  determinism_tests();
  property_tests();
  sha_tests();
  std::cout << "PASS=" << passed << " FAIL=" << failed << '\n';
  return failed == 0 ? 0 : 1;
}
