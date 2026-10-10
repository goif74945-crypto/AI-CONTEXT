# CASE EX018 Prisma audit continuation
RISK: Source contains up/down migrations with DROP/ALTER; this is not itself a defect because rollback scripts deliberately reverse migrations.
NEGATIVE CLAIM CORRECTION: No PostgreSQL execution in this turn -> cannot infer migration failed; 57 files read does not prove production schema or rollback.
FINDING: User emailHash unique vs literal historical 'User.email unique' requires semantic normalization and migration consideration; current source-based uniqueness assertion passes. Verify DB constraints in runtime.
ACTION: 57/57 Prisma files SHA-matched, 21/21 independent structural source assertions pass.
ROLLBACK: Product unchanged; Control log only.
