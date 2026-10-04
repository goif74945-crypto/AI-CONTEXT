# IRC-20 Local Exact-Byte Seal

MANIFEST_SHA256: `2c7925d9ad17acd439e709616c020e563c65eefd3edd7b75371d7efc186649b7`
SEALED_FILE_COUNT: `61`
SOURCE_FILE_COUNT: `11`
TEST_FILE_COUNT: `7`
PER_MECHANISM_DESIGN_FILE_COUNT: `20`
CLEAN_VERIFY: `PASS`
CLEAN_CLI_HEALTHY_REPLAY: `BYTE_IDENTICAL`
CLEAN_CLI_BROKEN_EXIT: `1`
NEXY_MUTATION: `NONE / FORBIDDEN`

The manifest hashes exact local candidate bytes excluding generated `dist/`, itself, and this seal file. A GitHub publication is not considered verified until remote read-back reproduces these file hashes.
