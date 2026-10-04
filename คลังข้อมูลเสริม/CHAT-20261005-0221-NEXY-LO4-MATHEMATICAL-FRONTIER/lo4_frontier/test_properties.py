import itertools
import random
import unittest

from lo4_frontier.minimal_cut_failure_geometry.engine import minimal_failure_cut_sets
from lo4_frontier.liveness_deadlock_sentinel.engine import analyze_liveness
from lo4_frontier.dependency_dominator_analyzer.engine import compute_dominators, critical_dominators
from lo4_frontier.symmetry_state_space_reducer.engine import canonical_partition_key
from lo4_frontier.lo4_mutation_tournament.engine import run_tournament


def brute_minimal_hitting_sets(paths):
    universe = sorted(set().union(*paths))
    hits = []
    for size in range(1, len(universe) + 1):
        for combo in itertools.combinations(universe, size):
            chosen = set(combo)
            if all(chosen & path for path in paths):
                if not any(set(existing) < chosen for existing in hits):
                    hits.append(combo)
    return tuple(sorted(hits, key=lambda item: (len(item), item)))


def simple_paths(graph, start, target):
    result = []
    stack = [(start, (start,))]
    while stack:
        node, path = stack.pop()
        if node == target:
            result.append(path)
            continue
        for nxt in reversed(graph.get(node, [])):
            if nxt not in path:
                stack.append((nxt, path + (nxt,)))
    return result


class MinimalCutPropertyTests(unittest.TestCase):
    def test_random_small_instances_match_bruteforce(self):
        rng = random.Random(20261005)
        nodes = ["a", "b", "c", "d", "e"]
        for _ in range(80):
            paths = []
            for _ in range(rng.randint(1, 5)):
                path = set(rng.sample(nodes, rng.randint(1, 3)))
                paths.append(path)
            self.assertEqual(minimal_failure_cut_sets(paths), brute_minimal_hitting_sets(paths))

    def test_every_result_hits_every_path_and_is_minimal(self):
        paths = [{"a", "b", "c"}, {"b", "d"}, {"c", "d"}]
        for result in minimal_failure_cut_sets(paths):
            chosen = set(result)
            self.assertTrue(all(chosen & path for path in paths))
            for node in chosen:
                smaller = chosen - {node}
                self.assertFalse(all(smaller & path for path in paths))

    def test_redundant_superset_path_does_not_change_answer(self):
        core = [{"a", "b"}, {"c"}]
        redundant = core + [{"a", "b", "d"}]
        self.assertEqual(minimal_failure_cut_sets(core), minimal_failure_cut_sets(redundant))


class LivenessPropertyTests(unittest.TestCase):
    def test_input_permutation_does_not_change_result(self):
        items = [
            {"id":"a","state":"WAITING","waits_for":["b"]},
            {"id":"b","state":"WAITING","waits_for":["c"]},
            {"id":"c","state":"WAITING","waits_for":["a"]},
        ]
        expected = analyze_liveness(items)
        for perm in itertools.permutations(items):
            self.assertEqual(analyze_liveness(perm), expected)

    def test_terminal_dependency_does_not_create_false_deadlock(self):
        items = [
            {"id":"done","state":"PASS","waits_for":[]},
            {"id":"ready","state":"READY","waits_for":["done"]},
        ]
        self.assertEqual(analyze_liveness(items)["status"], "PROGRESSABLE")

    def test_self_wait_is_deadlock(self):
        result = analyze_liveness([{"id":"a","state":"WAITING","waits_for":["a"]}])
        self.assertEqual(result["status"], "DEADLOCK")
        self.assertEqual(result["cycles"], (("a",),))

    def test_duplicate_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            analyze_liveness([
                {"id":"a","state":"READY","waits_for":[]},
                {"id":"a","state":"READY","waits_for":[]},
            ])


class DominatorPropertyTests(unittest.TestCase):
    def test_dominators_match_all_simple_paths_definition(self):
        graph = {
            "s":["a","b"],
            "a":["c","d"],
            "b":["c"],
            "c":["e"],
            "d":["e"],
            "e":["t"],
            "t":[],
        }
        dom = compute_dominators(graph, "s")
        for target in dom:
            paths = simple_paths(graph, "s", target)
            expected = set(paths[0])
            for path in paths[1:]:
                expected &= set(path)
            self.assertEqual(set(dom[target]), expected)

    def test_shared_critical_dominator_matches_path_intersection(self):
        graph = {"s":["a"], "a":["b","c"], "b":["x"], "c":["y"], "x":[], "y":[]}
        self.assertEqual(critical_dominators(graph, "s", ["x","y"]), ("a",))

    def test_unknown_start_rejected(self):
        with self.assertRaises(ValueError):
            compute_dominators({"a":[]}, "missing")

    def test_unreachable_target_rejected(self):
        graph = {"s":["a"], "a":[], "z":[]}
        with self.assertRaises(ValueError):
            critical_dominators(graph, "s", ["a","z"])


class SymmetryPropertyTests(unittest.TestCase):
    def test_all_worker_id_permutations_collapse(self):
        states = [{"q":0},{"q":1},{"q":2}]
        keys = set()
        for perm in itertools.permutations(states):
            entities = {f"id-{i}": {"class":"worker", "state":state} for i, state in enumerate(perm)}
            keys.add(canonical_partition_key(entities))
        self.assertEqual(len(keys), 1)

    def test_nested_json_key_order_is_irrelevant(self):
        a = {"x":{"class":"worker","state":{"a":1,"b":{"x":2,"y":3}}}}
        b = {"z":{"class":"worker","state":{"b":{"y":3,"x":2},"a":1}}}
        self.assertEqual(canonical_partition_key(a), canonical_partition_key(b))

    def test_non_json_state_rejected(self):
        with self.assertRaises(ValueError):
            canonical_partition_key({"x":{"class":"worker","state":{"bad":{1,2}}}})

    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            canonical_partition_key({"x":{"class":"worker","state":{"bad":float("nan")}}})


class TournamentPropertyTests(unittest.TestCase):
    def candidate(self, candidate_id, **metrics):
        base = {"safety":0.95,"utility":0.8,"proof":0.9,"reversibility":0.9,"novelty":0.8}
        base.update(metrics)
        return {"id":candidate_id,"metrics":base,"invariant_failures":[]}

    def test_promotion_is_never_permitted(self):
        for candidates in [
            [self.candidate("a")],
            [self.candidate("a"), self.candidate("b", novelty=0.9)],
            [{**self.candidate("x"), "invariant_failures":["WRITE_CANON"]}],
        ]:
            self.assertFalse(run_tournament(candidates)["promotion_permitted"])

    def test_input_permutation_is_deterministic(self):
        candidates = [
            self.candidate("a", utility=0.7, novelty=0.9),
            self.candidate("b", utility=0.9, novelty=0.7),
            self.candidate("c", utility=0.8, novelty=0.8),
        ]
        expected = run_tournament(candidates)
        for perm in itertools.permutations(candidates):
            self.assertEqual(run_tournament(perm), expected)

    def test_metric_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            run_tournament([self.candidate("x", novelty=1.01)])

    def test_unknown_metric_rejected(self):
        c = self.candidate("x")
        c["metrics"]["bonus"] = 1
        with self.assertRaises(ValueError):
            run_tournament([c])

    def test_dominated_candidate_never_wins(self):
        strong = self.candidate("strong", utility=0.9, novelty=0.9)
        weak = self.candidate("weak", utility=0.7, novelty=0.7)
        result = run_tournament([weak, strong])
        self.assertEqual(result["winner_id"], "strong")
        self.assertNotIn("weak", result["pareto_ids"])


if __name__ == "__main__":
    unittest.main()
