# EX018 Independent RED: unused OTAC utility defects
SOURCE_REPO: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.ai
SOURCE_REVISION: 58b1200bd61b867e917057d0019eea78ea9f6b2a
FILE: packages/auth/otac.ts
SOURCE_GIT_BLOB_SHA: bb6134ab1946c8cfa8f130eb7eea5a777d02c58e
RUNNER: Existing Floot VM id bbdaa2a3-a6ff-4b49-b8d1-462eb5863f29, Node 22.23.2, isolated temporary directory, `node --experimental-transform-types --test test.mjs`; source fetched verbatim with authorized GitHub connector.
ACTUAL RESULT: 14 tests, 11 PASS, 3 FAIL, process exit 1; no Product write by independent auditor.
FAILED 12: safeEqual("é","a") -> RangeError ERR_CRYPTO_TIMING_SAFE_EQUAL_LENGTH, expected false.
FAILED 13: safeEqual("🙂","ab") -> same RangeError, expected false.
FAILED 14: computeDeviceId("foo1","2.3.4.5") === computeDeviceId("foo","12.3.4.5"), sha256 269adda7ef0550b38e446729413cebaee4f45065cd608b2b5eb7a1cbd5d12ac8, even though input tuples differ.
SOURCE_CAUSE: `safeEqual` compares JS UTF-16 `string.length` then passes UTF-8 Buffers to crypto.timingSafeEqual; identical UTF-16 length does NOT imply equal byte length. `computeDeviceId` concatenates userAgent+ipAddress with no prefix-length or delimiter framing, so distinct tuple serialization is non-injective.
NEGATIVE PROOF CORRECTIVE: Search `computeDeviceId` across all 887 eligible UTF-8 blobs found ONLY its definition in packages/auth/otac.ts. Search `safeEqual(` found helper definition but no import/caller of this helper (other occurrences are `timingSafeEqual`). Hence CURRENT PRODUCTION REACHABILITY NOT PROVEN, cannot claim session bypass or exploit. Actual auth uses packages/auth/device-binding.ts with separate CSPRNG binding-token SHA256 and constant-time comparison of fixed-size hex-derived buffers.
REPRODUCTION:
```ts
import { safeEqual, computeDeviceId } from "./packages/auth/otac.ts";
safeEqual("é","a"); // throws ERR_CRYPTO_TIMING_SAFE_EQUAL_LENGTH, expected false
safeEqual("🙂","ab"); // throws same RangeError, expected false
computeDeviceId("foo1","2.3.4.5") === computeDeviceId("foo","12.3.4.5"); // true, semantic collision
```
EXPECTED_REPAIR: if preserving exported APIs is required, compare Buffer byte lengths and return false before timingSafeEqual, document supported Unicode behavior; encode device tuple unambiguously using length-prefix or structured canonical representation, with migration/compat review if ever persisted; add negative tests. DO NOT change actual session format until authorized spec+dependency analysis.
CLASSIFICATION: S3 UTILITY CORRECTNESS; live exploit status UNVERIFIED / no importer observed.
HISTORICAL SCOPE: These are tests against exact HEAD only. Future HEAD invalidates pass/fail freshness.
