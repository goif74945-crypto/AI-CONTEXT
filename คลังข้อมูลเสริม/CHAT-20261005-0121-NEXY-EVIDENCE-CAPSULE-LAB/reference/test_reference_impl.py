import copy, unittest
from datetime import datetime, timedelta, timezone
from reference_impl import *

K = b"k" * 32
T = datetime(2026, 10, 5, 0, 0, tzinfo=timezone.utc)
REC = {"public":"ok", "internal":{"n":1}, "secret":"hidden"}
CLS = {"public":"PUBLIC", "internal":"INTERNAL", "secret":"SECRET"}
SALTS = {"public":b"p"*32, "internal":b"i"*32, "secret":b"s"*32}

def sealed():
    return seal(REC, record_id="r1", issuer="lab", key_id="k1", key=K, issued_at=T,
                expires_at=T+timedelta(hours=1), salts=SALTS, nonce="fixed")

def bundle(fields=("public",), role="PUBLIC_USER", audience="viewer", shown=None):
    return present(sealed(), fields=fields, role=role, purpose="audit", audience=audience,
                   classifications=CLS, key=K, presented_at=shown or T+timedelta(minutes=1), nonce="p1")

class Tests(unittest.TestCase):
    def test_canonical_key_order(self): self.assertEqual(canonical({"b":1,"a":2}), canonical({"a":2,"b":1}))
    def test_float_rejected(self):
        with self.assertRaises(IntegrityError): canonical({"x":1.2})
    def test_non_string_key_rejected(self):
        with self.assertRaises(IntegrityError): canonical({1:"x"})
    def test_deterministic_capsule(self): self.assertEqual(sealed()["header"]["capsule_id"], sealed()["header"]["capsule_id"])
    def test_empty_record(self):
        with self.assertRaises(IntegrityError): seal({},record_id="r",issuer="i",key_id="k1",key=K,issued_at=T,expires_at=T+timedelta(seconds=1))
    def test_short_key(self):
        with self.assertRaises(IntegrityError): seal({"x":1},record_id="r",issuer="i",key_id="k",key=b"x",issued_at=T,expires_at=T+timedelta(seconds=1))
    def test_public_policy(self): bundle()
    def test_policy_denies_internal(self):
        with self.assertRaises(PolicyError): bundle(("internal",))
    def test_owner_secret(self): bundle(("secret",), role="OWNER")
    def test_unknown_role(self):
        with self.assertRaises(PolicyError): bundle(role="NOPE")
    def test_valid_verify(self):
        out=verify(bundle(),keys={"k1":K},now=T+timedelta(minutes=2),expected_audience="viewer",required_fields=["public"])
        self.assertEqual(out["fields"],["public"])
    def test_tamper_value(self):
        b=bundle(); b["presentation"]["disclosures"][0]["value"]="evil"
        with self.assertRaises(IntegrityError): verify(b,keys={"k1":K},now=T+timedelta(minutes=2))
    def test_tamper_header(self):
        b=bundle(); b["header"]["record_id"]="evil"
        with self.assertRaises(IntegrityError): verify(b,keys={"k1":K},now=T+timedelta(minutes=2))
    def test_wrong_audience(self):
        with self.assertRaises(IntegrityError): verify(bundle(),keys={"k1":K},now=T+timedelta(minutes=2),expected_audience="other")
    def test_missing_required(self):
        with self.assertRaises(IntegrityError): verify(bundle(),keys={"k1":K},now=T+timedelta(minutes=2),required_fields=["internal"])
    def test_expired(self):
        with self.assertRaises(FreshnessError): verify(bundle(),keys={"k1":K},now=T+timedelta(hours=2))
    def test_stale(self):
        with self.assertRaises(FreshnessError): verify(bundle(),keys={"k1":K},now=T+timedelta(minutes=10),max_age=60)
    def test_replay(self):
        guard=set(); b=bundle(); verify(b,keys={"k1":K},now=T+timedelta(minutes=2),replay=guard)
        with self.assertRaises(ReplayError): verify(b,keys={"k1":K},now=T+timedelta(minutes=2),replay=guard)
    def test_bad_key_registry(self):
        with self.assertRaises(IntegrityError): verify(bundle(),keys={"k1":b"z"*32},now=T+timedelta(minutes=2))
    def test_bad_proof(self):
        b=bundle(); b["presentation"]["disclosures"][0]["proof"][0]["hash"]="00"*32
        with self.assertRaises(IntegrityError): verify(b,keys={"k1":K},now=T+timedelta(minutes=2))

if __name__ == "__main__": unittest.main(verbosity=2)
