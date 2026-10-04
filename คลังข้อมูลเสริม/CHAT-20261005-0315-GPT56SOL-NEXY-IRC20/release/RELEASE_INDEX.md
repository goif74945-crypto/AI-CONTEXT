# IRC-20 Deterministic Release Index

RELEASE_KIND: `Lo4 reference / non-canonical / non-governing`
CHAT_ID: `CHAT-20261005-0315-GPT56SOL-NEXY-IRC20`
PLATFORM_NATIVE_CHAT_ID: `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
ARCHIVE_SHA256: `59bb050e80ea8a423bd835a2f66447ddd5f09be069bca5f1caca8acb87fc1253`
ARCHIVE_BYTES: `42904`
BASE64_BYTES: `57208`
BASE64_PARTS: `1`
TREE_MANIFEST_SHA256: `2c7925d9ad17acd439e709616c020e563c65eefd3edd7b75371d7efc186649b7`
TREE_SEALED_FILES: `61 + MANIFEST.sha256 + evidence/LOCAL_SEAL.md = 63`

## Reconstruct

`cat IRC20_RELEASE.tar.gz.b64.part* | base64 -d > IRC20_RELEASE.tar.gz`

`sha256sum IRC20_RELEASE.tar.gz`

Expected: `59bb050e80ea8a423bd835a2f66447ddd5f09be069bca5f1caca8acb87fc1253`

`mkdir IRC20_RELEASE && tar -xzf IRC20_RELEASE.tar.gz -C IRC20_RELEASE`

Then inside the reconstructed tree:

`npm run verify`

## Integrity law
The archive contains the exact local candidate tree used for the clean verification record. The release index is external to the archive to avoid self-referential hashing. This artifact has no Canon/promotion authority.
