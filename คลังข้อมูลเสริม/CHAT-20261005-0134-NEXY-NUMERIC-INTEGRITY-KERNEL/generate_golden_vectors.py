from __future__ import annotations
import json
from pathlib import Path
from nnik.canonical import canonical_dumps
from nnik.errors import NumericIntegrityError
from nnik.evaluator import evaluate
from nnik.fixed128 import project_exact
from nnik.units import BUILTIN_REGISTRY
ROOT = Path(__file__).resolve().parent

def eval_vector(name, contract, observation):
    return {"name":name,"input":{"contract":contract,"observation":observation},"expected":evaluate(contract,observation)}

def fixed_vector(name, value, quantum):
    try:
        output={"verdict":"ACCEPT","projection":project_exact(value,quantum)}
    except NumericIntegrityError as exc:
        output={"verdict":"FREEZE","reason_code":exc.code,"message":exc.message,"details":dict(exc.details or {})}
    return {"name":name,"input":{"value":value,"quantum":quantum},"expected":output}

def build_vectors():
    length_contract={"schema_version":"1","name":"golden-length","dimension":"length","canonical_unit":"m","lower":{"value":"1","inclusive":True},"upper":{"value":"2","inclusive":False},"normalization":{"quantum":None,"rounding_mode":None},"uncertainty_policy":"FREEZE_ON_BOUNDARY_OVERLAP"}
    temperature_contract={"schema_version":"1","name":"golden-temperature","dimension":"temperature","canonical_unit":"C","lower":{"value":"-1","inclusive":True},"upper":{"value":"1","inclusive":True},"normalization":{"quantum":None,"rounding_mode":None},"uncertainty_policy":"FREEZE_ON_BOUNDARY_OVERLAP"}
    doc_c_confidence={"schema_version":"1","name":"DOC-C confidence_min example","dimension":"dimensionless","canonical_unit":"1","lower":{"value":"0.85","inclusive":True},"upper":None,"normalization":{"quantum":None,"rounding_mode":None},"uncertainty_policy":"FREEZE_ON_BOUNDARY_OVERLAP"}
    quantized={"schema_version":"1","name":"golden-quantized","dimension":"length","canonical_unit":"m","lower":{"value":"1.2","inclusive":True},"upper":{"value":"1.3","inclusive":True},"normalization":{"quantum":"0.1","rounding_mode":"HALF_EVEN"},"uncertainty_policy":"FREEZE_ON_BOUNDARY_OVERLAP"}
    return {"schema_version":"1","purpose":"Cross-language semantic conformance vectors for the NNIK proposal","registry_digest":BUILTIN_REGISTRY.digest,"evaluation_vectors":[
        eval_vector("length_accept_exact_conversion",length_contract,{"value":"150","unit":"cm","uncertainty_abs":"0"}),
        eval_vector("length_exclusive_upper_reject",length_contract,{"value":"2","unit":"m","uncertainty_abs":"0"}),
        eval_vector("length_uncertainty_overlap_freeze",length_contract,{"value":"1.05","unit":"m","uncertainty_abs":"0.1"}),
        eval_vector("dimension_mismatch_freeze",length_contract,{"value":"1","unit":"s"}),
        eval_vector("temperature_32f_exact_zero_c",temperature_contract,{"value":"32","unit":"F","uncertainty_abs":"0"}),
        eval_vector("doc_c_confidence_example_accept",doc_c_confidence,{"value":"0.90","unit":"1","uncertainty_abs":"0"}),
        eval_vector("quantization_half_even",quantized,{"value":"1.25","unit":"m","uncertainty_abs":"0"})
    ],"fixed128_vectors":[
        fixed_vector("doc_c_confidence_0_85_centiscale","0.85","0.01"),
        fixed_vector("doc_c_match_0_90_centiscale","0.90","0.01"),
        fixed_vector("one_third_not_centiscale_representable","1/3","0.01")
    ]}

def main() -> int:
    payload=build_vectors()
    target=ROOT/"GOLDEN_VECTORS.json"
    target.write_text(json.dumps(payload,ensure_ascii=False,sort_keys=True,indent=2)+"
",encoding="utf-8")
    print(canonical_dumps({"written":str(target.name),"registry_digest":BUILTIN_REGISTRY.digest}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
