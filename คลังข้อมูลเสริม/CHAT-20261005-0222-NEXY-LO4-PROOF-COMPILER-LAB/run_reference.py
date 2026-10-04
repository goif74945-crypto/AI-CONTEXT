from nexy_lo4_lab.integration import run_reference_pipeline


if __name__ == "__main__":
    result = run_reference_pipeline()
    print("authority_digest=" + result.authority_digest)
    print("proof_probe_ids=" + ",".join(result.proof_probe_ids))
    print("witness_kinds=" + ",".join(result.witness_kinds))
    print("compile_status=" + result.compile_result.status)
    print("compile_digest=" + result.compile_result.digest)
