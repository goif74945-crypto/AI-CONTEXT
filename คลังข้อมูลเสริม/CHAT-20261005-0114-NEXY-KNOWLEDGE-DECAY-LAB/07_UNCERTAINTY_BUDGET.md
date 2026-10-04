# Uncertainty Budget
**AI-PROPOSED CONCEPT — NOT AUTHORITATIVE — NOT IMPLEMENTED — NOT VERIFIED**

## Problem
Individual UNKNOWN labels do not express cumulative uncertainty. Many small unknowns can make a high-impact decision unsafe.

## Categories
U-A Authority; U-I Identity; U-S State; U-D Dependency; U-E Evidence; U-R Runtime/environment; U-X External/provider; U-T Temporal/freshness.

## Control model
Impact/radius determines the maximum permitted uncertainty envelope. Discovery reduces uncertainty; assumptions consume budget; verified evidence retires uncertainty. Some categories are non-compensable: unresolved authority or target identity can force FREEZE regardless of other evidence.

## No fake arithmetic
Never sum arbitrary confidence percentages. This is categorical control logic, not pseudo-mathematical certainty.

## Example gates
Reversible research may proceed with some dependency UNKNOWNs if labeled.
Production mutation cannot proceed with unresolved authority/identity.
Release cannot use stale revision-bound evidence to retire evidence uncertainty.
Irreversible migration requires explicit recovery evidence.

## Decision packet
knowns; unknowns; assumptions; conflicts; retired uncertainties; non-compensable blockers; highest-value next evidence.

## Benefit
Makes “what remains unknown?” operational and aligns with freeze-over-guess.
