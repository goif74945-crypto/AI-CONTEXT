#pragma once

#include <boost/multiprecision/cpp_int.hpp>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <string_view>

namespace nexy::cfpc {

using i128 = boost::multiprecision::int128_t;
using i256 = boost::multiprecision::int256_t;

class Q64 final {
 public:
  static constexpr std::uint32_t FRACTION_BITS = 64;

  Q64() = default;

  static Q64 from_raw(const i128& raw);
  static Q64 from_integer(std::int64_t value);
  static Q64 from_ratio(const i128& numerator, const i128& denominator);
  static Q64 parse_decimal(std::string_view text);

  [[nodiscard]] const i128& raw() const noexcept { return raw_; }
  [[nodiscard]] std::string to_decimal(std::uint32_t fractional_digits = 18) const;

  [[nodiscard]] Q64 checked_add(const Q64& other) const;
  [[nodiscard]] Q64 checked_sub(const Q64& other) const;
  [[nodiscard]] Q64 checked_mul(const Q64& other) const;
  [[nodiscard]] Q64 checked_div(const Q64& other) const;
  [[nodiscard]] Q64 checked_mul_integer(const i128& value) const;

  friend bool operator==(const Q64&, const Q64&) = default;
  friend bool operator<(const Q64& a, const Q64& b) noexcept { return a.raw_ < b.raw_; }
  friend bool operator>(const Q64& a, const Q64& b) noexcept { return b < a; }
  friend bool operator<=(const Q64& a, const Q64& b) noexcept { return !(a > b); }
  friend bool operator>=(const Q64& a, const Q64& b) noexcept { return !(a < b); }

 private:
  explicit Q64(i128 raw) : raw_(std::move(raw)) {}
  static i128 checked_narrow(const i256& value);
  i128 raw_{0};
};

[[nodiscard]] const i128& q64_scale();
[[nodiscard]] const i128& i128_min_value();
[[nodiscard]] const i128& i128_max_value();

}  // namespace nexy::cfpc
