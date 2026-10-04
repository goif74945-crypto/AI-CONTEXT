#pragma once
#include <string>
#include <string_view>
namespace nexy::cfpc {
[[nodiscard]] std::string sha256_hex(std::string_view input);
}
