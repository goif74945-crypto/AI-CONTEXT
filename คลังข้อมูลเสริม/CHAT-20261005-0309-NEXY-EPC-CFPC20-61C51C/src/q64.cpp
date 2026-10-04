#include "nexy_cfpc/q64.hpp"

#include <algorithm>
#include <cctype>
#include <limits>

namespace nexy::cfpc {
namespace {
const i128 SCALE = i128(1) << Q64::FRACTION_BITS;
const i128 I128_MIN = -(i128(1) << 127);
const i128 I128_MAX = (i128(1) << 127) - 1;

[[nodiscard]] i128 pow10(std::uint32_t exp) {
  i128 out = 1;
  for (std::uint32_t i = 0; i < exp; ++i) {
    if (out > I128_MAX / 10) throw std::overflow_error("Q64_DECIMAL_POWER_OVERFLOW");
    out *= 10;
  }
  return out;
}

[[nodiscard]] bool digits_only(std::string_view s) {
  return !s.empty() && std::all_of(s.begin(), s.end(), [](char c) {
    return c >= '0' && c <= '9';
  });
}
}  // namespace

const i128& q64_scale() { return SCALE; }
const i128& i128_min_value() { return I128_MIN; }
const i128& i128_max_value() { return I128_MAX; }

i128 Q64::checked_narrow(const i256& value) {
  if (value < i256(I128_MIN) || value > i256(I128_MAX)) {
    throw std::overflow_error("Q64_SIGNED_I128_OVERFLOW");
  }
  return static_cast<i128>(value);
}

Q64 Q64::from_raw(const i128& raw) {
  if (raw < I128_MIN || raw > I128_MAX) throw std::overflow_error("Q64_RAW_RANGE");
  return Q64(raw);
}

Q64 Q64::from_integer(std::int64_t value) {
  return Q64(checked_narrow(i256(value) * i256(SCALE)));
}

Q64 Q64::from_ratio(const i128& numerator, const i128& denominator) {
  if (denominator == 0) throw std::domain_error("Q64_DIVISION_BY_ZERO");
  return Q64(checked_narrow((i256(numerator) * i256(SCALE)) / i256(denominator)));
}

Q64 Q64::parse_decimal(std::string_view text) {
  if (text.empty()) throw std::invalid_argument("Q64_DECIMAL_EMPTY");
  bool negative = false;
  if (text.front() == '+' || text.front() == '-') {
    negative = text.front() == '-';
    text.remove_prefix(1);
  }
  if (text.empty()) throw std::invalid_argument("Q64_DECIMAL_INVALID");
  const auto dot = text.find('.');
  const std::string_view whole = dot == std::string_view::npos ? text : text.substr(0, dot);
  const std::string_view frac = dot == std::string_view::npos ? std::string_view{} : text.substr(dot + 1);
  if (whole.empty() || !digits_only(whole) || (!frac.empty() && !digits_only(frac))) {
    throw std::invalid_argument("Q64_DECIMAL_INVALID");
  }
  if (frac.size() > 18U) throw std::invalid_argument("Q64_DECIMAL_TOO_PRECISE");

  i256 whole_value = 0;
  for (const char c : whole) whole_value = whole_value * 10 + (c - '0');
  i256 raw = whole_value * i256(SCALE);
  if (!frac.empty()) {
    i256 frac_value = 0;
    for (const char c : frac) frac_value = frac_value * 10 + (c - '0');
    const i128 denom = pow10(static_cast<std::uint32_t>(frac.size()));
    raw += (frac_value * i256(SCALE)) / i256(denom);
  }
  if (negative) raw = -raw;
  return Q64(checked_narrow(raw));
}

std::string Q64::to_decimal(std::uint32_t fractional_digits) const {
  if (fractional_digits > 18U) throw std::invalid_argument("Q64_DECIMAL_DIGITS_TOO_LARGE");
  i256 value = raw_;
  const bool negative = value < 0;
  if (negative) value = -value;
  const i256 whole = value / i256(SCALE);
  i256 remainder = value % i256(SCALE);
  std::string out = whole.convert_to<std::string>();
  if (fractional_digits > 0U) {
    out.push_back('.');
    for (std::uint32_t i = 0; i < fractional_digits; ++i) {
      remainder *= 10;
      const i256 digit = remainder / i256(SCALE);
      remainder %= i256(SCALE);
      out.push_back(static_cast<char>('0' + digit.convert_to<unsigned>()));
    }
  }
  if (negative && raw_ != 0) out.insert(out.begin(), '-');
  return out;
}

Q64 Q64::checked_add(const Q64& other) const {
  return Q64(checked_narrow(i256(raw_) + i256(other.raw_)));
}
Q64 Q64::checked_sub(const Q64& other) const {
  return Q64(checked_narrow(i256(raw_) - i256(other.raw_)));
}
Q64 Q64::checked_mul(const Q64& other) const {
  return Q64(checked_narrow((i256(raw_) * i256(other.raw_)) / i256(SCALE)));
}
Q64 Q64::checked_div(const Q64& other) const {
  if (other.raw_ == 0) throw std::domain_error("Q64_DIVISION_BY_ZERO");
  return Q64(checked_narrow((i256(raw_) * i256(SCALE)) / i256(other.raw_)));
}
Q64 Q64::checked_mul_integer(const i128& value) const {
  return Q64(checked_narrow(i256(raw_) * i256(value)));
}

}  // namespace nexy::cfpc
