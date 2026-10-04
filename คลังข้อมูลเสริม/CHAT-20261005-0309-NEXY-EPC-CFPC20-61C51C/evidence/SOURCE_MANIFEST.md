# CFPC-20 Exact Tested Source Manifest

The following SHA-256 and Git blob identities were computed from the exact local bytes used for the final GCC/Clang/ASan test cycle. GitHub read-back matched every listed Git blob identity.

| Path | SHA-256 | Git blob SHA-1 | Published read-back |
|---|---|---|---|
| CMakeLists.txt | 69ffd1ce5a4293b08113acc4bcec6b5621984875ff9d2cd01613542b350c450a | 5a811ed92af2a48e2a2ef8902cd0aa5a5b502a37 | MATCH |
| include/nexy_cfpc/q64.hpp | f1610e3c6057d335c0db3ff642725aff7f9f8b7027fc60c8e9cf2df6f9127ecc | e85f223a35ad58c6824fc1ed67ad482fe3f246cb | MATCH |
| include/nexy_cfpc/sha256.hpp | 1298bd4047951c4c83b0067aec94cd169330036ddf13c6eb24ac4a6e69cb793f | d48825770099090ad2fe185a954d23d50c4d8fef | MATCH |
| include/nexy_cfpc/cfpc.hpp | 59428ed729d265f2bd9ce8087deabeb6532fdfc872dd0bd6cf10be9d83fe2a58 | 96fe39ebb7645a6d4ded8d743cb79c530992248f | MATCH |
| src/q64.cpp | f2d9bd09e3af7c2bb2d3081d830417df31492936f3875e97d443e480a012e563 | 5012101c3eb1a202340c835d80fbfe6a32da72aa | MATCH |
| src/sha256.cpp | c6fa5d5b14e899d5eb9ddd65fd19d938dbf4c624ae302a058ae6793004aeacdc | 9f99dd63d074e4cd96d99384432eda2db3d8f4a1 | MATCH |
| src/cfpc.cpp | 2f1c557c653d8e29dc44474c2dcef1bbfcd7cabbae61a5d99483e7fd46c7d95a | d1b6d89dd1b1898d19eb78b5477c7da0b303f66c | MATCH |
| tests/test_cfpc.cpp | 3bd6561818e951ed1c3565575d0adbcee44dfdaa589de30b02ed3b5f1aa5bb65 | 3fae3b7ea4d0395b3589ef34a55785dbeff56010 | MATCH |
| examples/integration_example.cpp | 44da5fe15e6bcc22a04903da9b5b940652e7000f997c5140e77866ba2a946dbf | e3c721a3329d611f266e013279c4fd11acd26914 | MATCH |

This manifest proves byte identity for the standalone source/test set only. It does not prove NEXY integration or deployment.
