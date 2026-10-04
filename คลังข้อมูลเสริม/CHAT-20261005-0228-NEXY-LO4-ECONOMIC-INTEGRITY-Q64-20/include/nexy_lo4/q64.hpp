#pragma once

#include <boost/multiprecision/cpp_int.hpp>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <string_view>

namespace nexy::lo4 {

class Q64 final {
public:
    using storage_type = __int128_t;
    using wide_type = boost::multiprecision::int256_t;

    constexpr Q64() noexcept = default;

    [[nodiscard]] static constexpr Q64 from_raw(storage_type raw) noexcept {
        return Q64(raw, RawTag{});
    }

    [[nodiscard]] static constexpr Q64 zero() noexcept { return from_raw(0); }
    [[nodiscard]] static constexpr Q64 one() noexcept { return from_raw(storage_type{1} << 64); }

    [[nodiscard]] static Q64 from_int(std::int64_t value) {
        const wide_type w = wide_type(value) << 64;
        return from_wide_checked(w, "Q64::from_int overflow");
    }

    [[nodiscard]] static Q64 from_ratio(std::int64_t numerator, std::int64_t denominator) {
        if (denominator == 0) {
            throw std::domain_error("Q64::from_ratio division by zero");
        }
        wide_type n = wide_type(numerator) << 64;
        const wide_type d = denominator;
        return from_wide_checked(n / d, "Q64::from_ratio overflow");
    }

    [[nodiscard]] static Q64 from_basis_points(std::int32_t basis_points) {
        return from_ratio(basis_points, 10'000);
    }

    [[nodiscard]] constexpr storage_type raw() const noexcept { return raw_; }

    [[nodiscard]] std::string raw_decimal() const {
        return wide_type(raw_).convert_to<std::string>();
    }

    [[nodiscard]] std::string decimal(unsigned fractional_digits = 6) const {
        if (fractional_digits > 18) {
            throw std::invalid_argument("Q64::decimal fractional_digits must be <= 18");
        }
        wide_type v = raw_;
        const bool negative = v < 0;
        if (negative) v = -v;
        const wide_type scale = wide_type{1} << 64;
        const wide_type integer = v / scale;
        wide_type remainder = v % scale;

        std::string out;
        if (negative) out.push_back('-');
        out += integer.convert_to<std::string>();
        if (fractional_digits == 0) return out;
        out.push_back('.');
        for (unsigned i = 0; i < fractional_digits; ++i) {
            remainder *= 10;
            const wide_type digit = remainder / scale;
            remainder %= scale;
            out.push_back(static_cast<char>('0' + digit.convert_to<unsigned>()));
        }
        return out;
    }

    [[nodiscard]] friend Q64 operator+(Q64 lhs, Q64 rhs) {
        return from_wide_checked(wide_type(lhs.raw_) + wide_type(rhs.raw_), "Q64 addition overflow");
    }

    [[nodiscard]] friend Q64 operator-(Q64 lhs, Q64 rhs) {
        return from_wide_checked(wide_type(lhs.raw_) - wide_type(rhs.raw_), "Q64 subtraction overflow");
    }

    [[nodiscard]] friend Q64 operator-(Q64 value) {
        return from_wide_checked(-wide_type(value.raw_), "Q64 negation overflow");
    }

    [[nodiscard]] friend Q64 operator*(Q64 lhs, Q64 rhs) {
        const wide_type product = wide_type(lhs.raw_) * wide_type(rhs.raw_);
        const wide_type scale = wide_type{1} << 64;
        return from_wide_checked(product / scale, "Q64 multiplication overflow");
    }

    [[nodiscard]] friend Q64 operator/(Q64 lhs, Q64 rhs) {
        if (rhs.raw_ == 0) {
            throw std::domain_error("Q64 division by zero");
        }
        const wide_type numerator = wide_type(lhs.raw_) << 64;
        return from_wide_checked(numerator / wide_type(rhs.raw_), "Q64 division overflow");
    }

    Q64& operator+=(Q64 rhs) { return *this = *this + rhs; }
    Q64& operator-=(Q64 rhs) { return *this = *this - rhs; }
    Q64& operator*=(Q64 rhs) { return *this = *this * rhs; }
    Q64& operator/=(Q64 rhs) { return *this = *this / rhs; }

    [[nodiscard]] friend constexpr bool operator==(Q64, Q64) noexcept = default;
    [[nodiscard]] friend constexpr auto operator<=>(Q64 lhs, Q64 rhs) noexcept {
        return lhs.raw_ <=> rhs.raw_;
    }

    [[nodiscard]] static Q64 abs(Q64 value) {
        return value.raw_ < 0 ? -value : value;
    }

    [[nodiscard]] static constexpr Q64 min(Q64 a, Q64 b) noexcept { return a.raw_ < b.raw_ ? a : b; }
    [[nodiscard]] static constexpr Q64 max(Q64 a, Q64 b) noexcept { return a.raw_ > b.raw_ ? a : b; }

    [[nodiscard]] static Q64 clamp(Q64 value, Q64 lower, Q64 upper) {
        if (lower > upper) {
            throw std::invalid_argument("Q64::clamp lower > upper");
        }
        return min(max(value, lower), upper);
    }

    [[nodiscard]] static Q64 clamp01(Q64 value) {
        return clamp(value, zero(), one());
    }

private:
    struct RawTag {};
    storage_type raw_{0};

    constexpr Q64(storage_type raw, RawTag) noexcept : raw_(raw) {}

    [[nodiscard]] static wide_type max_raw_wide() {
        return (wide_type{1} << 127) - 1;
    }

    [[nodiscard]] static wide_type min_raw_wide() {
        return -(wide_type{1} << 127);
    }

    [[nodiscard]] static Q64 from_wide_checked(const wide_type& value, std::string_view message) {
        if (value > max_raw_wide() || value < min_raw_wide()) {
            throw std::overflow_error(std::string(message));
        }
        return from_raw(value.convert_to<storage_type>());
    }
};

inline void require_unit(Q64 value, std::string_view field) {
    if (value < Q64::zero() || value > Q64::one()) {
        throw std::invalid_argument(std::string(field) + " must be in [0,1]");
    }
}

inline void require_nonnegative(Q64 value, std::string_view field) {
    if (value < Q64::zero()) {
        throw std::invalid_argument(std::string(field) + " must be nonnegative");
    }
}

} // namespace nexy::lo4
