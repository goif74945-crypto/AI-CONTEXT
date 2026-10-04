# Counterfactual Release Review
Ask what plausible hidden condition would make confidence wrong: stale upstream returning 200, repeated action after timeout, identifier format change, reversed ordering, absent optional fields, racing writes, cache surviving migration, tool success without durable mutation, too-narrow requirement interpretation, rollback failure.

For each critical subsystem list strongest evidence, construct a world where evidence exists but behavior is wrong, find a discriminating test, add the cheapest discriminator, and record residual risk if none exists.