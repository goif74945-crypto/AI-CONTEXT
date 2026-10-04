#pragma once

#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <compare>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <string>

namespace mmcrc {

using i128 = __int128_t;
using u128 = __uint128_t;
using boost::multiprecision::int256_t;

class Q64 final {
 public:
  static constexpr int FRACTION_BITS = 64;
  constexpr Q64() noexcept : raw_(0) {}
  static constexpr Q64 from_raw(i128 raw) noexcept { return Q64(raw, RawTag{}); }
  static constexpr Q64 zero() noexcept { return from_raw(0); }
  static constexpr Q64 one() noexcept { return from_raw(static_cast<i128>(u128{1} << 64)); }
  static Q64 from_integer(std::int64_t value) {
    const int256_t wide = int256_t(value) << FRACTION_BITS;
    return checked_from_wide(wide, "Q64 integer overflow");
  }
  static Q64 from_ratio(std::int64_t numerator, std::int64_t denominator) {
    if (denominator == 0) throw std::domain_error("Q64 division by zero");
    const int256_t scaled = int256_t(numerator) << FRACTION_BITS;
    return checked_from_wide(scaled / int256_t(denominator), "Q64 ratio overflow");
  }
  [[nodiscard]] constexpr i128 raw() const noexcept { return raw_; }
  [[nodiscard]] static Q64 add(Q64 a, Q64 b) {
    return checked_from_wide(int256_t(a.raw_) + int256_t(b.raw_), "Q64 addition overflow");
  }
  [[nodiscard]] static Q64 sub(Q64 a, Q64 b) {
    return checked_from_wide(int256_t(a.raw_) - int256_t(b.raw_), "Q64 subtraction overflow");
  }
  [[nodiscard]] static Q64 mul(Q64 a, Q64 b) {
    const int256_t product = int256_t(a.raw_) * int256_t(b.raw_);
    return checked_from_wide(product >> FRACTION_BITS, "Q64 multiplication overflow");
  }
  [[nodiscard]] static Q64 div(Q64 a, Q64 b) {
    if (b.raw_ == 0) throw std::domain_error("Q64 division by zero");
    const int256_t numerator = int256_t(a.raw_) << FRACTION_BITS;
    return checked_from_wide(numerator / int256_t(b.raw_), "Q64 division overflow");
  }
  [[nodiscard]] static Q64 ratio(std::uint64_t numerator, std::uint64_t denominator) {
    if (denominator == 0) throw std::domain_error("Q64 ratio division by zero");
    const int256_t scaled = int256_t(numerator) << FRACTION_BITS;
    return checked_from_wide(scaled / int256_t(denominator), "Q64 ratio overflow");
  }
  [[nodiscard]] static Q64 unit_checked(Q64 value, const char* label) {
    if (value < zero() || value > one()) throw std::range_error(std::string(label) + " must be in Q64 [0,1]");
    return value;
  }
  [[nodiscard]] std::string raw_string() const {
    if (raw_ == 0) return "0";
    const bool negative = raw_ < 0;
    u128 magnitude;
    if (negative) { magnitude = static_cast<u128>(-(raw_ + 1)); magnitude += 1; }
    else magnitude = static_cast<u128>(raw_);
    std::string out;
    while (magnitude != 0) {
      const unsigned digit = static_cast<unsigned>(magnitude % 10);
      out.push_back(static_cast<char>('0' + digit));
      magnitude /= 10;
    }
    if (negative) out.push_back('-');
    std::reverse(out.begin(), out.end());
    return out;
  }
  friend constexpr bool operator==(Q64, Q64) noexcept = default;
  friend constexpr std::strong_ordering operator<=>(Q64 a, Q64 b) noexcept { return a.raw_ <=> b.raw_; }

 private:
  struct RawTag {};
  constexpr Q64(i128 raw, RawTag) noexcept : raw_(raw) {}
  static Q64 checked_from_wide(const int256_t& value, const char* message) {
    const int256_t minv = -(int256_t(1) << 127);
    const int256_t maxv = (int256_t(1) << 127) - 1;
    if (value < minv || value > maxv) throw std::overflow_error(message);
    return from_raw(static_cast<i128>(value));
  }
  i128 raw_;
};

}  // namespace mmcrc
