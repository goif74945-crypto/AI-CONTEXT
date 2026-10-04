#pragma once

#include <cstdint>
#include <stdexcept>
#include <string>

namespace nexy::epc {

class ArithmeticFreeze final : public std::runtime_error {
public:
  explicit ArithmeticFreeze(const char* message) : std::runtime_error(message) {}
};

class Q64 final {
public:
  using raw_type = __int128_t;

  constexpr Q64() noexcept = default;

  static constexpr Q64 from_raw(raw_type raw) noexcept { return Q64(raw); }
  static Q64 from_ratio(std::int64_t numerator, std::int64_t denominator);

  static constexpr Q64 zero() noexcept { return Q64(0); }
  static constexpr Q64 one() noexcept { return Q64(raw_type{1} << 64); }
  static constexpr Q64 max() noexcept { return Q64(max_raw()); }
  static constexpr Q64 min() noexcept { return Q64(min_raw()); }

  [[nodiscard]] constexpr raw_type raw() const noexcept { return raw_; }
  [[nodiscard]] std::string raw_decimal() const;

  friend Q64 operator+(Q64 a, Q64 b);
  friend Q64 operator-(Q64 a, Q64 b);
  friend Q64 operator*(Q64 a, Q64 b);
  friend Q64 operator/(Q64 a, Q64 b);

  friend constexpr bool operator==(Q64, Q64) noexcept = default;
  friend constexpr auto operator<=>(Q64, Q64) noexcept = default;

private:
  explicit constexpr Q64(raw_type raw) noexcept : raw_(raw) {}

  static constexpr raw_type max_raw() noexcept {
    using u128 = __uint128_t;
    return static_cast<raw_type>((u128{1} << 127) - u128{1});
  }
  static constexpr raw_type min_raw() noexcept { return -max_raw() - raw_type{1}; }

  raw_type raw_{0};
};

} // namespace nexy::epc
