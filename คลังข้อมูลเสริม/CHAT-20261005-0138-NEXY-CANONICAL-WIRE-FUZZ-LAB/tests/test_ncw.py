import ast
import itertools
import json
from pathlib import Path
import unittest

from ncw import (
    DecodeError, I128_MAX, I128_MIN, Policy, StrictJSONError, ValidationError,
    canonical_sha256, decode, encode, loads_strict, malformed_mutations,
)


class NCWTests(unittest.TestCase):
    def test_round_trip(self):
        value={"min":I128_MIN,"max":I128_MAX,"n":-42,"s":"é ไทย","v":[False,True,None,{"x":7}]}
        self.assertEqual(decode(encode(value)), value)

    def test_map_order_and_hash_are_deterministic(self):
        a={"z":3,"a":1,"m":[True,None,"ไทย"]}; b={"m":[True,None,"ไทย"],"z":3,"a":1}
        self.assertEqual(encode(a),encode(b)); self.assertEqual(canonical_sha256(a),canonical_sha256(b))

    def test_all_six_key_permutations_match(self):
        items=[("a",1),("b",2),("c",3),("d",4),("é",5),("ไทย",6)]
        expected=encode(dict(items)); count=0
        for perm in itertools.permutations(items):
            self.assertEqual(encode(dict(perm)),expected); count+=1
        self.assertEqual(count,720)

    def test_bool_is_not_integer_encoding(self):
        self.assertNotEqual(encode(True),encode(1)); self.assertNotEqual(encode(False),encode(0))

    def test_i128_boundaries(self):
        for good in (I128_MIN,I128_MAX): self.assertEqual(decode(encode(good)),good)
        for bad in (I128_MIN-1,I128_MAX+1):
            with self.assertRaises(ValidationError): encode(bad)

    def test_unsupported_types_fail_closed(self):
        for bad in (1.0,(1,2),b"x",bytearray(b"x"),{1:"x"}):
            with self.subTest(kind=type(bad).__name__), self.assertRaises(ValidationError): encode(bad)

    def test_non_nfc_rejected(self):
        with self.assertRaises(ValidationError): encode("e\u0301")

    def test_limits(self):
        with self.assertRaises(ValidationError): encode([[[0]]],Policy(max_depth=1))
        with self.assertRaises(ValidationError): encode([1,2,3],Policy(max_container_items=2))
        with self.assertRaises(ValidationError): encode("ไทย",Policy(max_string_bytes=3))

    def test_duplicate_json_key_rejected(self):
        raw='{"a":1,"a":2}'
        self.assertEqual(json.loads(raw),{"a":2})
        with self.assertRaises(StrictJSONError): loads_strict(raw)

    def test_nfc_key_collision_rejected(self):
        with self.assertRaises(StrictJSONError): loads_strict('{"é":1,"e\\u0301":2}')

    def test_float_and_nonstandard_numbers_rejected(self):
        for raw in ('{"x":1.0}','{"x":1e3}','{"x":NaN}','{"x":Infinity}','{"x":-Infinity}'):
            with self.subTest(raw=raw), self.assertRaises(StrictJSONError): loads_strict(raw)

    def test_json_surface_variants_converge(self):
        variants=('{"a":1,"b":[true,null],"c":"ไทย"}',' { "c":"ไทย", "b":[true,null], "a":1 } ')
        self.assertEqual(len({encode(loads_strict(v)) for v in variants}),1)

    def test_raw_json_size_gate(self):
        with self.assertRaises(StrictJSONError): loads_strict(" "*20+"null",Policy(max_json_text_bytes=8))

    def test_lone_surrogate_rejected(self):
        with self.assertRaises(StrictJSONError): loads_strict('{"x":"\\ud800"}')

    def test_wire_corruption_rejected(self):
        valid=encode({"x":1})
        bads=[b"BAD!\x00",b"NCW1\xff",valid+b"x",valid[:-1],b"NCW1\x03\x00",b"NCW1\x04\x00\x00\x00\x01\xff"]
        for bad in bads:
            with self.subTest(bad=bad.hex()), self.assertRaises(DecodeError): decode(bad)

    def test_non_nfc_wire_rejected(self):
        raw="e\u0301".encode(); wire=b"NCW1\x04"+len(raw).to_bytes(4,"big")+raw
        with self.assertRaises(DecodeError): decode(wire)

    def test_noncanonical_map_order_and_duplicate_rejected(self):
        i1=b"\x03"+(1).to_bytes(16,"big",signed=True); i2=b"\x03"+(2).to_bytes(16,"big",signed=True)
        desc=b"NCW1\x06\x00\x00\x00\x02"+b"\x00\x00\x00\x01b"+i1+b"\x00\x00\x00\x01a"+i2
        dup=b"NCW1\x06\x00\x00\x00\x02"+b"\x00\x00\x00\x01a"+i1+b"\x00\x00\x00\x01a"+i2
        for bad in (desc,dup):
            with self.assertRaises(DecodeError): decode(bad)

    def test_golden_vectors(self):
        fixture=json.loads((Path(__file__).parents[1]/"fixtures/golden_vectors.json").read_text(encoding="utf-8"))
        self.assertEqual(fixture["format"],"NCW1")
        for v in fixture["vectors"]:
            with self.subTest(vector=v["id"]):
                wire=encode(v["value"])
                self.assertEqual(wire.hex(),v["wire_hex"])
                self.assertEqual(canonical_sha256(v["value"]),v["sha256"])
                self.assertEqual(encode(decode(wire)),wire)

    def test_generated_small_domain(self):
        scalars=[None,False,True,-2,-1,0,1,2,"","a","é","ไทย"]
        values=list(scalars)+[[x] for x in scalars]+[[x,y] for x,y in itertools.product(scalars[:8],repeat=2)]
        values += [{"a":x,"b":y} for x,y in itertools.product(scalars[:8],repeat=2)]
        self.assertGreaterEqual(len(values),150)
        for value in values:
            wire=encode(value); self.assertEqual(encode(decode(wire)),wire)

    def test_deterministic_malformed_mutation_corpus(self):
        base=encode({"a":[1,2,3],"b":"ไทย"})
        cases=malformed_mutations(base)
        self.assertGreaterEqual(len(cases),10)
        self.assertEqual(len({c.mutation_id for c in cases}),len(cases))
        for case in cases:
            with self.subTest(case=case.mutation_id):
                if case.should_decode:
                    decode(case.data)
                else:
                    with self.assertRaises(DecodeError): decode(case.data)

    def test_core_imports_avoid_common_side_effect_modules(self):
        tree=ast.parse((Path(__file__).parents[1]/"src/ncw.py").read_text(encoding="utf-8"))
        forbidden={"os","pathlib","random","secrets","socket","subprocess","time","datetime","urllib","http","requests","aiohttp","sqlite3"}
        violations=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                violations += [a.name for a in node.names if a.name.split(".",1)[0] in forbidden]
            elif isinstance(node,ast.ImportFrom) and node.module and node.module.split(".",1)[0] in forbidden:
                violations.append(node.module)
        self.assertEqual(violations,[])


if __name__ == "__main__": unittest.main()
