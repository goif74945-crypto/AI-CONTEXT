from __future__ import annotations

import math

from .model import Direction, IntervalResult, MetricKind, MetricObservation, MetricSpec


_EPS = 1e-15


def normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def inverse_normal_cdf(p: float) -> float:
    """Acklam rational approximation for the inverse standard-normal CDF."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be strictly between 0 and 1")

    a = (-3.969683028665376e01, 2.209460984245205e02, -2.759285104469687e02,
         1.383577518672690e02, -3.066479806614716e01, 2.506628277459239e00)
    b = (-5.447609879822406e01, 1.615858368580409e02, -1.556989798598866e02,
         6.680131188771972e01, -1.328068155288572e01)
    c = (-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e00,
         -2.549732539343734e00, 4.374664141464968e00, 2.938163982698783e00)
    d = (7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00,
         3.754408661907416e00)

    plow = 0.02425
    phigh = 1.0 - plow

    if p < plow:
        q = math.sqrt(-2.0 * math.log(p))
        num = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
        den = ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
        return num / den

    if p <= phigh:
        q = p - 0.5
        r = q * q
        num = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q
        den = (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0)
        return num / den

    q = math.sqrt(-2.0 * math.log(1.0 - p))
    num = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
    den = ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
    return -(num / den)


def z_for_two_sided_alpha(alpha: float) -> float:
    return inverse_normal_cdf(1.0 - alpha / 2.0)


def sample_size_per_arm(spec: MetricSpec) -> int:
    z_alpha = z_for_two_sided_alpha(spec.alpha)
    z_power = inverse_normal_cdf(spec.power)
    delta = spec.mde_abs

    if spec.kind is MetricKind.PROPORTION:
        p1 = spec.baseline
        p2 = p1 + delta if spec.direction is Direction.HIGHER_IS_BETTER else p1 - delta
        p_bar = (p1 + p2) / 2.0
        term1 = z_alpha * math.sqrt(2.0 * p_bar * (1.0 - p_bar))
        term2 = z_power * math.sqrt(p1 * (1.0 - p1) + p2 * (1.0 - p2))
        return max(2, math.ceil(((term1 + term2) ** 2) / (delta ** 2)))

    if spec.kind is MetricKind.MEAN:
        if spec.planning_stddev is None:
            raise ValueError("planning_stddev required for mean metric")
        n = 2.0 * ((z_alpha + z_power) ** 2) * (spec.planning_stddev ** 2) / (delta ** 2)
        return max(2, math.ceil(n))

    raise ValueError(f"unsupported metric kind: {spec.kind}")


def _desired_effect(raw_effect: float, direction: Direction) -> float:
    return raw_effect if direction is Direction.HIGHER_IS_BETTER else -raw_effect


def observed_interval(spec: MetricSpec, obs: MetricObservation) -> IntervalResult:
    raw_effect = obs.treatment_value - obs.control_value

    if spec.kind is MetricKind.PROPORTION:
        p_c = obs.control_value
        p_t = obs.treatment_value
        se = math.sqrt(
            max(_EPS, p_c * (1.0 - p_c) / obs.control_n + p_t * (1.0 - p_t) / obs.treatment_n)
        )
        pooled = (p_c * obs.control_n + p_t * obs.treatment_n) / (obs.control_n + obs.treatment_n)
        pooled_se = math.sqrt(max(_EPS, pooled * (1.0 - pooled) * (1.0 / obs.control_n + 1.0 / obs.treatment_n)))
        z0 = raw_effect / pooled_se
    elif spec.kind is MetricKind.MEAN:
        if obs.control_stddev is None or obs.treatment_stddev is None:
            raise ValueError("observed stddevs required for mean metric")
        se = math.sqrt((obs.control_stddev ** 2) / obs.control_n + (obs.treatment_stddev ** 2) / obs.treatment_n)
        se = max(_EPS, se)
        z0 = raw_effect / se
    else:
        raise ValueError(f"unsupported metric kind: {spec.kind}")

    z = z_for_two_sided_alpha(spec.alpha)
    raw_lower = raw_effect - z * se
    raw_upper = raw_effect + z * se

    if spec.direction is Direction.HIGHER_IS_BETTER:
        desired_effect = raw_effect
        lower = raw_lower
        upper = raw_upper
    else:
        desired_effect = -raw_effect
        lower = -raw_upper
        upper = -raw_lower

    p_value = min(1.0, max(0.0, 2.0 * (1.0 - normal_cdf(abs(z0)))))
    return IntervalResult(
        effect_in_desired_direction=desired_effect,
        lower=lower,
        upper=upper,
        p_value_vs_zero=p_value,
    )
