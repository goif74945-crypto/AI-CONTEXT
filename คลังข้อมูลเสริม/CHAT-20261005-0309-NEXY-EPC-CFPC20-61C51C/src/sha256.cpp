#include "nexy_cfpc/sha256.hpp"

#include <array>
#include <cstdint>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>

namespace nexy::cfpc {
namespace {
constexpr std::array<std::uint32_t, 64> K = {
  0x428a2f98U,0x71374491U,0xb5c0fbcfU,0xe9b5dba5U,0x3956c25bU,0x59f111f1U,0x923f82a4U,0xab1c5ed5U,
  0xd807aa98U,0x12835b01U,0x243185beU,0x550c7dc3U,0x72be5d74U,0x80deb1feU,0x9bdc06a7U,0xc19bf174U,
  0xe49b69c1U,0xefbe4786U,0x0fc19dc6U,0x240ca1ccU,0x2de92c6fU,0x4a7484aaU,0x5cb0a9dcU,0x76f988daU,
  0x983e5152U,0xa831c66dU,0xb00327c8U,0xbf597fc7U,0xc6e00bf3U,0xd5a79147U,0x06ca6351U,0x14292967U,
  0x27b70a85U,0x2e1b2138U,0x4d2c6dfcU,0x53380d13U,0x650a7354U,0x766a0abbU,0x81c2c92eU,0x92722c85U,
  0xa2bfe8a1U,0xa81a664bU,0xc24b8b70U,0xc76c51a3U,0xd192e819U,0xd6990624U,0xf40e3585U,0x106aa070U,
  0x19a4c116U,0x1e376c08U,0x2748774cU,0x34b0bcb5U,0x391c0cb3U,0x4ed8aa4aU,0x5b9cca4fU,0x682e6ff3U,
  0x748f82eeU,0x78a5636fU,0x84c87814U,0x8cc70208U,0x90befffaU,0xa4506cebU,0xbef9a3f7U,0xc67178f2U
};
constexpr std::array<std::uint32_t, 8> H0 = {
  0x6a09e667U,0xbb67ae85U,0x3c6ef372U,0xa54ff53aU,0x510e527fU,0x9b05688cU,0x1f83d9abU,0x5be0cd19U
};
[[nodiscard]] constexpr std::uint32_t rotr(std::uint32_t x, std::uint32_t n) {
  return (x >> n) | (x << (32U - n));
}
}

std::string sha256_hex(std::string_view input) {
  std::vector<std::uint8_t> msg(input.begin(), input.end());
  const std::uint64_t bit_len = static_cast<std::uint64_t>(msg.size()) * 8ULL;
  msg.push_back(0x80U);
  while ((msg.size() % 64U) != 56U) msg.push_back(0U);
  for (int i = 7; i >= 0; --i) msg.push_back(static_cast<std::uint8_t>((bit_len >> (i * 8)) & 0xffU));

  auto h = H0;
  for (std::size_t offset = 0; offset < msg.size(); offset += 64U) {
    std::array<std::uint32_t, 64> w{};
    for (std::size_t i = 0; i < 16U; ++i) {
      const std::size_t j = offset + i * 4U;
      w[i] = (static_cast<std::uint32_t>(msg[j]) << 24U)
           | (static_cast<std::uint32_t>(msg[j + 1U]) << 16U)
           | (static_cast<std::uint32_t>(msg[j + 2U]) << 8U)
           | static_cast<std::uint32_t>(msg[j + 3U]);
    }
    for (std::size_t i = 16U; i < 64U; ++i) {
      const std::uint32_t s0 = rotr(w[i - 15U], 7U) ^ rotr(w[i - 15U], 18U) ^ (w[i - 15U] >> 3U);
      const std::uint32_t s1 = rotr(w[i - 2U], 17U) ^ rotr(w[i - 2U], 19U) ^ (w[i - 2U] >> 10U);
      w[i] = w[i - 16U] + s0 + w[i - 7U] + s1;
    }
    std::uint32_t a=h[0], b=h[1], c=h[2], d=h[3], e=h[4], f=h[5], g=h[6], hh=h[7];
    for (std::size_t i=0;i<64U;++i) {
      const std::uint32_t S1=rotr(e,6U)^rotr(e,11U)^rotr(e,25U);
      const std::uint32_t ch=(e&f)^((~e)&g);
      const std::uint32_t temp1=hh+S1+ch+K[i]+w[i];
      const std::uint32_t S0=rotr(a,2U)^rotr(a,13U)^rotr(a,22U);
      const std::uint32_t maj=(a&b)^(a&c)^(b&c);
      const std::uint32_t temp2=S0+maj;
      hh=g; g=f; f=e; e=d+temp1; d=c; c=b; b=a; a=temp1+temp2;
    }
    h[0]+=a; h[1]+=b; h[2]+=c; h[3]+=d; h[4]+=e; h[5]+=f; h[6]+=g; h[7]+=hh;
  }
  std::ostringstream out;
  out << std::hex << std::setfill('0');
  for (const auto v : h) out << std::setw(8) << v;
  return out.str();
}

}  // namespace nexy::cfpc
