import { requireNonNegative, requirePositive } from './q64.js';

export interface ArrivalContract {
  readonly burstQ: bigint; // work units
  readonly rateQ: bigint;  // work units / time unit
}

export interface ServiceContract {
  readonly rateQ: bigint;    // work units / time unit
  readonly latencyQ: bigint; // time units
}

export interface NamedServiceContract extends ServiceContract {
  readonly id: string;
}

export function validateArrival(input: ArrivalContract): ArrivalContract {
  requireNonNegative(input.burstQ, 'ARRIVAL_BURST_NEGATIVE');
  requireNonNegative(input.rateQ, 'ARRIVAL_RATE_NEGATIVE');
  return input;
}

export function validateService(input: ServiceContract): ServiceContract {
  requirePositive(input.rateQ, 'SERVICE_RATE_NON_POSITIVE');
  requireNonNegative(input.latencyQ, 'SERVICE_LATENCY_NEGATIVE');
  return input;
}

export function validateNamedService(input: NamedServiceContract): NamedServiceContract {
  if (input.id.trim().length === 0) throw new Error('SERVICE_ID_REQUIRED');
  validateService(input);
  return input;
}
