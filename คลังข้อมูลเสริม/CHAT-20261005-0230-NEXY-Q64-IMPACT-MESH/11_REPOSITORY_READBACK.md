# Repository Read-Back Evidence

Tested snapshot revision: `ac85525121a59aefe46737b7e97ff1f4d9522f59`

Exact files were fetched back from GitHub at that immutable revision.

| File | Expected Git blob SHA-1 | Read-back |
|---|---|---|
| PROJECT_INDEX.md | a1c36e30264371f301f26db308e53b3c1ea7202b | MATCH |
| VERIFICATION_SNAPSHOT.md | c7ee3d1613569dd314008bd9b6498b55e4e8767c | MATCH |
| SHA256SUMS.txt | 52cfdfc3880fbf3b34549dcba84a3c4833308a65 | MATCH |
| part00 | 1ae9a8061808850dc04d2665f966403a0c818be8 | MATCH |
| part01 | 80ceb2116e0a8e8ccf4ba29436934944551c0a9e | MATCH |
| part02 | 4e30632e3237acfac54c7269c63b1f81d2d67e9e | MATCH |
| part03 | 3b3f0965437fba8f4bcd99c63a94d32705bf7c52 | MATCH |

Publication race history:
- attempt 1: rejected non-fast-forward;
- attempt 2: rejected non-fast-forward;
- attempt 3: rebased on current head, non-force update succeeded.

No protected NEXY.AI repository was targeted by mutation tools.
