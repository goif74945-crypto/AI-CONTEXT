#include "nexy_cfpc/cfpc.hpp"
#include <iostream>

using namespace nexy::cfpc;

static BoundExpression linear(const std::string& dim, std::int64_t coefficient, std::int64_t constant = 0) {
  BoundExpression e;
  e.terms.push_back({Q64::from_integer(coefficient), {{dim, 1U}}});
  if (constant > 0) e.terms.push_back({Q64::from_integer(constant), {}});
  return e;
}

int main() {
  ProposalBoundSpec spec;
  spec.proposal_id = "cfpc.integration.demo";
  spec.spec_hash = std::string(64, 'a');
  spec.code_hash = std::string(64, 'b');
  spec.required_verification_steps = {"static", "unit", "integration"};
  spec.provided_verification_steps = spec.required_verification_steps;

  const std::vector<ResourceKind> kinds = {
    ResourceKind::CpuWork, ResourceKind::PeakMemory, ResourceKind::DurableState,
    ResourceKind::EvidenceBytes, ResourceKind::Fanout, ResourceKind::RetryWork,
    ResourceKind::QueuePressure, ResourceKind::SerializationBytes,
    ResourceKind::ExternalCalls, ResourceKind::VerifierWork
  };
  for (const auto kind : kinds) {
    spec.resources.push_back({kind, linear("n", 2, 1), Q64::from_integer(1001)});
  }

  const auto result = evaluate_proposal(spec, Workload{{{"n", 500U}}});
  std::cout << result.canonical_record << "\n" << result.certificate_sha256 << "\n";
  return result.verdict == Verdict::Pass ? 0 : 2;
}
