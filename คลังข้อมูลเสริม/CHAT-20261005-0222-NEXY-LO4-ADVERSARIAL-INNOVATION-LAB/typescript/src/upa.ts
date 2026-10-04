export type TruthState = "TRUE" | "FALSE" | "UNKNOWN" | "CONFLICT";
type Bits = readonly [0 | 1, 0 | 1];

const bits: Record<TruthState, Bits> = {
  TRUE: [1, 0],
  FALSE: [0, 1],
  UNKNOWN: [0, 0],
  CONFLICT: [1, 1],
};

function fromBits(value: Bits): TruthState {
  const key = `${value[0]}${value[1]}`;
  if (key === "10") return "TRUE";
  if (key === "01") return "FALSE";
  if (key === "00") return "UNKNOWN";
  return "CONFLICT";
}

export class EvidenceValue {
  public readonly state: TruthState;
  public readonly provenance: readonly string[];

  public constructor(state: TruthState, provenance: readonly string[] = []) {
    const unique = [...new Set(provenance)];
    if (unique.length !== provenance.length || unique.some((x) => x.length === 0)) {
      throw new Error("provenance entries must be unique and non-empty");
    }
    this.state = state;
    this.provenance = Object.freeze(unique);
    Object.freeze(this);
  }

  public get releaseable(): boolean { return this.state === "TRUE"; }

  private merge(other: EvidenceValue): readonly string[] {
    return Object.freeze([...new Set([...this.provenance, ...other.provenance])]);
  }

  public negate(): EvidenceValue {
    const [t, f] = bits[this.state];
    return new EvidenceValue(fromBits([f, t]), this.provenance);
  }

  public and(other: EvidenceValue): EvidenceValue {
    const [t1, f1] = bits[this.state];
    const [t2, f2] = bits[other.state];
    return new EvidenceValue(fromBits([(t1 & t2) as 0 | 1, (f1 | f2) as 0 | 1]), this.merge(other));
  }

  public or(other: EvidenceValue): EvidenceValue {
    const [t1, f1] = bits[this.state];
    const [t2, f2] = bits[other.state];
    return new EvidenceValue(fromBits([(t1 | t2) as 0 | 1, (f1 & f2) as 0 | 1]), this.merge(other));
  }

  public knowledgeJoin(other: EvidenceValue): EvidenceValue {
    const [t1, f1] = bits[this.state];
    const [t2, f2] = bits[other.state];
    return new EvidenceValue(fromBits([(t1 | t2) as 0 | 1, (f1 | f2) as 0 | 1]), this.merge(other));
  }

  public static requireAll(values: readonly EvidenceValue[]): EvidenceValue {
    if (values.length === 0) throw new Error("requireAll needs at least one value");
    let current = values[0];
    if (current === undefined) throw new Error("unreachable empty values");
    for (let i = 1; i < values.length; i += 1) {
      const next = values[i];
      if (next === undefined) throw new Error("invalid sparse values");
      current = current.and(next);
    }
    return current;
  }
}
