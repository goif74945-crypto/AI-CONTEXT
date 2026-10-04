export interface InfluenceNode {
  readonly nodeId: string;
  readonly parents: Readonly<Record<string, number>>;
  readonly isAgentSource?: boolean;
  readonly verified?: boolean;
}

export interface InfluenceReport {
  readonly targetId: string;
  readonly sourceInfluence: readonly (readonly [string, number])[];
  readonly dominantSource: string;
  readonly dominanceRatio: number;
  readonly effectiveSourceCount: number;
  readonly unverifiedInfluence: number;
  readonly status: "PASS" | "FREEZE";
  readonly reasons: readonly string[];
}

export class InfluenceGraph {
  private readonly nodes: ReadonlyMap<string, InfluenceNode>;

  public constructor(nodes: readonly InfluenceNode[]) {
    if (nodes.length === 0) throw new Error("at least one node is required");
    const map = new Map<string, InfluenceNode>();
    for (const node of nodes) {
      if (!node.nodeId || map.has(node.nodeId)) throw new Error("nodeId values must be unique and non-empty");
      if (node.isAgentSource && Object.keys(node.parents).length !== 0) throw new Error("agent source nodes cannot have parents");
      for (const [parent, weight] of Object.entries(node.parents)) {
        if (!parent || !Number.isFinite(weight) || weight <= 0) throw new Error("invalid influence edge");
      }
      map.set(node.nodeId, Object.freeze({ ...node, parents: Object.freeze({ ...node.parents }) }));
    }
    for (const node of map.values()) {
      for (const parent of Object.keys(node.parents)) if (!map.has(parent)) throw new Error(`missing parent: ${parent}`);
    }
    this.nodes = map;
  }

  private contributions(nodeId: string, visiting: Set<string>, memo: Map<string, Map<string, number>>): Map<string, number> {
    const cached = memo.get(nodeId);
    if (cached !== undefined) return cached;
    if (visiting.has(nodeId)) throw new Error(`cycle detected at ${nodeId}`);
    const node = this.nodes.get(nodeId);
    if (node === undefined) throw new Error("unknown node");
    if (node.isAgentSource) {
      const result = new Map([[nodeId, 1]]);
      memo.set(nodeId, result);
      return result;
    }
    const entries = Object.entries(node.parents).sort(([a], [b]) => a.localeCompare(b));
    if (entries.length === 0) throw new Error(`non-source node ${nodeId} has no parents`);
    visiting.add(nodeId);
    const totalWeight = entries.reduce((sum, [, weight]) => sum + weight, 0);
    const out = new Map<string, number>();
    for (const [parentId, edgeWeight] of entries) {
      const factor = edgeWeight / totalWeight;
      for (const [source, influence] of this.contributions(parentId, visiting, memo)) {
        out.set(source, (out.get(source) ?? 0) + factor * influence);
      }
    }
    visiting.delete(nodeId);
    memo.set(nodeId, out);
    return out;
  }

  public analyze(targetId: string, maxDominanceRatio = 0.70, maxUnverifiedInfluence = 0.10): InfluenceReport {
    if (!this.nodes.has(targetId)) throw new Error("unknown targetId");
    if (maxDominanceRatio < 0 || maxDominanceRatio > 1) throw new Error("invalid maxDominanceRatio");
    if (maxUnverifiedInfluence < 0 || maxUnverifiedInfluence > 1) throw new Error("invalid maxUnverifiedInfluence");
    const contrib = this.contributions(targetId, new Set(), new Map());
    const total = [...contrib.values()].reduce((a, b) => a + b, 0);
    const ordered = [...contrib.entries()]
      .map(([source, value]) => [source, value / total] as const)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    const dominant = ordered[0];
    if (dominant === undefined) throw new Error("target has no source ancestry");
    const concentration = ordered.reduce((sum, [, value]) => sum + value * value, 0);
    const unverifiedInfluence = ordered.reduce((sum, [source, value]) => {
      const sourceNode = this.nodes.get(source);
      return sum + (sourceNode?.verified === true ? 0 : value);
    }, 0);
    const reasons: string[] = [];
    if (dominant[1] > maxDominanceRatio) reasons.push("single_source_dominance");
    if (unverifiedInfluence > maxUnverifiedInfluence) reasons.push("unverified_influence_exceeded");
    return Object.freeze({
      targetId,
      sourceInfluence: Object.freeze(ordered),
      dominantSource: dominant[0],
      dominanceRatio: dominant[1],
      effectiveSourceCount: 1 / concentration,
      unverifiedInfluence,
      status: reasons.length === 0 ? "PASS" : "FREEZE",
      reasons: Object.freeze(reasons),
    });
  }
}
