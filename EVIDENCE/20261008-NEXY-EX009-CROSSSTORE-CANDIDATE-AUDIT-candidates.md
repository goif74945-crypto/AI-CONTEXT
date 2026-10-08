# 009 Candidate decision table
Source product HEAD 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08, exact original packages/queue/dispatch.ts blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29.
| Candidate | Patch SHA | Source after apply | Matching regression test SHA | Original RED this turn | Own GREEN this turn | Product typecheck | G3 real PG Redis | Verdict |
|---|---|---|---|---|---|---|---|---|
| A FIXED | b7c9444d4348fd84691cea287c9477e6c90dd734 | 36e56aef98a5b8b52f644a0178eb3638d2c4b9af | 8900ea58bb5b94c5ccc5e38e2079276df3954cfc | executed on unpatched source | 9/9 exit 0 | see remote check log | NOT_RUN | HOLD |
| B FENCED | 3296992af5276641046accc5941ed595008b63e3 | 94340b7a591e2961b03591780668352ade165394 | e64653d893e5403ebf60505303c63a590a8cdcf5 | executed on unpatched source | 9/9 exit 0 | see remote check log | NOT_RUN | HOLD |
| C PATCHES/008 | 4236bcf95a1541065053d9c77d0558f923523537 | 4610dd2d0da5aee7f1cc525b83b0815eef11fb29 | 3c3c477551c3036f1800e3b5216c43b2fcc4d3d7 | executed on unpatched source | 10/10 exit 0 | see remote check log | NOT_RUN | HOLD |
All patches passed git apply --check, git diff --check and reverse to original Git source blob; no substitutions across test families. Superseded corrupted patch blob ac06e695aa6e4944acbbaf6d626b5f2a73e91ac8 was NEVER used.
Potential preference C contains extra PROCESSING early-return & CAS lastError guard, but no G3; C is not selected for production. A and B have their own semantics. Cannot claim best security before cross-store proof.
