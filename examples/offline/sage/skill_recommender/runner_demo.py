from __future__ import annotations

import tempfile
from pathlib import Path

from .recommender import build_recommender
from .runner_printer import _print_query_results


def _run_demo() -> None:
    """Quick-start demo using real scenario data — no network or GEPA run required.

    Loads two synthetic scenarios (smarthub-support and code-review), builds
    their oracles from static golden examples, then routes one sample query per
    scenario so you can see the recommender output format.
    """
    from examples.offline.sage.data import get_scenario

    demo_scenario_names = ["smarthub-support", "code-review"]

    with tempfile.TemporaryDirectory(prefix="skill_recommender_demo_") as tmpdir:
        oracle_dir = Path(tmpdir)

        print("\n  Building demo oracle from real scenario examples …")
        scenarios = []
        for name in demo_scenario_names:
            s = get_scenario(name)
            s.build_oracle(oracle_dir, n_examples=50, overwrite=False)
            scenarios.append(s)

        rec = build_recommender(oracle_dir=oracle_dir, variant="baseline",
                                embedder_method="tfidf")
        print(f"  Loaded  : {rec.n_examples} rows · "
              f"{len(rec.skills)} skill(s) · {len(rec.metrics)} metric(s)")
        print(f"  Skills  : {rec.skills}")
        print(f"  Metrics : {rec.metrics}")

        # Route the sample query of each scenario through the recommender
        for s in scenarios:
            query = s.sample_query
            results = rec.recommend(query=query, sim_threshold=0.10,
                                    score_threshold=0.00, top_k=3)
            _print_query_results(results, query, "baseline")
