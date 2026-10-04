# Mathematical Source Grounding

This lab uses standard deterministic network-calculus results as mathematical background, not as NEXY authority.

## External references consulted
- Jean-Yves Le Boudec and Patrick Thiran, *Network Calculus: A Theory of Deterministic Queuing Systems for the Internet*, free book portal: https://leboudec.github.io/netcal/
- Jean-Yves Le Boudec, network-calculus tutorial material: https://leboudec.github.io/leboudec/resources/tutorial-nc-dagstuhl-EPFL-2019-LEB.pdf
- Short-course composition material: https://leboudec.github.io/netcal/resources/NetCalAv31.pdf

The tutorial material states the token/leaky-bucket arrival form and rate-latency service model and gives aggregate backlog/delay bounds equivalent to `B=b+rT` and `D=T+b/R` under the stated service assumptions. The short-course material gives the service-curve concatenation theorem via min-plus convolution.

## Deliberate model restriction
The prototype implements a fluid rate-latency abstraction only. It does not silently extend those equations to packetized GR nodes, stochastic queues, arbitrary schedulers or unknown cross traffic. Those require additional terms/models and fresh authority.
