# VBR — Vector Budget Reactor

## Objective
Stop incomparable risk/resources from being laundered through a single aggregate score. Privacy headroom cannot compensate for exhausted irreversibility headroom merely because an average still looks acceptable.

## State
- `caps[dimension]` — maximum allowed amount;
- `used[dimension]` — committed consumption;
- `reservations[id][dimension]` — pending consumption.

## Transitions
`reserve -> commit` spends capacity. `reserve -> release` returns pending capacity without spending it.

A reservation is admitted only if, independently for every requested dimension:
`used + all_reserved + requested <= cap`.

## Failure semantics
Unknown dimension, duplicate reservation ID, unknown commit/release ID, or dimension cap violation freezes that transition. Dimensions never borrow from each other.

## Production note
The reference implementation proves deterministic state-transition semantics only. Production concurrency needs transactional storage or compare-and-swap with reservation versioning and idempotency keys.
