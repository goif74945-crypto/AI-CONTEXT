from __future__ import annotations

import base64, hashlib, hmac, json, secrets
from datetime import datetime, timezone

PROTOCOL = "NEXY-EVIDENCE-CAPSULE/1-LAB"
SIG_ALG = "HMAC-SHA256-REFERENCE-ONLY"
ROLES = {
    "PUBLIC_USER": {"PUBLIC"},
    "OPERATOR": {"PUBLIC", "INTERNAL"},
    "AUDITOR": {"PUBLIC", "INTERNAL", "SENSITIVE"},
    "OWNER": {"PUBLIC", "INTERNAL", "SENSITIVE", "SECRET"},
    "SYSTEM": {"PUBLIC", "INTERNAL", "SENSITIVE", "SECRET"},
}

class CapsuleError(ValueError): pass
class PolicyError(CapsuleError): pass
class IntegrityError(CapsuleError): pass
class FreshnessError(CapsuleError): pass
class ReplayError(CapsuleError): pass


def canonical(value):
    def valid(v):
        if v is None or isinstance(v, (bool, int, str)): return
        if isinstance(v, float): raise IntegrityError("floats are forbidden")
        if isinstance(v, list):
            for x in v: valid(x)
            return
        if isinstance(v, dict):
            if any(not isinstance(k, str) for k in v): raise IntegrityError("object keys must be strings")
            for x in v.values(): valid(x)
            return
        raise IntegrityError(f"unsupported type: {type(v).__name__}")
    valid(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(data): return hashlib.sha256(data).digest()
def hx(data): return hashlib.sha256(data).hexdigest()
def b64(data): return base64.urlsafe_b64encode(data).rstrip(b"=").decode()
def unb64(text): return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))
def iso(dt):
    if dt.tzinfo is None or dt.utcoffset() is None: raise IntegrityError("timezone-aware datetime required")
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
def parse(text):
    if not isinstance(text, str) or not text.endswith("Z"): raise IntegrityError("UTC Z timestamp required")
    return datetime.fromisoformat(text[:-1] + "+00:00")
def sign(domain, obj, key):
    if not isinstance(key, bytes) or len(key) < 32: raise IntegrityError("signing key must be >=32 bytes")
    return hmac.new(key, domain + canonical(obj), hashlib.sha256).hexdigest()


def leaf(name, value, salt): return sha(b"NEXY-LEAF\0" + canonical(name) + b"\0" + canonical(value) + b"\0" + salt)
def node(left, right): return sha(b"NEXY-NODE\0" + left + right)
def root(leaves):
    if not leaves: raise IntegrityError("empty Merkle tree")
    level = list(leaves)
    while len(level) > 1:
        if len(level) % 2: level.append(level[-1])
        level = [node(level[i], level[i+1]) for i in range(0, len(level), 2)]
    return level[0]
def proof(leaves, index):
    out, level, pos = [], list(leaves), index
    while len(level) > 1:
        if len(level) % 2: level.append(level[-1])
        sibling = pos-1 if pos % 2 else pos+1
        out.append({"side": "L" if pos % 2 else "R", "hash": level[sibling].hex()})
        level = [node(level[i], level[i+1]) for i in range(0, len(level), 2)]
        pos //= 2
    return out
def verify_proof(digest, steps, expected):
    cur = digest
    for step in steps:
        try: sibling = bytes.fromhex(step["hash"])
        except Exception as exc: raise IntegrityError("invalid proof hash") from exc
        if len(sibling) != 32 or step.get("side") not in {"L", "R"}: raise IntegrityError("invalid proof step")
        cur = node(sibling, cur) if step["side"] == "L" else node(cur, sibling)
    return hmac.compare_digest(cur, expected)


def seal(record, *, record_id, issuer, key_id, key, issued_at, expires_at, salts=None, nonce=None):
    if not isinstance(record, dict) or not record: raise IntegrityError("record required")
    names = sorted(record, key=lambda x: x.encode())
    if any(not isinstance(n, str) for n in names): raise IntegrityError("field names must be strings")
    if expires_at <= issued_at: raise FreshnessError("invalid validity interval")
    salts = dict(salts or {n: secrets.token_bytes(32) for n in names})
    if set(salts) != set(names) or any(not isinstance(v, bytes) or len(v) < 16 for v in salts.values()):
        raise IntegrityError("salts must cover all fields and be >=16 bytes")
    leaves = [leaf(n, record[n], salts[n]) for n in names]
    unsigned = {"protocol": PROTOCOL, "signature_algorithm": SIG_ALG, "record_id": record_id,
                "issuer": issuer, "key_id": key_id, "issued_at": iso(issued_at), "expires_at": iso(expires_at),
                "nonce": nonce or b64(secrets.token_bytes(18)), "field_count": len(names), "root": root(leaves).hex()}
    sig = sign(b"NEXY-CAPSULE-HDR\0", unsigned, key)
    header0 = {**unsigned, "signature": sig}
    header = {**header0, "capsule_id": hx(b"NEXY-CAPSULE-ID\0" + canonical(header0))}
    return {"header": header, "names": names, "values": record, "salts": salts, "leaves": leaves}


def present(sealed, *, fields, role, purpose, audience, classifications, key, presented_at, nonce=None):
    allowed = ROLES.get(role)
    if allowed is None: raise PolicyError("unknown role")
    wanted = list(dict.fromkeys(fields))
    if not wanted: raise PolicyError("at least one field required")
    index = {n:i for i,n in enumerate(sealed["names"])}
    disclosed = []
    for name in wanted:
        if name not in index: raise IntegrityError(f"unknown field: {name}")
        cls = classifications.get(name)
        if cls not in allowed: raise PolicyError(f"role {role} cannot disclose {name}")
        i = index[name]
        disclosed.append({"field": name, "value": sealed["values"][name], "salt": b64(sealed["salts"][name]),
                          "index": i, "proof": proof(sealed["leaves"], i)})
    unsigned = {"capsule_id": sealed["header"]["capsule_id"], "role": role, "purpose": purpose,
                "audience": audience, "presented_at": iso(presented_at), "nonce": nonce or b64(secrets.token_bytes(18)),
                "disclosures": disclosed}
    sig = sign(b"NEXY-PRESENTATION\0", unsigned, key)
    pres0 = {**unsigned, "signature": sig}
    return {"header": sealed["header"], "presentation": {**pres0, "presentation_id": hx(b"NEXY-PRES-ID\0" + canonical(pres0))}}


def verify(bundle, *, keys, now, expected_audience=None, required_fields=(), max_age=300, replay=None, consume=True):
    if set(bundle) != {"header", "presentation"}: raise IntegrityError("bundle shape")
    h, p = bundle["header"], bundle["presentation"]
    if h.get("protocol") != PROTOCOL or h.get("signature_algorithm") != SIG_ALG: raise IntegrityError("protocol mismatch")
    key = keys.get(h.get("key_id"))
    if key is None: raise IntegrityError("unknown key")
    hu = {k:v for k,v in h.items() if k not in {"signature", "capsule_id"}}
    if not hmac.compare_digest(sign(b"NEXY-CAPSULE-HDR\0", hu, key), h.get("signature", "")): raise IntegrityError("header signature")
    h0 = {**hu, "signature": h["signature"]}
    if not hmac.compare_digest(hx(b"NEXY-CAPSULE-ID\0" + canonical(h0)), h.get("capsule_id", "")): raise IntegrityError("capsule id")
    if p.get("capsule_id") != h["capsule_id"]: raise IntegrityError("capsule binding")
    pu = {k:v for k,v in p.items() if k not in {"signature", "presentation_id"}}
    if not hmac.compare_digest(sign(b"NEXY-PRESENTATION\0", pu, key), p.get("signature", "")): raise IntegrityError("presentation signature")
    p0 = {**pu, "signature": p["signature"]}
    if not hmac.compare_digest(hx(b"NEXY-PRES-ID\0" + canonical(p0)), p.get("presentation_id", "")): raise IntegrityError("presentation id")
    if expected_audience is not None and p.get("audience") != expected_audience: raise IntegrityError("audience mismatch")
    issued, expires, shown = parse(h["issued_at"]), parse(h["expires_at"]), parse(p["presented_at"])
    now = now.astimezone(timezone.utc)
    if now < issued or now > expires or shown < issued or shown > expires: raise FreshnessError("outside validity interval")
    if max_age is not None and (now - shown).total_seconds() > max_age: raise FreshnessError("presentation too old")
    pid = p["presentation_id"]
    if replay is not None and pid in replay: raise ReplayError("replay")
    expected_root = bytes.fromhex(h["root"]); count = h["field_count"]
    seen_fields, seen_indices = set(), set()
    for item in p.get("disclosures", []):
        field, idx = item.get("field"), item.get("index")
        if field in seen_fields or idx in seen_indices: raise IntegrityError("duplicate disclosure")
        seen_fields.add(field); seen_indices.add(idx)
        try: salt = unb64(item["salt"])
        except Exception as exc: raise IntegrityError("invalid salt") from exc
        if not verify_proof(leaf(field, item["value"], salt), item["proof"], expected_root): raise IntegrityError("Merkle proof")
        if not isinstance(idx, int) or idx < 0 or idx >= count: raise IntegrityError("index")
    missing = set(required_fields) - seen_fields
    if missing: raise IntegrityError("missing required fields: " + ",".join(sorted(missing)))
    if replay is not None and consume: replay.add(pid)
    return {"capsule_id": h["capsule_id"], "presentation_id": pid, "fields": sorted(seen_fields)}
