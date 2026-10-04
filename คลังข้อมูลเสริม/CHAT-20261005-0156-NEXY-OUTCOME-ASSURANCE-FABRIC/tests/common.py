from __future__ import annotations

from typing import Any


def contract_spec() -> dict[str, Any]:
    return {
        "objective_id": "deploy.safe-fast",
        "objective": "Deliver a safe deployment with bounded latency and preserved user trust",
        "criteria": [
            {
                "id": "availability",
                "path": "metrics.availability",
                "op": "min",
                "value": 99.9,
                "hard": True,
                "weight": 0,
                "regression_guard": True,
                "max_regression": 0.0,
            },
            {
                "id": "latency",
                "path": "metrics.latency_ms",
                "op": "max",
                "value": 200,
                "hard": False,
                "weight": 2,
                "regression_guard": True,
                "max_regression": 10,
            },
            {
                "id": "satisfaction",
                "path": "metrics.satisfaction",
                "op": "min",
                "value": 8.0,
                "hard": False,
                "weight": 3,
                "regression_guard": True,
                "max_regression": 0.2,
            },
        ],
        "forbidden_effects": [
            {"id": "no_data_loss", "path": "effects.data_loss", "op": "eq", "value": True}
        ],
    }


def good_observation() -> dict[str, Any]:
    return {
        "metrics": {"availability": 99.95, "latency_ms": 180, "satisfaction": 8.4},
        "effects": {"data_loss": False},
    }
