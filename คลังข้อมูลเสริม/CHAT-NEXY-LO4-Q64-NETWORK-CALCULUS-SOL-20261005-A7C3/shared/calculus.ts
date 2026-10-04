import type { ArrivalContract, ServiceContract } from './contracts.js';
import { validateArrival, validateService } from './contracts.js';
import { addQ, divQCeil, mulQCeil } from './q64.js';

export interface Bounds {
  readonly backlogBoundQ: bigint;
  readonly delayBoundQ: bigint;
}

export function isStable(arrival: ArrivalContract, service: ServiceContract): boolean {
  validateArrival(arrival); validateService(service);
  return service.rateQ >= arrival.rateQ;
}

/** Upper backlog bound for alpha(t)=b+r*t and beta(t)=R*[t-T]+ when R>=r. */
export function backlogUpperQ(arrival: ArrivalContract, service: ServiceContract): bigint {
  validateArrival(arrival); validateService(service);
  if (!isStable(arrival, service)) throw new Error('FLOW_UNSTABLE');
  return addQ(arrival.burstQ, mulQCeil(arrival.rateQ, service.latencyQ));
}

/** Upper delay bound T + ceil(b/R) for the same token-bucket/rate-latency pair. */
export function delayUpperQ(arrival: ArrivalContract, service: ServiceContract): bigint {
  validateArrival(arrival); validateService(service);
  if (!isStable(arrival, service)) throw new Error('FLOW_UNSTABLE');
  return addQ(service.latencyQ, divQCeil(arrival.burstQ, service.rateQ));
}

export function allBounds(arrival: ArrivalContract, service: ServiceContract): Bounds {
  return { backlogBoundQ: backlogUpperQ(arrival, service), delayBoundQ: delayUpperQ(arrival, service) };
}
